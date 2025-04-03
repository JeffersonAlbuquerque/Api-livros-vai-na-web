from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

#Flask: Framework para criar a API.
#request: Permite manipular dados enviados pelo cliente (como formulários ou JSON).
#jsonify: Converte os dados em JSON para serem enviados como resposta da API.
#sqlite3: Banco de dados leve que armazena os livros.
#CORS: Habilita requisições de diferentes origens (para permitir que o front-end acesse a API).

app = Flask(__name__)
CORS(app)

#app = Flask(name): Cria a aplicação Flask.
#CORS(app): Permite que a API seja acessada de domínios diferentes (evita erros de bloqueio de requisições entre diferentes origens).

def init_db():

    with sqlite3.connect("database.db") as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS LIVROS(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     titulo TEXT NOT NULL,
                     categoria TEXT NOT NULL,
                     autor TEXT NOT NULL,
                     image_url TEXT NOT NULL
                     )
""") 
#Cria a tabela "LIVROS" no banco de dados database.db, caso ela ainda não exista.
#id INTEGER PRIMARY KEY AUTOINCREMENT: Coluna "id" que é a chave primária e se autoincrementa automaticamente.
#titulo, categoria, autor, image_url: Campos obrigatórios (NOT NULL).

init_db()
#Aqui garante que a tabela seja criada antes de qualquer operação.

@app.route("/")
def bem_vindo():
    return "<h1>Fernanda não paga nada!</h1>"

#@app.route("/"): Define a rota principal (/).
#Retorna um HTML com a mensagem "Fernanda não paga nada!".

#end point é o router.
@app.route("/doar", methods=["POST"]) #POST, ENVIA OS DADOS PARA A API.
def doar():

    dados = request.get_json()

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    image_url = dados.get("image_url")

    with sqlite3.connect("database.db") as conn:
        conn.execute(f"""
            INSERT INTO LIVROS (titulo, categoria, autor, image_url)
            VALUES ("{titulo}", "{categoria}","{autor}","{image_url}")
""")
        
        conn.commit() #COMANDO PARA SALVAR AS MUDANÇAS NO BANCO DE DADOS.

        #return jsonify é pra retornar um arquivo json.
        return jsonify({"Mensagem":"Livro cadastrado com sucesso!"}), 201

#@app.route("/doar", methods=["POST"]): Define a rota /doar, que aceita requisições POST (envio de dados).
#request.get_json(): Obtém os dados enviados pelo cliente no formato JSON.
#conn.execute(INSERT INTO LIVROS ...): Insere os dados na tabela do banco de dados.
#conn.commit(): Confirma a inserção dos dados no banco.
#Retorna um JSON com a mensagem "Livro cadastrado com sucesso!" e status 201 (Recurso criado com sucesso).

@app.route("/livros", methods=["GET"]) #GET PUXA OS DADOS

def listar_livros():
    with sqlite3.connect("database.db") as conn:
        livros = conn.execute("SELECT * FROM LIVROS").fetchall()

        livros_formatados = []

        for item in livros:
            dicionario_livros = {
                "id":item[0],
                "titulo": item[1],
                "categoria": item[2],
                "autor":item[3],
                "image_url":item[4]
            }
            livros_formatados.append(dicionario_livros)
        return jsonify(livros_formatados), 200 #o 200, seria um "aviso" de sucesso, para saber mais, pesquisa HTTPS REQUESTS

#@app.route("/livros", methods=["GET"]): Define a rota /livros, que aceita requisições GET (para buscar dados).
#conn.execute("SELECT * FROM LIVROS").fetchall(): Busca todos os livros cadastrados no banco.
#Cada livro do banco é transformado em um dicionário, que depois é convertido para JSON.
#Retorna a lista de livros com o status 200 (sucesso).

if __name__ == "__main__":
    app.run(debug=True)

#if __name__ == "__main__": Garante que o script seja executado diretamente e não importado como módulo.

#Comando para ativar o ambiente virtual no terminal antes de rodar a API.
#source venv/Scripts/active

#O que esse código faz?
#Cria uma API Flask com um banco de dados SQLite.
#Possui 3 endpoints principais:
#/ → Página inicial.
#/doar (POST) → Adiciona um livro ao banco de dados.
#/livros (GET) → Retorna todos os livros cadastrados.
#Armazena os livros no banco SQLite com título, categoria, autor e imagem.
#Permite requisições de qualquer origem (CORS habilitado).
#Executa o servidor Flask em modo de depuração.


