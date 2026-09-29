-- 1) Ventas por categoría
SELECT p.categoria, ROUND(SUM(v.total),2) AS ventas_usd
FROM fact_ventas v JOIN dim_producto p ON p.id_producto = v.id_producto
GROUP BY p.categoria ORDER BY ventas_usd DESC;

-- 2) Top 5 productos
SELECT p.nombre, SUM(v.cantidad) AS unidades, ROUND(SUM(v.total),2) AS ventas_usd
FROM fact_ventas v JOIN dim_producto p ON p.id_producto = v.id_producto
GROUP BY p.nombre ORDER BY ventas_usd DESC LIMIT 5;

-- 3) Ventas por canal y ciudad
SELECT c.canal, c.ciudad, ROUND(SUM(v.total),2) AS ventas_usd
FROM fact_ventas v JOIN dim_cliente c ON c.id_cliente = v.id_cliente
GROUP BY c.canal, c.ciudad ORDER BY ventas_usd DESC;

-- 4) Tendencia mensual (usa la vista)
SELECT anio, mes, ROUND(SUM(ventas_usd),2) AS ventas_usd
FROM v_ventas_mensuales GROUP BY anio, mes ORDER BY anio, mes;
