import sqlite3  # Importa o módulo para interação com banco de dados SQLite.
from datetime import datetime  # Importa a classe datetime para manipulação de datas e horas.
import matplotlib.pyplot as plt  # Importa a biblioteca matplotlib para geração de gráficos.
import seaborn as sns  # Importa a biblioteca seaborn para gráficos estatísticos.
import getpass  # Importa o módulo para esconder a senha ao ser digitada no console.

# Função de login, onde o usuário digita o nome e a senha para acessar o sistema
def login():
    while True:
        username = input("Digite seu nome de usuário: ")  # Solicita o nome de usuário.
        senha = getpass.getpass("Digite sua senha: ")  # Solicita a senha de forma oculta.

        try:
            conn = sqlite3.connect("estoque.db")  # Conecta ao banco de dados SQLite.
            cur = conn.cursor()  # Cria um cursor para realizar operações no banco de dados.
            cur.execute("SELECT role FROM Usuarios WHERE username = ? AND senha = ?", (username, senha))  # Verifica a existência do usuário e senha.
            resultado = cur.fetchone()  # Obtém o resultado da consulta.
        except sqlite3.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")  # Exibe mensagem de erro caso haja falha na conexão.
            return None
        finally:
            conn.close()  # Fecha a conexão com o banco de dados.

        # Se as credenciais forem corretas, exibe uma mensagem e retorna a função do usuário.
        if resultado:
            print(f"Bem-vindo(a), {username}! Função: {resultado[0]}")
            return resultado[0] 
        else:
            print("Usuário ou senha incorretos.")  # Mensagem de erro se a senha ou o nome de usuário estiverem incorretos.

# Função para registrar um novo usuário no sistema
def registrar_usuario():
    username = input("Digite o nome de usuário: ")  # Solicita o nome de usuário.
    senha = getpass.getpass("Digite a senha: ")  # Solicita a senha do novo usuário de forma oculta.
    role = input("Digite a função (estoquista/usuario/gerente): ")  # Solicita a função do novo usuário.

    try:
        conn = sqlite3.connect("estoque.db")  # Conecta ao banco de dados SQLite.
        cur = conn.cursor()  # Cria um cursor para realizar operações no banco de dados.
        cur.execute("INSERT INTO Usuarios (username, senha, role) VALUES (?, ?, ?)", (username, senha, role))  # Insere o novo usuário na tabela Usuarios.
        conn.commit()  # Confirma as alterações no banco de dados.
        print("Usuário registrado com sucesso!")  # Mensagem de sucesso.
    except sqlite3.Error as e:
        print(f"Erro ao registrar usuário: {e}")  # Exibe mensagem de erro caso algo dê errado.
    finally:
        conn.close()  # Fecha a conexão com o banco de dados.

# Função para trocar de usuário
def trocar_usuario():
    print("\nSaindo da conta atual...")  # Exibe mensagem de logout.
    return login()  # Chama a função de login para um novo usuário.

# Função para visualizar todos os produtos no estoque
def visualizar_produtos():
    try:
        conn = sqlite3.connect("estoque.db")  # Conecta ao banco de dados SQLite.
        cur = conn.cursor()  # Cria um cursor para realizar operações no banco de dados.
        cur.execute("SELECT * FROM Produtos")  # Consulta todos os produtos na tabela Produtos.
        produtos = cur.fetchall()  # Obtém todos os produtos.
    except sqlite3.Error as e:
        print(f"Erro ao acessar produtos: {e}")  # Exibe mensagem de erro se houver problema na consulta.
        return
    finally:
        conn.close()  # Fecha a conexão com o banco de dados.
    
    # Exibe os produtos, se encontrados.
    if produtos:
        print("\nProdutos no estoque:")
        print(f"{'ID':<5} {'Nome':<30} {'Categoria':<20}{'Quantidade':<10} {'Preço':<10} {'Localização':<15}")
        print("-"*90)
        for produto in produtos:  # Exibe cada produto de forma tabular.
            print(f"{produto[0]:<5} {produto[1]:<30} {produto[2]:<20} {produto[3]:<10} {produto[4]:<10} {produto[5]:<15}")
    else:
        print("Nenhum produto encontrado.")  # Caso não existam produtos no estoque.

# Função para registrar a entrada de um produto no estoque
def registrar_entrada(produto_id, quantidade):
    try:
        quantidade = int(quantidade)  # Converte a quantidade para inteiro.
    except ValueError:
        print("Quantidade inválida. Insira um número.")  # Exibe mensagem de erro caso a quantidade não seja um número.
        return
    
    try:
        conn = sqlite3.connect("estoque.db")  # Conecta ao banco de dados SQLite.
        cur = conn.cursor()  # Cria um cursor para realizar operações no banco de dados.
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtém a data e hora atuais.
        cur.execute("INSERT INTO Movimentacoes (produto_id, quantidade, tipo, data) VALUES (?, ?, 'entrada', ?)", 
                    (produto_id, quantidade, data))  # Registra a movimentação de entrada.
        cur.execute('UPDATE Produtos SET quantidade = quantidade + ? WHERE id = ?', (quantidade, produto_id))  # Atualiza a quantidade do produto no estoque.
        conn.commit()  # Confirma as alterações no banco de dados.
        print("Entrada registrada com sucesso!")  # Mensagem de sucesso.
    except sqlite3.Error as e:
        print(f"Erro ao registrar entrada: {e}")  # Exibe mensagem de erro caso algo dê errado.
    finally:
        conn.close()  # Fecha a conexão com o banco de dados.

# Função para registrar a saída de um produto do estoque
def registro_saida(produto_id, quantidade):
    try:
        quantidade = int(quantidade)  # Converte a quantidade para inteiro.
    except ValueError:
        print("Quantidade inválida. Insira um número.")  # Exibe mensagem de erro caso a quantidade não seja um número.
        return
    
    try:
        conn = sqlite3.connect("estoque.db")  # Conecta ao banco de dados SQLite.
        cur = conn.cursor()  # Cria um cursor para realizar operações no banco de dados.
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtém a data e hora atuais.
        cur.execute("INSERT INTO Movimentacoes (produto_id, quantidade, tipo, data) VALUES (?, ?, 'saida', ?)", 
                    (produto_id, quantidade, data))  # Registra a movimentação de saída.
        cur.execute('UPDATE Produtos SET quantidade = quantidade - ? WHERE id = ?', (quantidade, produto_id))  # Atualiza a quantidade do produto no estoque.
        conn.commit()  # Confirma as alterações no banco de dados.
        print("Saída registrada com sucesso!")  # Mensagem de sucesso.
    except sqlite3.Error as e:
        print(f"Erro ao registrar saída: {e}")  # Exibe mensagem de erro caso algo dê errado.
    finally:
        conn.close()  # Fecha a conexão com o banco de dados.

# Função para adicionar um novo produto ao estoque
def adicionar_produto():
    nome = input("Digite o nome do produto: ")  # Solicita o nome do produto.
    categoria = input("Digite a categoria do produto: ")  # Solicita a categoria do produto.

    try:
        quantidade = int(input("Digite a quantidade do produto: "))  # Solicita a quantidade do produto.
        preco = float(input("Digite o preço do produto: "))  # Solicita o preço do produto.
    except ValueError:
        print("Quantidade ou preço inválido. Insira valores numéricos.")  # Exibe mensagem de erro se a quantidade ou preço não forem numéricos.
        return

    localizacao = input("Digite a localização do produto: ")  # Solicita a localização do produto.

    try:
        conn = sqlite3.connect("estoque.db")  # Conecta ao banco de dados SQLite.
        cur = conn.cursor()  # Cria um cursor para realizar operações no banco de dados.
        cur.execute('''INSERT INTO Produtos (nome, categoria, quantidade, preco, localizacao) VALUES (?, ?, ?, ?, ?)''', 
                    (nome, categoria, quantidade, preco, localizacao))  # Adiciona o produto à tabela Produtos.
        conn.commit()  # Confirma as alterações no banco de dados.
        print("Produto adicionado com sucesso!")  # Mensagem de sucesso.
    except sqlite3.Error as e:
        print(f"Erro ao adicionar produto: {e}")  # Exibe mensagem de erro caso algo dê errado.
    finally:
        conn.close()  # Fecha a conexão com o banco de dados.

# Função para visualizar todas as movimentações de produtos
def visualizar_movimentacoes():
    try:
        conn = sqlite3.connect("estoque.db")  # Conecta ao banco de dados SQLite.
        cur = conn.cursor()  # Cria um cursor para realizar operações no banco de dados.
        cur.execute("SELECT Movimentacoes.*, Produtos.nome FROM Movimentacoes JOIN Produtos ON Movimentacoes.produto_id = Produtos.id")  # Junta as tabelas de movimentações e produtos.
        movimentacoes = cur.fetchall()  # Obtém todas as movimentações.
    except sqlite3.Error as e:
        print(f"Erro ao acessar movimentações: {e}")  # Exibe mensagem de erro caso algo dê errado.
        return
    finally:
        conn.close()  # Fecha a conexão com o banco de dados.

    # Exibe as movimentações, se encontradas.
    if movimentacoes:
        print("\nMovimentações no estoque:")
        print(f"{'ID':<5} {'Produto':<20} {'Quantidade':<10} {'Tipo':<10} {'Data':<20}")
        print("-"*70)
        for mov in movimentacoes:  # Exibe cada movimentação de forma tabular.
            print(f"{mov[0]:<5} {mov[1]:<20} {mov[2]:<10} {mov[3]:<10} {mov[4]:<20}")
    else:
        print("Nenhuma movimentação encontrada.")  # Caso não existam movimentações no banco.

# Função para gerar relatórios gráficos sobre o estoque
def gerar_relatorios():
    try:
        conn = sqlite3.connect("estoque.db")  # Conecta ao banco de dados SQLite.
        cur = conn.cursor()  # Cria um cursor para realizar operações no banco de dados.
        cur.execute("SELECT nome, quantidade FROM Produtos")  # Consulta o nome e quantidade dos produtos.
        produtos = cur.fetchall()  # Obtém todos os produtos.
    except sqlite3.Error as e:
        print(f"Erro ao acessar produtos: {e}")  # Exibe mensagem de erro caso algo dê errado.
        return
    finally:
        conn.close()  # Fecha a conexão com o banco de dados.

    # Cria o gráfico de barras de quantidade de produtos no estoque.
    if produtos:
        nomes = [produto[0] for produto in produtos]  # Obtém os nomes dos produtos.
        quantidades = [produto[1] for produto in produtos]  # Obtém as quantidades dos produtos.

        plt.figure(figsize=(10, 6))  # Define o tamanho da figura do gráfico.
        sns.barplot(x=nomes, y=quantidades, palette='viridis')  # Cria o gráfico de barras.
        plt.title('Quantidade de Produtos no Estoque')  # Título do gráfico.
        plt.xlabel('Produto')  # Rótulo do eixo X.
        plt.ylabel('Quantidade')  # Rótulo do eixo Y.
        plt.xticks(rotation=90)  # Rotaciona as labels do eixo X.
        plt.tight_layout()  # Ajusta o layout para evitar sobreposição.
        plt.show()  # Exibe o gráfico.

# Função principal, onde o menu e a lógica de execução do programa acontecem
def main():
    role = login()  # Realiza o login e obtém a função do usuário.

    if not role:  # Se o login falhar, encerra a execução.
        return
    
    while True:
        # Exibe o menu de opções baseado na função do usuário.
        if role == 'gerente':
            print("\nMenu Gerente:")
            print("1. Visualizar produtos")
            print("2. Registrar entrada de produto")
            print("3. Registrar saída de produto")
            print("4. Adicionar produto")
            print("5. Visualizar movimentações")
            print("6. Gerar relatórios")
            print("7. Registrar novo usuário")
            print("8. Trocar de usuário")
            print("9. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                visualizar_produtos()
            elif opcao == "2":
                produto_id = int(input("Digite o ID do produto: "))
                quantidade = input("Digite a quantidade a ser adicionada: ")
                registrar_entrada(produto_id, quantidade)
            elif opcao == "3":
                produto_id = int(input("Digite o ID do produto: "))
                quantidade = input("Digite a quantidade a ser retirada: ")
                registro_saida(produto_id, quantidade)
            elif opcao == "4":
                adicionar_produto()
            elif opcao == "5":
                visualizar_movimentacoes()
            elif opcao == "6":
                gerar_relatorios()
            elif opcao == "7":
                registrar_usuario()
            elif opcao == "8":
                role = trocar_usuario()
            elif opcao == "9":
                print("Saindo...")
                break
            else:
                print("Opção inválida.")
        elif role == 'estoquista':
            print("\nMenu Estoquista:")
            print("1. Visualizar produtos")
            print("2. Registrar entrada de produto")
            print("3. Registrar saída de produto")
            print("4. Visualizar movimentações")
            print("5. Trocar de usuário")
            print("6. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                visualizar_produtos()
            elif opcao == "2":
                produto_id = int(input("Digite o ID do produto: "))
                quantidade = input("Digite a quantidade a ser adicionada: ")
                registrar_entrada(produto_id, quantidade)
            elif opcao == "3":
                produto_id = int(input("Digite o ID do produto: "))
                quantidade = input("Digite a quantidade a ser retirada: ")
                registro_saida(produto_id, quantidade)
            elif opcao == "4":
                visualizar_movimentacoes()
            elif opcao == "5":
                role = trocar_usuario()
            elif opcao == "6":
                print("Saindo...")
                break
            else:
                print("Opção inválida.")
        elif role == 'usuario':
            print("\nMenu Usuário:")
            print("1. Visualizar produtos")
            print("2. Visualizar movimentações")
            print("3. Trocar de usuário")
            print("4. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                visualizar_produtos()
            elif opcao == "2":
                visualizar_movimentacoes()
            elif opcao == "3":
                role = trocar_usuario()
            elif opcao == "4":
                print("Saindo...")
                break
            else:
                print("Opção inválida.")

# Chama a função principal para rodar o programa
if __name__ == "__main__":
    main()