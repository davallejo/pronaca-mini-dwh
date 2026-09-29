# 📘 Diccionario de datos

> Datos ficticios con fines demostrativos.

## dim_producto
| Columna | Tipo | Descripción |
|---|---|---|
| id_producto | INTEGER (PK) | Identificador del producto |
| nombre | TEXT | Nombre comercial |
| categoria | TEXT | Pollo, Cerdo o Embutidos |
| unidad | TEXT | kg, caja o paquete |
| precio_lista | REAL | Precio de lista en USD (> 0) |

## dim_cliente
| Columna | Tipo | Descripción |
|---|---|---|
| id_cliente | INTEGER (PK) | Identificador del cliente |
| nombre | TEXT | Nombre del cliente |
| canal | TEXT | Supermercado, Tienda de barrio, Restaurante o Distribuidor |
| ciudad | TEXT | Ciudad normalizada (Title Case, sin espacios extra) |

## dim_fecha
| Columna | Tipo | Descripción |
|---|---|---|
| id_fecha | INTEGER (PK) | Formato AAAAMMDD |
| fecha | TEXT | AAAA-MM-DD |
| anio, mes, trimestre | INTEGER | Atributos de calendario |
| nombre_mes, dia_semana | TEXT | Nombres en español |

## fact_ventas (grano: una línea de venta)
| Columna | Tipo | Descripción |
|---|---|---|
| id_venta | INTEGER (PK) | Identificador de la venta |
| id_fecha | INTEGER (FK) | -> dim_fecha |
| id_cliente | INTEGER (FK) | -> dim_cliente |
| id_producto | INTEGER (FK) | -> dim_producto |
| cantidad | INTEGER | Unidades vendidas (> 0) |
| precio_unitario | REAL | Precio aplicado en USD |
| total | REAL | cantidad × precio_unitario |

## calidad_datos
Resultado de las reglas de calidad por dimensión DAMA: completitud, unicidad, validez, consistencia e integridad referencial.

## Reglas de rechazo (ventas)
Se envían a `ventas_rechazadas.csv` con su motivo: cliente nulo, cantidad no positiva, producto inexistente, cliente inexistente.
