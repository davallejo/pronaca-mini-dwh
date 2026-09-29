-- Modelo dimensional (esquema estrella) - Ventas PRONACA (datos ficticios)
PRAGMA foreign_keys = ON;

DROP VIEW  IF EXISTS v_ventas_mensuales;
DROP TABLE IF EXISTS fact_ventas;
DROP TABLE IF EXISTS dim_producto;
DROP TABLE IF EXISTS dim_cliente;
DROP TABLE IF EXISTS dim_fecha;
DROP TABLE IF EXISTS calidad_datos;

CREATE TABLE dim_producto (
    id_producto      INTEGER PRIMARY KEY,
    nombre           TEXT NOT NULL,
    categoria        TEXT NOT NULL,
    unidad           TEXT NOT NULL,
    precio_lista     REAL NOT NULL CHECK (precio_lista > 0)
);

CREATE TABLE dim_cliente (
    id_cliente       INTEGER PRIMARY KEY,
    nombre           TEXT NOT NULL,
    canal            TEXT NOT NULL,
    ciudad           TEXT NOT NULL
);

CREATE TABLE dim_fecha (
    id_fecha         INTEGER PRIMARY KEY,   -- formato AAAAMMDD
    fecha            TEXT NOT NULL,
    anio             INTEGER NOT NULL,
    mes              INTEGER NOT NULL,
    nombre_mes       TEXT NOT NULL,
    trimestre        INTEGER NOT NULL,
    dia_semana       TEXT NOT NULL
);

CREATE TABLE fact_ventas (
    id_venta         INTEGER PRIMARY KEY,
    id_fecha         INTEGER NOT NULL,
    id_cliente       INTEGER NOT NULL,
    id_producto      INTEGER NOT NULL,
    cantidad         INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario  REAL    NOT NULL CHECK (precio_unitario > 0),
    total            REAL    NOT NULL,
    FOREIGN KEY (id_fecha)    REFERENCES dim_fecha(id_fecha),
    FOREIGN KEY (id_cliente)  REFERENCES dim_cliente(id_cliente),
    FOREIGN KEY (id_producto) REFERENCES dim_producto(id_producto)
);

CREATE INDEX idx_fact_fecha    ON fact_ventas(id_fecha);
CREATE INDEX idx_fact_cliente  ON fact_ventas(id_cliente);
CREATE INDEX idx_fact_producto ON fact_ventas(id_producto);

CREATE TABLE calidad_datos (
    dimension_dama   TEXT NOT NULL,
    regla            TEXT NOT NULL,
    registros_total  INTEGER NOT NULL,
    registros_error  INTEGER NOT NULL,
    porcentaje_ok    REAL NOT NULL
);

-- Vista de consumo (capa de seguridad: se expone la vista, no las tablas)
CREATE VIEW v_ventas_mensuales AS
SELECT f.anio, f.mes, f.nombre_mes, p.categoria,
       SUM(v.total)    AS ventas_usd,
       SUM(v.cantidad) AS unidades
FROM fact_ventas v
JOIN dim_fecha    f ON f.id_fecha    = v.id_fecha
JOIN dim_producto p ON p.id_producto = v.id_producto
GROUP BY f.anio, f.mes, f.nombre_mes, p.categoria;
