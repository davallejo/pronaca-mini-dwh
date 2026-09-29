"""Genera datos FICTICIOS de PRONACA con errores sembrados a propósito
para demostrar limpieza y calidad de datos. Tres fuentes dispares:
  - productos.csv  (catálogo)
  - clientes.json  (CRM)
  - ventas.csv     (ERP)
"""
import json
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

random.seed(42)
RAW = Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

# ---------- Fuente 1: productos (CSV) ----------
productos = [
    (1, "Pollo entero", "Pollo", "kg", 3.20),
    (2, "Pechuga de pollo", "Pollo", "kg", 5.10),
    (3, "Alitas de pollo", "Pollo", "kg", 4.30),
    (4, "Nuggets de pollo", "Pollo", "caja", 6.50),
    (5, "Chuleta de cerdo", "Cerdo", "kg", 5.80),
    (6, "Costilla de cerdo", "Cerdo", "kg", 6.40),
    (7, "Jamón cocido", "Embutidos", "kg", 7.90),
    (8, "Salchicha", "Embutidos", "paquete", 3.60),
    (9, "Mortadela", "Embutidos", "kg", 4.90),
    (10, "Chorizo", "Embutidos", "paquete", 4.20),
]
pd.DataFrame(
    productos,
    columns=["id_producto", "nombre", "categoria", "unidad", "precio_lista"],
).to_csv(RAW / "productos.csv", index=False)

# ---------- Fuente 2: clientes (JSON) con ciudades sucias ----------
ciudades_sucias = ["Quito", "quito ", "GUAYAQUIL", "Guayaquil", " Cuenca",
                   "cuenca", "Ambato", "Manta", "MANTA"]
canales = ["Supermercado", "Tienda de barrio", "Restaurante", "Distribuidor"]
clientes = []
for i in range(1, 21):
    clientes.append({
        "id_cliente": i,
        "nombre": f"Cliente {i:02d}",
        "canal": random.choice(canales),
        "ciudad": random.choice(ciudades_sucias),
    })
with open(RAW / "clientes.json", "w", encoding="utf-8") as f:
    json.dump(clientes, f, ensure_ascii=False, indent=2)

# ---------- Fuente 3: ventas (CSV) con errores ----------
precios = {p[0]: p[4] for p in productos}
inicio = date(2025, 1, 1)
filas = []
for i in range(1, 301):
    d = inicio + timedelta(days=random.randint(0, 179))
    idp = random.randint(1, 10)
    # Fechas en dos formatos distintos (inconsistencia)
    fecha = d.strftime("%d/%m/%Y") if random.random() < 0.15 else d.isoformat()
    filas.append({
        "id_venta": i,
        "fecha": fecha,
        "id_cliente": random.randint(1, 20),
        "id_producto": idp,
        "cantidad": random.randint(5, 120),
        "precio_unitario": round(precios[idp] * random.uniform(0.95, 1.05), 2),
    })

# Errores sembrados
filas[10]["cantidad"] = -5        # cantidad negativa
filas[25]["cantidad"] = 0         # cantidad cero
filas[40]["id_cliente"] = None    # cliente nulo
filas[55]["id_producto"] = 99     # producto inexistente
filas[70]["id_cliente"] = 777     # cliente inexistente
filas.append(dict(filas[5]))      # duplicado exacto
filas.append(dict(filas[6]))      # duplicado exacto

pd.DataFrame(filas).to_csv(RAW / "ventas.csv", index=False)
print("✅ Datos generados en data/raw/ (productos.csv, clientes.json, ventas.csv)")
