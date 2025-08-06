/********************************************************************************
*                                                                               *
*			OPTIMIZACIÓN DE QUERIES SQL				*
*										*
********************************************************************************/

-- ==============================================================================
-- PASO 1: ESTRATEGIA DE INDEXACIÓN
-- ==============================================================================

-- La estrategia de indexación es la mejora de rendimiento más importante.

/*
-- Index on the date column used for filtering ranges.
CREATE INDEX idx_ventas_fecha_venta ON ventas (fecha_venta);

-- Index on the foreign key column used in JOINs.
CREATE INDEX idx_ventas_producto_id ON ventas (producto_id);
CREATE INDEX idx_productos_nombre_producto ON productos (nombre_producto);
*/


-- ==============================================================================
-- Query 1: Ventas por mes
-- ==============================================================================

-- OBSERVACIONES:
-- La query original realiza un escaneo completo de la tabla (Table Scan) si no
-- existe un índice en `fecha_venta`. Esto es ineficiente en tablas grandes.

-- PROPUESTA:
-- 1. Asegurar la existencia de un índice en `fecha_venta`.
-- 2. Usar `BETWEEN` para el rango de fechas, que es más legible y, aunque
-- similar funcionamiento a los dos `AND`.

-- -- Query 1: Optimizada
SELECT
    DATE_TRUNC('month', fecha_venta)::DATE AS mes,
    SUM(monto_total) AS ventas_totales
FROM
    ventas
WHERE
    fecha_venta BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY
    mes
ORDER BY
    mes;


-- ==============================================================================
-- Query 2: Top 10 productos por revenue
-- ==============================================================================

-- OBSERVACIONES:
-- 1. La query original une las tablas `ventas` y `productos` y luego agrupa. Esto
-- implica que el motor de la base de datos maneje un gran conjunto de datos
-- intermedio antes de la agregación.
-- 2. Agrupar por `p.nombre_producto` (string) es menos eficiente que agrupar
-- por `v.producto_id` (integer).

-- PROPUESTA:
-- 1. Usar una Common Table Expression (CTE) para agregar primero los datos en la
-- tabla `ventas` por `producto_id`. Esto reduce el conjunto de datos a un registro
-- por producto *antes* de hacer el JOIN. El JOIN final es más rápido, ya que
-- une un conjunto de datos pequeño (resultado agregado) con la tabla `productos`.

-- -- Query 2: Optimizada
WITH ventas_agregadas_por_producto AS (
    -- Step 1: Aggregate data in the large 'ventas' table first.
    SELECT
        producto_id,
        SUM(cantidad) AS total_vendido,
        SUM(monto_total) AS revenue_total
    FROM
        ventas
    WHERE
        fecha_venta >= '2024-01-01'
    GROUP BY
        producto_id
)
-- Step 2: Join the small, aggregated result with the 'productos' table.
SELECT
    p.nombre_producto,
    vap.total_vendido,
    vap.revenue_total
FROM
    ventas_agregadas_por_producto vap
JOIN
    productos p ON vap.producto_id = p.id
ORDER BY
    vap.revenue_total DESC
LIMIT 10;


-- ==============================================================================
-- Query 3: Rentabilidad por categoría
-- ==============================================================================

-- OBSERVACIONES:
-- Al igual que en la query 2, se realiza un JOIN de todas las filas de ventas
-- del año con la tabla de productos antes de la agregación.
-- Agrupar por `p.categoria` (string) es la única opción aquí, pero podemos
-- optimizar la operación de JOIN.

-- PROPUESTA:
-- 1. Usar una CTE para pre-filtrar la tabla `ventas`. Aunque no podemos pre-agregar
-- como en la query 2 (porque necesitamos la categoría producto para la agrupación),
-- la CTE mejora la legibilidad y puede ayudar al planificador de la BD.
-- 2. La principal ganancia de rendimiento proviene del índice en `fecha_venta` y
-- `producto_id`, que aceleran tanto el `WHERE` como el `JOIN`.

-- -- Query 3: Optimizada
WITH ventas_filtradas AS (
    -- Step 1: Select only the relevant subset of sales data.
    SELECT
        producto_id,
        precio_unitario,
        monto_total
    FROM
        ventas
    WHERE
        fecha_venta BETWEEN '2024-01-01' AND '2024-12-31'
)
-- Step 2: Join the filtered sales with the products table to get the category.
SELECT
    p.categoria,
    COUNT(*) AS productos_vendidos,
    AVG(vf.precio_unitario) AS precio_promedio,
    SUM(vf.monto_total) AS revenue_total
FROM
    ventas_filtradas vf
JOIN
    productos p ON vf.producto_id = p.id
GROUP BY
    p.categoria
ORDER BY
    revenue_total DESC;
