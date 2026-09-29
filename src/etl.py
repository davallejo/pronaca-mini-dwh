"""ETL: Extrae 3 fuentes -> limpia y valida -> carga esquema estrella en SQLite.
Incluye reporte de calidad basado en dimensiones DAMA.
"""
import json
import sqlite3
from pathlib import Path

import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)
DB_PATH = Path("data/pronaca_dwh.db")

MESES = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo",
         6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre",
         10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def parsear_fecha(valor):
    """Acepta AAAA-MM-DD y DD/MM/AAAA."""
    v = str(valor).strip()
    if "/" in v:
        return pd.to_datetime(v, format="%d/%m/%Y", errors="coerce")
    return pd.to_datetime(v, format="%Y-%m-%d", errors="coerce")


# ---------------- EXTRACT ----------------
def extraer():
    productos = pd.read_csv(RAW / "productos.csv")
    with open(RAW / "clientes.json", encoding="utf-8") as f:
        clientes = pd.DataFrame(json.load(f))
    ventas = pd.read_csv(RAW / "ventas.csv")
    return productos, clientes, ventas


# ---------------- TRANSFORM ----------------
def transformar(productos, clientes, ventas):
    calidad = []
    total_inicial = len(ventas)

    def registrar(dimension, regla, total, errores):
        ok = round(100 * (total - errores) / total, 2) if total else 100.0
        calidad.append((dimension, regla, total, errores, ok))

    # Consistencia: normalizar ciudades (espacios y mayúsculas)
    ciudades_antes = clientes["ciudad"].nunique()
    clientes["ciudad"] = clientes["ciudad"].str.strip().str.title()
    registrar("Consistencia", "Ciudades con formato único (strip + title)",
              len(clientes), ciudades_antes - clientes["ciudad"].nunique())

    # Unicidad: duplicados exactos
    duplicados = ventas.duplicated().sum()
    registrar("Unicidad", "Ventas sin duplicados exactos", total_inicial, int(duplicados))
    ventas = ventas.drop_duplicates().copy()

    # Consistencia: fechas en formato único
    ventas["fecha_dt"] = ventas["fecha"].apply(parsear_fecha)
    fechas_malas = ventas["fecha_dt"].isna().sum()
    registrar("Consistencia", "Fechas parseables (ISO y DD/MM/AAAA)",
              len(ventas), int(fechas_malas))

    # Reglas de rechazo
    ventas["motivo_rechazo"] = ""

    m = ventas["id_cliente"].isna()
    registrar("Completitud", "id_cliente no nulo", len(ventas), int(m.sum()))
    ventas.loc[m, "motivo_rechazo"] = "cliente nulo"

    m = ventas["cantidad"] <= 0
    registrar("Validez", "cantidad > 0", len(ventas), int(m.sum()))
    ventas.loc[m & (ventas["motivo_rechazo"] == ""), "motivo_rechazo"] = "cantidad no positiva"

    m = ~ventas["id_producto"].isin(productos["id_producto"])
    registrar("Integridad referencial", "id_producto existe en dim_producto",
              len(ventas), int(m.sum()))
    ventas.loc[m & (ventas["motivo_rechazo"] == ""), "motivo_rechazo"] = "producto inexistente"

    m = ventas["id_cliente"].notna() & ~ventas["id_cliente"].isin(clientes["id_cliente"])
    registrar("Integridad referencial", "id_cliente existe en dim_cliente",
              len(ventas), int(m.sum()))
    ventas.loc[m & (ventas["motivo_rechazo"] == ""), "motivo_rechazo"] = "cliente inexistente"

    rechazadas = ventas[ventas["motivo_rechazo"] != ""].copy()
    validas = ventas[ventas["motivo_rechazo"] == ""].copy()

    validas["id_cliente"] = validas["id_cliente"].astype(int)
    validas["id_fecha"] = validas["fecha_dt"].dt.strftime("%Y%m%d").astype(int)
    validas["total"] = (validas["cantidad"] * validas["precio_unitario"]).round(2)
    fact = validas[["id_venta", "id_fecha", "id_cliente", "id_producto",
                    "cantidad", "precio_unitario", "total"]]

    # Dimensión fecha
    fechas = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    dim_fecha = pd.DataFrame({
        "id_fecha": fechas.strftime("%Y%m%d").astype(int),
        "fecha": fechas.strftime("%Y-%m-%d"),
        "anio": fechas.year,
        "mes": fechas.month,
        "nombre_mes": [MESES[x] for x in fechas.month],
        "trimestre": fechas.quarter,
        "dia_semana": [DIAS[x] for x in fechas.dayofweek],
    })

    df_calidad = pd.DataFrame(
        calidad,
        columns=["dimension_dama", "regla", "registros_total",
                 "registros_error", "porcentaje_ok"])
    return productos, clientes, dim_fecha, fact, rechazadas, df_calidad


# ---------------- LOAD ----------------
def cargar(dim_producto, dim_cliente, dim_fecha, fact, df_calidad):
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    con.executescript(Path("sql/01_crear_esquema.sql").read_text(encoding="utf-8"))
    dim_producto.to_sql("dim_producto", con, if_exists="append", index=False)
    dim_cliente.to_sql("dim_cliente", con, if_exists="append", index=False)
    dim_fecha.to_sql("dim_fecha", con, if_exists="append", index=False)
    fact.to_sql("fact_ventas", con, if_exists="append", index=False)
    df_calidad.to_sql("calidad_datos", con, if_exists="append", index=False)
    con.commit()
    con.close()


def main():
    productos, clientes, ventas = extraer()
    dprod, dcli, dfec, fact, rech, cal = transformar(productos, clientes, ventas)
    cargar(dprod, dcli, dfec, fact, cal)

    # Exportar CSV (para Tableau / Power BI / Spark)
    dprod.to_csv(OUT / "dim_producto.csv", index=False)
    dcli.to_csv(OUT / "dim_cliente.csv", index=False)
    dfec.to_csv(OUT / "dim_fecha.csv", index=False)
    fact.to_csv(OUT / "fact_ventas.csv", index=False)
    rech.to_csv(OUT / "ventas_rechazadas.csv", index=False)
    cal.to_csv(OUT / "reporte_calidad.csv", index=False)

    print(f"✅ Base creada: {DB_PATH}")
    print(f"   Ventas cargadas:    {len(fact)}")
    print(f"   Ventas rechazadas:  {len(rech)}")
    print("\n📊 Reporte de calidad (DAMA):")
    print(cal.to_string(index=False))


if __name__ == "__main__":
    main()
