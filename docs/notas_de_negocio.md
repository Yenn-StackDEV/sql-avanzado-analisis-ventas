# Notas de negocio: razonamiento detras de cada consulta

Este documento explica, en lenguaje de negocio, por que se eligio cada
consulta y por que una funcion de ventana resuelve mejor el problema que
un simple GROUP BY.

## 1. Ranking de vendedores por region

**Pregunta:** Quien es el mejor vendedor dentro de cada region?

Un GROUP BY normal permite sumar las ventas por vendedor, pero no permite
comparar directamente contra los demas vendedores de su misma region sin
una segunda consulta o un calculo manual. Usar RANK() con PARTITION BY
region resuelve esto en una sola pasada, asignando una posicion relativa
dentro de cada grupo. Esto es util para decidir bonificaciones o
reconocimientos por region, en lugar de comparar vendedores de regiones
distintas que pueden tener mercados de tamanos diferentes.

## 2. Media movil mensual por vendedor

**Pregunta:** Como evoluciona la tendencia de ventas de cada vendedor
mes a mes, sin dejarse enganar por picos puntuales?

Mirar el total de un solo mes puede llevar a conclusiones erradas: un mes
excepcionalmente bueno o malo puede deberse a un evento aislado (una
promocion, una temporada) y no a un cambio real de desempeno. La media
movil de 3 meses, calculada con AVG() OVER una ventana de filas, suaviza
esas variaciones y muestra la tendencia real, algo que un GROUP BY simple
no puede ofrecer porque no tiene nocion de "orden" ni de "ventana deslizante".

## 3. Participacion porcentual por producto

**Pregunta:** Que productos concentran mayor parte de los ingresos?

Calcular el porcentaje que representa cada producto sobre el total general
requiere conocer, al mismo tiempo, el total individual y el total global.
Con SQL tradicional esto exigiria una subconsulta aparte para el total
general. Usando SUM() OVER () sin PARTITION BY, se obtiene el total global
en la misma fila que el detalle de cada producto, simplificando la consulta
y evitando uniones adicionales.

## 4. Crecimiento mes a mes por vendedor

**Pregunta:** Que vendedores estan creciendo o decreciendo respecto al
mes anterior?

Comparar un mes contra el mes inmediatamente anterior, por vendedor,
requiere "mirar hacia atras" en una secuencia ordenada. LAG() OVER
(PARTITION BY vendedor ORDER BY mes) trae el valor del registro anterior
en la misma fila, permitiendo calcular el crecimiento porcentual
directamente. Esto identifica alertas tempranas (vendedores en caida) y
buenas practicas a replicar (vendedores en crecimiento sostenido).

## 5. Top 2 productos por categoria

**Pregunta:** Cuales son los productos estrella dentro de cada categoria?

Cuando se necesita el "top N" dentro de cada grupo (no el top N global),
ROW_NUMBER() combinado con PARTITION BY categoria asigna una posicion
independiente por categoria, permitiendo filtrar facilmente los primeros
2 lugares de cada una. Esto es clave para decisiones de inventario y
marketing: los productos estrella de Electronica no compiten por espacio
en el analisis con los de Ropa u Hogar.
