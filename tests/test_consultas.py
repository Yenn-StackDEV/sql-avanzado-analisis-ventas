import pytest

from src.db import get_connection, inicializar_base_datos
from src.consultas import (
    RANKING_VENDEDORES_POR_REGION,
    MEDIA_MOVIL_MENSUAL,
    PARTICIPACION_POR_PRODUCTO,
    TOP_2_PRODUCTOS_POR_CATEGORIA,
    ejecutar_consulta,
)


@pytest.fixture
def conexion():
    conexion = get_connection()
    inicializar_base_datos(conexion)
    yield conexion
    conexion.close()


def test_ranking_tiene_una_fila_por_vendedor_y_region(conexion):
    columnas, filas = ejecutar_consulta(conexion, RANKING_VENDEDORES_POR_REGION)
    assert "posicion_en_region" in columnas
    # Hay 3 regiones con 1 vendedor cada una en los datos de ejemplo
    assert len(filas) == 3


def test_media_movil_devuelve_filas_por_mes(conexion):
    columnas, filas = ejecutar_consulta(conexion, MEDIA_MOVIL_MENSUAL)
    assert "media_movil_3_meses" in columnas
    # 3 vendedores x 6 meses = 18 filas
    assert len(filas) == 18


def test_participacion_suma_aproximadamente_100(conexion):
    columnas, filas = ejecutar_consulta(conexion, PARTICIPACION_POR_PRODUCTO)
    indice_porcentaje = columnas.index("porcentaje_participacion")
    total = sum(fila[indice_porcentaje] for fila in filas)
    assert 99.0 <= total <= 101.0


def test_top_2_por_categoria_no_excede_dos_filas(conexion):
    columnas, filas = ejecutar_consulta(conexion, TOP_2_PRODUCTOS_POR_CATEGORIA)
    indice_categoria = columnas.index("categoria")
    conteo_por_categoria = {}
    for fila in filas:
        categoria = fila[indice_categoria]
        conteo_por_categoria[categoria] = conteo_por_categoria.get(categoria, 0) + 1

    for categoria, conteo in conteo_por_categoria.items():
        assert conteo <= 2, f"La categoria {categoria} tiene mas de 2 productos"
