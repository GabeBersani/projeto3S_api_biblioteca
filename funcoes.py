import requests

from api import *

def get_livros():
    url = 'http://10.135.232.8:5001/livros'
    response =requests.get(url)
    print(response)
    if response.status_code == 200:
        dados = response.json()
        print(dados)
        return dados
    else:
        print('algo deu errado')

#get_livros()

def post_livro(titulo,autor,ISBN,resumo):
    url = 'http://10.135.232.8:5001/cadastro_livros'
    livro = {
        'titulo': titulo,
        'autor': autor,
        'ISBN': ISBN,
        'resumo': resumo
    }
    response =requests.post(url, json=livro)
    if response.status_code == 201:
        print('deu certo')
        dados_post = response.json()
        print(dados_post)
        return dados_post
    else:
        print('fudeu')
        return {
            'erro': response.json(),
        }
# get_livros()
# post_livro('pequeno principe','gabriele',123456789,'muito legal')

def get_usuarios():
    url = 'http://10.135.232.8:5001/usuarios'
    response =requests.get(url)
    if response.status_code == 200:
        dados = response.json()

        print(dados)
    else:
        print('algo deu errado')

def post_usuarios(nome, CPF, endereco):
    url = 'http://10.135.232.8:5001/cadastro_usuario'
    usuario = {
        'Nome': nome,
        'CPF': CPF,
        'Endereço': endereco
    }
    response =requests.post(url, json=usuario)
    if response.status_code == 200:
        dados_post = response.json()
        print(dados_post)

def get_emprestimos():
    url = 'http://10.135.232.8:5001/emprestimos'
    response =requests.get(url)
    if response.status_code == 200:
        dados = response.json()

        print(dados)
    else:
        print('algo deu errado')

def post_emprestimos(data_emprestimo, data_devolucao, livro_emprestado, usuario_emprestado, id_usuario, id_livro):
    url = 'http://10.135.232.8:5001/realizacao_emprestimos'
    emprestimo = {
        'data_emprestimo': data_emprestimo,
        'data_devolucao': data_devolucao,
        'livro_emprestado': livro_emprestado,
        'usuario_emprestado': usuario_emprestado,
        'id_usuario': id_usuario,
        'id_livro': id_livro,
    }
    response =requests.post(url, json=emprestimo)
    if response.status_code == 200:
        dados_post = response.json()
        print(dados_post)