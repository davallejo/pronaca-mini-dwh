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

Demostrar, en un proyecto pequeño y reproducible, las habilidades clave de un **Ingeniero/a de Datos**:

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

> 💸 Todo el stack es **gratuito y sin suscripción** con fines demostrativos.

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

1. Abrir el notebook `notebooks/pronaca_dwh.ipynb` en [Google Colab](https://colab.research.google.com).
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

🔗 **[Ver dashboard en Tableau Public](https://public.tableau.com/views/DashboardEjecutivoPRONACA-Demo/DashboardEjecutivoPRONACA-Demo?:language=es-ES&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**

<img width="1849" height="768" alt="image" src="https://github.com/user-attachments/assets/f5c45368-250a-4ac7-b731-e5036fc816db" />

Incluye:
- 📊 Ventas por categoría
- 📈 Tendencia mensual de ventas

## 📊 Análisis de resultados

![Dashboard Ejecutivo](docs/dashboard.png)

> ℹ️ Los datos son **ficticios** y fueron generados por código. Las conclusiones ilustran el tipo de análisis que habilita el modelo dimensional y no representan la operación real de ninguna empresa.

### 🎯 Resumen ejecutivo

Entre **enero y junio de 2025** se registraron **295 ventas válidas** por **$93,500**, con **18,070 unidades** vendidas y un **ticket promedio de $316.95**. Cada venta movió en promedio **61 unidades** a un precio medio de **$5.17 por unidad**. El negocio se apoya en dos líneas (Embutidos y Pollo, **76%** de las ventas), en cinco productos (**62%**) y en dos ciudades (Guayaquil y Cuenca, **53%**). El **segundo trimestre vendió 45% más que el primero**, pero el ritmo se desacelera desde abril.

### 📌 Indicadores clave

| Indicador | Valor |
|---|---|
| 💰 Ventas totales | **$93,500** |
| 📦 Unidades vendidas | **18,070** |
| 🧾 Nº de ventas | **295** |
| 🎯 Ticket promedio | **$316.95** |

### 🔎 Hallazgos

#### 📈 Tendencia mensual

| Mes | Ventas |
|---|---|
| Enero | $16,110 |
| Febrero | $10,521 |
| Marzo | $11,562 |
| **Abril** | **$21,500** |
| Mayo | $18,276 |
| Junio | $15,531 |

- **Abril es el mejor mes**: supera en **38%** al promedio mensual (~$15.6K) y crece **+86%** frente a marzo.
- **Febrero es el mínimo** y cae **35%** frente a enero.
- **Por trimestre**: el 1.er trimestre suma $38.2K (41%) y el 2.º suma $55.3K (59%).
- **Alerta**: desde abril las ventas bajan mes a mes (**-15%** en mayo y **-15%** en junio). Conviene vigilar si se consolida esta tendencia.

#### 🍗 Categorías

| Categoría | Ventas | Participación |
|---|---|---|
| Embutidos | $35,930 | 38.4% |
| Pollo | $35,127 | 37.6% |
| Cerdo | $22,443 | 24.0% |

- Embutidos y Pollo están **casi empatados** (diferencia de $0.8K).
- **Cerdo es la línea más eficiente por producto**: con solo 2 productos genera unos **$11.2K por producto**, frente a $9.0K en Embutidos y $8.8K en Pollo (4 productos cada una).
- **Embutidos lidera por amplitud de portafolio, no por un producto fuerte**: solo uno de sus productos (Jamón cocido) entra al Top 5.

#### 🏆 Productos

| # | Producto | Categoría | Ventas |
|---|---|---|---|
| 1 | Jamón cocido | Embutidos | $13,387 |
| 2 | Costilla de cerdo | Cerdo | $11,435 |
| 3 | Pechuga de pollo | Pollo | $11,370 |
| 4 | Chuleta de cerdo | Cerdo | $11,008 |
| 5 | Nuggets de pollo | Pollo | $10,633 |

- El **Top 5 concentra el 62% de las ventas** con la mitad del catálogo.
- El Jamón cocido lidera con una ventaja de **$1.9K** sobre el 2.º puesto.
- Del 2.º al 5.º la diferencia es de solo **$0.8K**: la competencia interna es pareja.
- El Top 5 está repartido entre las tres categorías (2 de Cerdo, 2 de Pollo y 1 de Embutidos), lo que reduce la dependencia de una sola línea.

#### 🏪 Canales

| Canal | Ventas | Participación |
|---|---|---|
| Supermercado | $30,335 | 32.4% |
| Distribuidor | $23,553 | 25.2% |
| Tienda de barrio | $20,998 | 22.5% |
| Restaurante | $18,612 | 19.9% |

El **Supermercado** es el canal principal, pero ningún canal supera un tercio de las ventas: la cartera está **diversificada**. La brecha entre el primero y el último canal es de $11.7K.

#### 📍 Ciudades

| Ciudad | Ventas | Participación |
|---|---|---|
| Guayaquil | $26,951 | 28.8% |
| Cuenca | $22,606 | 24.2% |
| Quito | $19,221 | 20.6% |
| Manta | $18,531 | 19.8% |
| Ambato | $6,190 | 6.6% |

- Guayaquil y Cuenca suman **más de la mitad de las ventas (53%)**.
- **Ambato queda muy por debajo del resto**: vende solo un tercio de lo que vende Manta, la ciudad que le sigue. Es la principal oportunidad de crecimiento.

### 💡 Recomendaciones (ilustrativas)

1. 🎯 **Proteger el Top 5**: asegurar abastecimiento e inventario de los productos que generan el 62% de las ventas.
2. 🐖 **Potenciar Cerdo**: es la línea con mayor venta por producto y aporta 2 de los 5 productos líderes; ampliar su portafolio podría elevar su participación.
3. 🌭 **Impulsar productos de Embutidos distintos al Jamón**: la categoría lidera en total, pero depende de un único producto estrella.
4. 📍 **Desarrollar Ambato**: reforzar distribución y presencia comercial en la ciudad de menor venta.
5. 📉 **Investigar la caída posterior a abril**: analizar causas (estacionalidad, promociones, quiebres de stock) antes de que se consolide la tendencia.
6. 🏪 **Mantener el equilibrio de canales**: apoyar al Supermercado sin descuidar Distribuidores y Tiendas de barrio.

### 🖱️ Cómo explorar el dashboard

El tablero incluye filtros por **Ciudad, Canal y Categoría**, y cada gráfico puede usarse como filtro con un clic. Esto permite responder preguntas como "¿cómo se comporta el Pollo en Quito?" o "¿qué productos venden los Distribuidores?".

### ✅ Calidad de los datos (DAMA)

Antes de llegar al dashboard, el ETL validó los datos con reglas de calidad:

| Control | Resultado |
|---|---|
| Ventas recibidas | 302 (2 duplicados exactos eliminados) |
| Ventas rechazadas | **5** (1.7%): cantidad no positiva (2), cliente nulo, producto inexistente y cliente inexistente |
| Ventas válidas cargadas | **295 (98.3%)** |
| Ciudades normalizadas | 3 variantes duplicadas por formato (espacios y mayúsculas) unificadas |

Los registros rechazados se conservan en `ventas_rechazadas.csv` con su motivo, lo que permite **auditar y trazar** cada decisión de limpieza.

### 🧠 Qué demuestra este análisis

- 🔗 **Integración**: 3 fuentes con formatos distintos convertidas en un único modelo consistente.
- 📐 **Modelado**: esquema estrella que permite analizar el mismo hecho por producto, cliente y tiempo.
- ✅ **Calidad**: cifras confiables gracias a reglas DAMA y registros rechazados auditables.
- 📊 **Comunicación**: indicadores y hallazgos orientados a la toma de decisiones.

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
