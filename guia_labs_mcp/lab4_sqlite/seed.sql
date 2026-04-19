-- ============================================================
-- seed.sql — Banco de dados de exemplo para o Lab 4 MCP SQLite
-- Loja de produtos de tecnologia (dados fictícios)
-- ============================================================

-- Categorias de produtos
CREATE TABLE IF NOT EXISTS categorias (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    nome      TEXT NOT NULL
);

-- Produtos
CREATE TABLE IF NOT EXISTS produtos (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT NOT NULL,
    categoria_id INTEGER NOT NULL,
    preco        REAL NOT NULL,
    estoque      INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    nome  TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    cidade TEXT NOT NULL
);

-- Pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id  INTEGER NOT NULL,
    data_pedido TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'concluido',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Itens de cada pedido
CREATE TABLE IF NOT EXISTS itens_pedido (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id   INTEGER NOT NULL,
    produto_id  INTEGER NOT NULL,
    quantidade  INTEGER NOT NULL,
    preco_unit  REAL NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- ============================================================
-- Dados de exemplo
-- ============================================================

INSERT INTO categorias (nome) VALUES
    ('Notebooks'),
    ('Periféricos'),
    ('Monitores'),
    ('Armazenamento'),
    ('Componentes');

INSERT INTO produtos (nome, categoria_id, preco, estoque) VALUES
    ('Notebook Pro 15"',          1, 4299.90, 12),
    ('Notebook Ultra Slim',       1, 5899.00,  8),
    ('Notebook Básico 14"',       1, 2199.90, 20),
    ('Mouse Wireless Ergonômico', 2,  189.90, 45),
    ('Teclado Compacto USB',      2,   99.90, 30),
    ('Headset Gamer 7.1',         2,  349.90,  7),
    ('Webcam Full HD',            2,  279.90, 15),
    ('Monitor 24" FHD',           3,  899.00, 18),
    ('Monitor 27" QHD',           3, 1599.00,  9),
    ('Monitor Ultrawide 34"',     3, 2799.00,  4),
    ('SSD 500GB NVMe',            4,  299.90, 35),
    ('SSD 1TB NVMe',              4,  499.90, 28),
    ('HD Externo 2TB',            4,  389.90, 22),
    ('Memória RAM 16GB DDR5',     5,  389.90, 14),
    ('Placa de Vídeo RTX 4060',   5, 2199.00,  6),
    ('Processador i7-13ª Gen',    5, 1799.90,  3);

INSERT INTO clientes (nome, email, cidade) VALUES
    ('Ana Costa',      'ana.costa@email.com',      'São Paulo'),
    ('Bruno Ferreira', 'bruno.ferreira@email.com', 'Rio de Janeiro'),
    ('Carla Mendes',   'carla.mendes@email.com',   'Belo Horizonte'),
    ('Diego Alves',    'diego.alves@email.com',    'Curitiba'),
    ('Elena Souza',    'elena.souza@email.com',    'Porto Alegre'),
    ('Felipe Lima',    'felipe.lima@email.com',    'Brasília'),
    ('Gabriela Nunes', 'gabriela.nunes@email.com', 'Salvador'),
    ('Henrique Rocha', 'henrique.rocha@email.com', 'Recife');

INSERT INTO pedidos (cliente_id, data_pedido, status) VALUES
    (1, '2024-10-05', 'concluido'),
    (2, '2024-10-12', 'concluido'),
    (3, '2024-11-03', 'concluido'),
    (1, '2024-11-18', 'concluido'),
    (4, '2024-11-22', 'concluido'),
    (5, '2024-12-01', 'concluido'),
    (2, '2024-12-10', 'concluido'),
    (6, '2024-12-15', 'concluido'),
    (3, '2025-01-08', 'concluido'),
    (7, '2025-01-14', 'concluido'),
    (8, '2025-01-20', 'concluido'),
    (1, '2025-02-03', 'concluido'),
    (4, '2025-02-17', 'concluido'),
    (5, '2025-03-02', 'concluido'),
    (6, '2025-03-11', 'concluido');

INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unit) VALUES
    -- Pedido 1: Ana - Notebook + Mouse
    (1, 1,  1, 4299.90),
    (1, 4,  1,  189.90),
    -- Pedido 2: Bruno - SSD + RAM
    (2, 11, 1,  299.90),
    (2, 14, 2,  389.90),
    -- Pedido 3: Carla - Monitor FHD + Teclado
    (3, 8,  1,  899.00),
    (3, 5,  1,   99.90),
    -- Pedido 4: Ana - SSD 1TB
    (4, 12, 2,  499.90),
    -- Pedido 5: Diego - Notebook Ultra Slim
    (5, 2,  1, 5899.00),
    -- Pedido 6: Elena - Headset + Webcam
    (6, 6,  1,  349.90),
    (6, 7,  1,  279.90),
    -- Pedido 7: Bruno - Monitor QHD
    (7, 9,  1, 1599.00),
    -- Pedido 8: Felipe - Placa de Vídeo
    (8, 15, 1, 2199.00),
    -- Pedido 9: Carla - HD Externo + Mouse
    (9, 13, 1,  389.90),
    (9, 4,  2,  189.90),
    -- Pedido 10: Gabriela - Notebook Básico
    (10, 3, 1, 2199.90),
    -- Pedido 11: Henrique - SSD + Teclado + Mouse
    (11, 11, 1,  299.90),
    (11, 5,  1,   99.90),
    (11, 4,  1,  189.90),
    -- Pedido 12: Ana - Monitor Ultrawide
    (12, 10, 1, 2799.00),
    -- Pedido 13: Diego - Processador + RAM
    (13, 16, 1, 1799.90),
    (13, 14, 2,  389.90),
    -- Pedido 14: Elena - Notebook Pro + SSD 1TB
    (14, 1,  1, 4299.90),
    (14, 12, 1,  499.90),
    -- Pedido 15: Felipe - Headset + Webcam + Mouse
    (15, 6,  1,  349.90),
    (15, 7,  1,  279.90),
    (15, 4,  1,  189.90);
