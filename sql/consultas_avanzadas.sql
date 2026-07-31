-- =========================================================
-- 1. Ranking de vendedores por region
-- Pregunta de negocio: Quien es el mejor vendedor dentro de cada region?
-- =========================================================
WITH ventas_por_vendedor AS (
    SELECT
        v.id_vendedor,
        ve.nombre AS vendedor,
        r.nombre AS region,
        SUM(v.cantidad * p.precio_unitario) AS total_ventas
    FROM ventas v
    JOIN vendedores ve ON ve.id = v.id_vendedor
    JOIN regiones r ON r.id = ve.id_region
    JOIN productos p ON p.id = v.id_producto
    GROUP BY v.id_vendedor, ve.nombre, r.nombre
)
SELECT
    region,
    vendedor,
    total_ventas,
    RANK() OVER (PARTITION BY region ORDER BY total_ventas DESC) AS posicion_en_region
FROM ventas_por_vendedor
ORDER BY region, posicion_en_region;


-- =========================================================
-- 2. Media movil mensual de ventas (por vendedor)
-- Pregunta de negocio: Como evoluciona la tendencia de ventas de cada
-- vendedor mes a mes, suavizando picos puntuales?
-- =========================================================
WITH ventas_mensuales AS (
    SELECT
        v.id_vendedor,
        ve.nombre AS vendedor,
        strftime('%Y-%m', v.fecha) AS mes,
        SUM(v.cantidad * p.precio_unitario) AS total_mes
    FROM ventas v
    JOIN vendedores ve ON ve.id = v.id_vendedor
    JOIN productos p ON p.id = v.id_producto
    GROUP BY v.id_vendedor, ve.nombre, mes
)
SELECT
    vendedor,
    mes,
    total_mes,
    AVG(total_mes) OVER (
        PARTITION BY id_vendedor
        ORDER BY mes
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS media_movil_3_meses
FROM ventas_mensuales
ORDER BY vendedor, mes;


-- =========================================================
-- 3. Participacion porcentual de cada producto en el total de ventas
-- Pregunta de negocio: Que productos concentran mayor parte de los ingresos?
-- =========================================================
WITH ventas_por_producto AS (
    SELECT
        p.nombre AS producto,
        p.categoria,
        SUM(v.cantidad * p.precio_unitario) AS total_producto
    FROM ventas v
    JOIN productos p ON p.id = v.id_producto
    GROUP BY p.nombre, p.categoria
)
SELECT
    producto,
    categoria,
    total_producto,
    ROUND(
        100.0 * total_producto / SUM(total_producto) OVER (),
        2
    ) AS porcentaje_participacion
FROM ventas_por_producto
ORDER BY porcentaje_participacion DESC;


-- =========================================================
-- 4. Crecimiento mes a mes por vendedor
-- Pregunta de negocio: Que vendedores estan creciendo o decreciendo
-- respecto al mes anterior?
-- =========================================================
WITH ventas_mensuales AS (
    SELECT
        v.id_vendedor,
        ve.nombre AS vendedor,
        strftime('%Y-%m', v.fecha) AS mes,
        SUM(v.cantidad * p.precio_unitario) AS total_mes
    FROM ventas v
    JOIN vendedores ve ON ve.id = v.id_vendedor
    JOIN productos p ON p.id = v.id_producto
    GROUP BY v.id_vendedor, ve.nombre, mes
)
SELECT
    vendedor,
    mes,
    total_mes,
    LAG(total_mes) OVER (PARTITION BY id_vendedor ORDER BY mes) AS mes_anterior,
    ROUND(
        100.0 * (total_mes - LAG(total_mes) OVER (PARTITION BY id_vendedor ORDER BY mes))
        / LAG(total_mes) OVER (PARTITION BY id_vendedor ORDER BY mes),
        2
    ) AS crecimiento_porcentual
FROM ventas_mensuales
ORDER BY vendedor, mes;


-- =========================================================
-- 5. Top 2 productos mas vendidos por categoria
-- Pregunta de negocio: Cuales son los productos estrella dentro de
-- cada categoria (Electronica, Hogar, Ropa)?
-- =========================================================
WITH ventas_por_producto AS (
    SELECT
        p.nombre AS producto,
        p.categoria,
        SUM(v.cantidad * p.precio_unitario) AS total_producto
    FROM ventas v
    JOIN productos p ON p.id = v.id_producto
    GROUP BY p.nombre, p.categoria
),
ranking AS (
    SELECT
        producto,
        categoria,
        total_producto,
        ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY total_producto DESC) AS posicion
    FROM ventas_por_producto
)
SELECT categoria, producto, total_producto, posicion
FROM ranking
WHERE posicion <= 2
ORDER BY categoria, posicion;
