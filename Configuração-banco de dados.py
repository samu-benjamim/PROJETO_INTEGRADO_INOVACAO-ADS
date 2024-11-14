import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('estoque.db')

# Criar um cursor
cur = conn.cursor()

# Criar tabelas
cur.execute('''
CREATE TABLE IF NOT EXISTS Produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    localizacao TEXT NOT NULL
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    tipo TEXT NOT NULL,  -- 'entrada' ou 'saida'
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES Produtos(id)
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    senha TEXT NOT NULL,
    role TEXT NOT NULL  -- 'estoquista', 'usuario', 'gerente'
)
''')

# Commitar mudanças e fechar conexão
conn.commit()
conn.close()
