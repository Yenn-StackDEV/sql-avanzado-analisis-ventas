-- Datos ficticios para pruebas y demostración del proyecto

INSERT INTO regiones (id, nombre) VALUES
    (1, 'Norte'),
    (2, 'Sur'),
    (3, 'Centro');

INSERT INTO vendedores (id, nombre, id_region) VALUES
    (1, 'Ana Gómez', 1),
    (2, 'Carlos Ruiz', 1),
    (3, 'Beatriz León', 2),
    (4, 'Diego Salazar', 2),
    (5, 'Elena Vargas', 3),
    (6, 'Felipe Ortiz', 3);

INSERT INTO productos (id, nombre, categoria, precio_unitario) VALUES
    (1, 'Audifonos Bluetooth', 'Electronica', 89000),
    (2, 'Cargador Rapido USB-C', 'Electronica', 45000),
    (3, 'Parlante Portatil', 'Electronica', 120000),
    (4, 'Smartwatch Basico', 'Electronica', 210000),
    (5, 'Juego de Ollas', 'Hogar', 180000),
    (6, 'Lampara LED de Escritorio', 'Hogar', 65000),
    (7, 'Organizador Multiuso', 'Hogar', 38000),
    (8, 'Camiseta Basica', 'Ropa', 42000),
    (9, 'Chaqueta Impermeable', 'Ropa', 150000),
    (10, 'Gorra Deportiva', 'Ropa', 35000);

INSERT INTO ventas (id, fecha, id_vendedor, id_producto, cantidad) VALUES
    (1, '2024-01-15', 1, 1, 12),
    (2, '2024-01-20', 1, 4, 5),
    (3, '2024-02-10', 1, 1, 15),
    (4, '2024-02-25', 1, 3, 8),
    (5, '2024-03-05', 1, 4, 7),
    (6, '2024-03-22', 1, 2, 20),
    (7, '2024-04-08', 1, 1, 18),
    (8, '2024-04-27', 1, 4, 9),
    (9, '2024-05-14', 1, 3, 11),
    (10, '2024-05-30', 1, 2, 25),
    (11, '2024-06-11', 1, 1, 22),
    (12, '2024-06-28', 1, 4, 13),
    (13, '2024-01-12', 2, 5, 6),
    (14, '2024-01-29', 2, 7, 10),
    (15, '2024-02-14', 2, 6, 8),
    (16, '2024-02-28', 2, 5, 9),
    (17, '2024-03-10', 2, 7, 14),
    (18, '2024-03-26', 2, 6, 6),
    (19, '2024-04-09', 2, 5, 11),
    (20, '2024-04-24', 2, 7, 16),
    (21, '2024-05-13', 2, 6, 9),
    (22, '2024-05-28', 2, 5, 13),
    (23, '2024-06-10', 2, 7, 19),
    (24, '2024-06-25', 2, 6, 10),
    (25, '2024-01-18', 3, 8, 30),
    (26, '2024-02-05', 3, 9, 4),
    (27, '2024-02-22', 3, 10, 25),
    (28, '2024-03-14', 3, 8, 28),
    (29, '2024-03-29', 3, 9, 6),
    (30, '2024-04-15', 3, 10, 22),
    (31, '2024-04-30', 3, 8, 26),
    (32, '2024-05-16', 3, 9, 8),
    (33, '2024-05-31', 3, 10, 20),
    (34, '2024-06-14', 3, 8, 24),
    (35, '2024-06-29', 3, 9, 10),
    (36, '2024-06-30', 3, 10, 18);
