import sqlite3 

username = input("Digite o nome de usuário: ")
senha = input("Digite a senha: ")
role = input("Digite a função (estoquista/usuario/gerente): ")

conn = sqlite3.connect("estoque.db")
cur = conn.cursor()
cur.execute("INSERT INTO Usuarios (username, senha, role) VALUES (?, ?, ?)", (username, senha, role))
conn.commit()
conn.close()

print("Usuário registrado com sucesso!")