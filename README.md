# SQL Avanzado: Análisis de Ventas por Vendedor y Región

Proyecto de portafolio enfocado en consultas SQL avanzadas: funciones de ventana (window functions), CTEs (common table expressions) y particiones, aplicadas sobre un dataset ficticio de ventas por vendedor y región. El objetivo no es solo mostrar sintaxis avanzada, sino explicar el razonamiento de negocio detrás de cada consulta, tal como se justificaría en una entrevista o en un informe real.

Todos los datos usados en este proyecto son **ficticios**, generados únicamente con fines demostrativos.

## Problema

Los equipos comerciales necesitan responder preguntas que van más allá de un simple total de ventas: ¿qué vendedor lidera en cada región?, ¿cómo evoluciona la tendencia mes a mes?, ¿qué productos concentran la mayor parte de las ventas dentro de su categoría? Responder esto con SQL básico (solo GROUP BY) es limitado; se necesitan funciones de ventana para comparar filas entre sí sin perder el detalle de cada una.

## Solución

Este proyecto modela un esquema simple de ventas (regiones, vendedores, productos y ventas) y resuelve 5 preguntas de negocio con consultas SQL avanzadas:

1. **Ranking de vendedores por región**: usa `RANK() OVER (PARTITION BY región ORDER BY total DESC)` para identificar al mejor vendedor de cada región sin perder la comparación dentro de su grupo.
2. **Media móvil de ventas mensuales**: usa `AVG() OVER (ORDER BY mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` para suavizar la variabilidad mes a mes y detectar tendencias reales.
3. **Participación porcentual de cada producto**: usa una CTE junto con `SUM() OVER ()` para calcular qué porcentaje del total representa cada producto, útil para decisiones de inventario y marketing.
4. **Crecimiento mes a mes por vendedor**: usa `LAG()` para comparar cada mes con el anterior y calcular el crecimiento porcentual, identificando vendedores en alza o en caída.
5. **Top 2 productos por categoría**: combina una CTE con `ROW_NUMBER() OVER (PARTITION BY categoría ORDER BY total DESC)` para responder "¿cuáles son los productos estrella de cada categoría?", algo que un simple `GROUP BY` no puede resolver directamente.

## Tecnologías

- SQL (SQLite)
- Python 3.10+ (orquestación y pruebas, usando la librería estándar `sqlite3`)
- pytest (pruebas unitarias)

## Estructura del repositorio

```
sql-avanzado-analisis-ventas/
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
├── sql/
│   ├── schema.sql
│   ├── seed.sql
│   └── consultas_avanzadas.sql
├── src/
│   ├── __init__.py
│   ├── db.py
│   └── consultas.py
├── docs/
│   └── notas_de_negocio.md
└── tests/
    └── test_consultas.py
```

## Cómo ejecutarlo

1. Instalar dependencias (solo se usa para las pruebas, SQLite ya viene incluido en Python):

```bash
pip install -r requirements.txt
```

2. Ejecutar el script principal:

```bash
python main.py
```

3. El script crea una base de datos SQLite en memoria, carga el esquema y los datos ficticios, y ejecuta las 5 consultas avanzadas, imprimiendo los resultados en consola.

4. Para correr las pruebas:

```bash
pytest
```

## Resultado esperado

Cinco reportes impresos en consola: ranking de vendedores por región, media móvil de ventas mensuales, participación porcentual por producto, crecimiento mes a mes por vendedor y el top 2 de productos por categoría.

## Razonamiento de negocio

Cada consulta está documentada con más detalle, incluyendo por qué se eligió esa función de ventana en particular y qué decisión de negocio ayuda a tomar, en [`docs/notas_de_negocio.md`](docs/notas_de_negocio.md).
