import sqlite3

# Lista de produtos
produtos = [
    {"nome": "Monitor 24''", "categoria": "Eletrônicos", "quantidade": 15, "preco": 700.00, "localizacao": "A1"},
    {"nome": "Teclado Mecânico", "categoria": "Acessórios", "quantidade": 25, "preco": 250.00, "localizacao": "B2"},
    {"nome": "Cadeira Gamer", "categoria": "Mobiliário", "quantidade": 10, "preco": 1200.00, "localizacao": "C3"},
    {"nome": "Smartphone X", "categoria": "Eletrônicos", "quantidade": 30, "preco": 2500.00, "localizacao": "A2"},
    {"nome": "Cabo HDMI", "categoria": "Acessórios", "quantidade": 100, "preco": 35.00, "localizacao": "B3"},
    {"nome": "Notebook Pro 15''", "categoria": "Computadores", "quantidade": 8, "preco": 4500.00, "localizacao": "A4"},
    {"nome": "Mouse Sem Fio", "categoria": "Acessórios", "quantidade": 50, "preco": 120.00, "localizacao": "B1"},
    {"nome": "Impressora Laser", "categoria": "Eletrônicos", "quantidade": 5, "preco": 850.00, "localizacao": "C1"},
    {"nome": "SSD 1TB", "categoria": "Armazenamento", "quantidade": 40, "preco": 450.00, "localizacao": "A3"},
    {"nome": "HD Externo 2TB", "categoria": "Armazenamento", "quantidade": 25, "preco": 380.00, "localizacao": "A5"},
    {"nome": "Webcam HD", "categoria": "Acessórios", "quantidade": 20, "preco": 200.00, "localizacao": "B4"},
    {"nome": "Fone de Ouvido Gamer", "categoria": "Acessórios", "quantidade": 35, "preco": 150.00, "localizacao": "B5"},
    {"nome": "Mesa de Escritório", "categoria": "Mobiliário", "quantidade": 12, "preco": 800.00, "localizacao": "C2"},
    {"nome": "Caixa de Som Bluetooth", "categoria": "Eletrônicos", "quantidade": 18, "preco": 300.00, "localizacao": "A6"},
    {"nome": "Router WiFi 6", "categoria": "Eletrônicos", "quantidade": 22, "preco": 500.00, "localizacao": "A7"},
    {"nome": "Switch Ethernet", "categoria": "Eletrônicos", "quantidade": 30, "preco": 400.00, "localizacao": "A8"},
    {"nome": "Hub USB 4 Portas", "categoria": "Acessórios", "quantidade": 50, "preco": 90.00, "localizacao": "B6"},
    {"nome": "Lâmpada LED", "categoria": "Iluminação", "quantidade": 100, "preco": 20.00, "localizacao": "D1"},
    {"nome": "Ar Condicionado Split", "categoria": "Eletrônicos", "quantidade": 6, "preco": 2500.00, "localizacao": "D2"},
    {"nome": "Geladeira Compacta", "categoria": "Eletrodomésticos", "quantidade": 4, "preco": 1200.00, "localizacao": "D3"},
    {"nome": "Micro-ondas", "categoria": "Eletrodomésticos", "quantidade": 7, "preco": 600.00, "localizacao": "D4"},
]

def inserir_produtos(produtos):
    try:
        conn = sqlite3.connect("estoque.db")
        cur = conn.cursor()
        for produto in produtos:
            cur.execute("""
                INSERT INTO Produtos (nome, categoria, quantidade, preco, localizacao)
                VALUES (?, ?, ?, ?, ?)
            """, (produto["nome"], produto["categoria"], produto["quantidade"], produto["preco"], produto["localizacao"]))
        conn.commit()
        print("Produtos inseridos com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inserir produtos: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    inserir_produtos(produtos)