from src.db import get_connection, inicializar_base_datos
from src.consultas import (
    RANKING_VENDEDORES_POR_REGION,
    MEDIA_MOVIL_MENSUAL,
    PARTICIPACION_POR_PRODUCTO,
    CRECIMIENTO_MES_A_MES,
    TOP_2_PRODUCTOS_POR_CATEGORIA,
    ejecutar_consulta,
)

CONSULTAS = [
    ("Ranking de vendedores por region", RANKING_VENDEDORES_POR_REGION),
    ("Media movil mensual por vendedor", MEDIA_MOVIL_MENSUAL),
    ("Participacion porcentual por producto", PARTICIPACION_POR_PRODUCTO),
    ("Crecimiento mes a mes por vendedor", CRECIMIENTO_MES_A_MES),
    ("Top 2 productos por categoria", TOP_2_PRODUCTOS_POR_CATEGORIA),
]


def imprimir_resultado(titulo: str, columnas, filas) -> None:
    print("=" * 70)
    print(titulo)
    print("=" * 70)
    print(" | ".join(columnas))
    for fila in filas:
        print(" | ".join(str(valor) for valor in fila))
    print()


def main() -> None:
    conexion = get_connection()
    inicializar_base_datos(conexion)

    for titulo, consulta_sql in CONSULTAS:
        columnas, filas = ejecutar_consulta(conexion, consulta_sql)
        imprimir_resultado(titulo, columnas, filas)

    conexion.close()


if __name__ == "__main__":
    main()
