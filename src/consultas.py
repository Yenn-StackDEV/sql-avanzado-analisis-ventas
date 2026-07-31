import sqlite3

RANKING_VENDEDORES_POR_REGION = """
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
"""

MEDIA_MOVIL_MENSUAL = """
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
"""

PARTICIPACION_POR_PRODUCTO = """
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
    ROUND(100.0 * total_producto / SUM(total_producto) OVER (), 2) AS porcentaje_participacion
FROM ventas_por_producto
ORDER BY porcentaje_participacion DESC;
"""

CRECIMIENTO_MES_A_MES = """
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
"""

TOP_2_PRODUCTOS_POR_CATEGORIA = """
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
"""


def ejecutar_consulta(conexion: sqlite3.Connection, consulta_sql: str):
    """Ejecuta una consulta y devuelve los nombres de columnas y las filas."""
    cursor = conexion.execute(consulta_sql)
    columnas = [descripcion[0] for descripcion in cursor.description]
    filas = cursor.fetchall()
    return columnas, filas
