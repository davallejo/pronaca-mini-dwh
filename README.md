<div align="center">

# 🐔🐖 Mini Data Warehouse de Ventas – Caso PRONACA

**Proyecto demostrativo de Ingeniería de Datos: integración, calidad (DAMA), modelo dimensional, SQL, Python y Spark**

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?logo=scipy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![Apache Spark](https://img.shields.io/badge/PySpark-E25A1C?logo=apachespark&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white)
![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00?logo=googlecolab&logoColor=white)
![Tableau](https://img.shields.io/badge/Tableau%20Public-E97627?logo=tableau&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)

</div>

> ⚠️ **Aviso:** proyecto **demostrativo**. Todos los datos son **ficticios** y generados por código. No pertenecen a PRONACA ni representan sus operaciones reales.

---

## 📑 Contenido

- [🎯 Objetivo](#-objetivo)
- [🧭 Escenario](#-escenario)
- [🧩 Arquitectura](#-arquitectura)
- [🛠️ Tecnologías](#️-tecnologías)
- [📁 Estructura del proyecto](#-estructura-del-proyecto)
- [📐 Modelo de datos](#-modelo-de-datos)
- [✅ Calidad de datos (DAMA)](#-calidad-de-datos-dama)
- [🔐 Integridad y seguridad](#-integridad-y-seguridad)
- [▶️ Cómo ejecutarlo](#️-cómo-ejecutarlo)
- [📊 Dashboard](#-dashboard)
- [🗺️ Competencias demostradas](#️-competencias-demostradas)
- [🚀 Próximos pasos](#-próximos-pasos)
- [👤 Autor](#-autor)

---

## 🎯 Objetivo

Demostrar, en un proyecto pequeño y reproducible, las habilidades clave de un/a **Ingeniero/a de Datos**:

- 🗄️ Administrar repositorios de datos con integridad y seguridad.
- 📐 Diseñar estructuras de datos optimizadas para análisis (modelo multidimensional).
- 🔗 Integrar fuentes de datos dispares garantizando consistencia y calidad.
- 📝 Documentar estructuras y repositorios para facilitar su uso.

## 🧭 Escenario

Una empresa de alimentos (línea de **pollo 🐔, cerdo 🐖 y embutidos 🌭**) recibe información de ventas desde tres sistemas distintos, cada uno con su formato y sus errores:

| Fuente | Formato | Sistema simulado | Problemas sembrados |
|---|---|---|---|
| `productos.csv` | 📄 CSV | Catálogo de productos | — |
| `clientes.json` | 🧾 JSON | CRM de clientes | Ciudades con espacios y mayúsculas inconsistentes |
| `ventas.csv` | 📄 CSV | ERP de ventas | Duplicados, cantidades negativas o cero, clientes nulos, claves inexistentes, fechas en 2 formatos |

El proyecto los integra en un **Data Warehouse** listo para análisis, y separa los registros inválidos con su motivo de rechazo.

## 🧩 Arquitectura

```
📄 productos.csv ─┐
🧾 clientes.json ─┼─► 🐍 ETL (Pandas) ─► ✅ Calidad DAMA ─► 🗄️ SQLite (esquema estrella) ─┬─► 📊 Tableau Public
📄 ventas.csv ────┘          │                                                            └─► 📓 Notebook (SciPy / scikit-learn / ⚡ PySpark)
                             └─► 🚫 ventas_rechazadas.csv (con motivo)
```

## 🛠️ Tecnologías

| | Herramienta | Uso en el proyecto |
|---|---|---|
| 🐍 | **Python** | Lenguaje principal |
| 🐼 | **Pandas** | Extracción, limpieza y transformación |
| 🔢 | **NumPy / SciPy** | Estadística descriptiva y correlación |
| 🤖 | **scikit-learn** | Pronóstico simple de ventas |
| 🗄️ | **SQLite + SQL** | Repositorio de datos y consultas analíticas |
| ⚡ | **PySpark** | Procesamiento distribuido de la tabla de hechos |
| 📓 | **Jupyter / Google Colab** | Notebook reproducible en la nube |
| 📊 | **Tableau Public** | Dashboard interactivo |
| 🐙 | **GitHub** | Versionado y portafolio |

> 💸 Todo el stack es **gratuito y sin suscripción**.

## 📁 Estructura del proyecto

```
pronaca-mini-dwh/
├── README.md
├── requirements.txt
├── .gitignore
├── sql/
│   ├── 01_crear_esquema.sql          # DDL: tablas, PK, FK, CHECK, índices, vista
│   └── 02_consultas_analiticas.sql   # Consultas de negocio
├── src/
│   ├── generar_datos.py              # Genera las 3 fuentes con errores sembrados
│   └── etl.py                        # Extract → Transform → Load + reporte de calidad
├── docs/
│   └── diccionario_datos.md          # Documentación de estructuras
├── notebooks/
│   └── pronaca_dwh.ipynb             # Análisis en Colab
└── data/
    ├── raw/                          # Fuentes originales (generadas)
    ├── processed/                    # CSV limpios + reporte de calidad
    └── pronaca_dwh.db                # Base de datos SQLite
```

## 📐 Modelo de datos

Modelo **multidimensional (esquema estrella)** con grano de una línea de venta.

```
            ┌──────────────┐
            │  dim_fecha   │
            └──────┬───────┘
┌──────────────┐   │   ┌──────────────┐
│ dim_producto ├───┼───┤  dim_cliente │
└──────────────┘   │   └──────────────┘
              ┌────┴──────┐
              │fact_ventas│
              └───────────┘
```

| Tabla | Tipo | Descripción |
|---|---|---|
| `fact_ventas` | Hechos | Cantidad, precio unitario y total por venta |
| `dim_producto` | Dimensión | Nombre, categoría, unidad y precio de lista |
| `dim_cliente` | Dimensión | Nombre, canal y ciudad normalizada |
| `dim_fecha` | Dimensión | Año, mes, trimestre y día de la semana |
| `calidad_datos` | Control | Resultado de las reglas de calidad |
| `v_ventas_mensuales` | Vista | Ventas mensuales por categoría (capa de consumo) |

📘 Detalle completo en el [**diccionario de datos**](docs/diccionario_datos.md).

## ✅ Calidad de datos (DAMA)

El ETL aplica reglas alineadas a las dimensiones de calidad de **DAMA** y registra el resultado en la tabla `calidad_datos` y en `data/processed/reporte_calidad.csv`.

| Dimensión DAMA | Regla aplicada |
|---|---|
| 🧱 **Completitud** | `id_cliente` no nulo |
| 🔑 **Unicidad** | Ventas sin duplicados exactos |
| ✔️ **Validez** | `cantidad > 0` |
| 🔄 **Consistencia** | Fechas en un solo formato; ciudades normalizadas |
| 🔗 **Integridad referencial** | Producto y cliente deben existir en sus dimensiones |

Los registros que no cumplen se envían a `data/processed/ventas_rechazadas.csv` con su **motivo de rechazo**, para conservar la trazabilidad.

## 🔐 Integridad y seguridad

- 🔑 Claves primarias y foráneas activas (`PRAGMA foreign_keys = ON`).
- 🛡️ Restricciones `CHECK` (cantidad y precios positivos).
- 👁️ Vista `v_ventas_mensuales` como capa de consumo, sin exponer las tablas base.
- 📝 Registros rechazados auditables.

## ▶️ Cómo ejecutarlo

### Opción 1: ☁️ En Google Colab (sin instalar nada)

1. Abre el notebook `notebooks/pronaca_dwh.ipynb` en [Google Colab](https://colab.research.google.com).
2. Ejecuta las celdas en orden con el botón ▶.

### Opción 2: 💻 En tu computador

```bash
# 1. Clonar el repositorio
git clone https://github.com/davallejo/pronaca-mini-dwh.git
cd pronaca-mini-dwh

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Generar los datos ficticios
python src/generar_datos.py

# 4. Ejecutar el ETL (crea la base de datos y el reporte de calidad)
python src/etl.py
```

### 🔎 Consultar la base de datos

```bash
sqlite3 data/pronaca_dwh.db
```

```sql
SELECT p.categoria, ROUND(SUM(v.total), 2) AS ventas_usd
FROM fact_ventas v
JOIN dim_producto p ON p.id_producto = v.id_producto
GROUP BY p.categoria
ORDER BY ventas_usd DESC;
```

Más consultas en [`sql/02_consultas_analiticas.sql`](sql/02_consultas_analiticas.sql).

## 📊 Dashboard

🔗 **[Ver dashboard en Tableau Public](PEGA_AQUI_TU_ENLACE)**

Incluye:
- 📊 Ventas por categoría
- 📈 Tendencia mensual de ventas

## 🗺️ Competencias demostradas

| Requisito del perfil | Evidencia en el proyecto |
|---|---|
| Administrar repositorios con integridad, seguridad y disponibilidad | PK/FK, `CHECK`, vista de consumo, base versionada en GitHub |
| Diseñar estructuras de datos para análisis | Esquema estrella con hechos y dimensiones |
| Integrar fuentes dispares con calidad | CSV + JSON + CSV → ETL con reglas de limpieza y rechazo |
| Documentación detallada | README y diccionario de datos |
| Metodología DAMA | Reporte de calidad por dimensión |
| SQL | DDL y consultas analíticas |
| Python (Pandas, NumPy, SciPy, scikit-learn) y Notebooks | ETL y notebook en Colab |
| Apache Spark | Agregación con PySpark sobre la tabla de hechos |
| Power BI / Tableau | Dashboard en Tableau Public |

## 🚀 Próximos pasos

- [ ] 🥉🥈🥇 Arquitectura Bronze / Silver / Gold (estilo Databricks)
- [ ] ☁️ Orquestación con Azure Data Factory
- [ ] 📦 Segunda tabla de hechos (inventario)
- [ ] 🔄 Carga incremental y dimensiones SCD Tipo 2
- [ ] 🧪 Pruebas automáticas de calidad con GitHub Actions

## 👤 Autor

**Diego Vallejo** – Ingeniería de Datos 🧑‍💻

[![GitHub](https://img.shields.io/badge/GitHub-davallejo-181717?logo=github&logoColor=white)](https://github.com/davallejo)

---

<div align="center">

⭐ Si te gustó este proyecto, dale una estrella al repositorio.

</div>
