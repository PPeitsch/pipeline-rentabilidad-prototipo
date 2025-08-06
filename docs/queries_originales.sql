/********************************************************************************
*                                                                               *
*                  QUERIES SQL PARA ANÁLISIS DE VENTAS 				*
*                                                                               *
********************************************************************************/

-- ==============================================================================
-- Query 1: Ventas por mes
-- ==============================================================================

SELECT
    DATE_TRUNC('month', fecha_venta) as mes,
    SUM(monto_total) as ventas_totales
FROM ventas
WHERE fecha_venta >= '2024-01-01'
    AND fecha_venta <= '2024-12-31'
GROUP BY mes
ORDER BY mes;

-- ==============================================================================
-- Query 2: Top 10 productos por revenue
-- ==============================================================================

SELECT
    p.nombre_producto,
    SUM(v.cantidad) as total_vendido,
    SUM(v.monto_total) as revenue_total
FROM ventas v
JOIN productos p ON v.producto_id = p.id
WHERE v.fecha_venta >= '2024-01-01'
GROUP BY p.nombre_producto
ORDER BY revenue_total DESC
LIMIT 10;

-- ==============================================================================
-- Query 3: Rentabilidad por categoría
-- ==============================================================================

SELECT
    p.categoria,
    COUNT(*) as productos_vendidos,
    AVG(v.precio_unitario) as precio_promedio,
    SUM(v.monto_total) as revenue_total
FROM ventas v
JOIN productos p ON v.producto_id = p.id
WHERE v.fecha_venta >= '2024-01-01'
    AND v.fecha_venta <= '2024-12-31'
GROUP BY p.categoria
ORDER BY revenue_total DESC;
