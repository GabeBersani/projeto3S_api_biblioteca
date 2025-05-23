import requests

from api import *
def get_livros():
    url = 'http://10.135.232.32:5000/livros'
    response =requests.get(url)
    if response.status_code == 200:
        dados = response.json()

        print(dados)
    else:
        print('algo deu errado')
def post_livro(titulo,autor,ISBN,resumo):
    url = 'http://10.135.232.32:5000/cadastro_livros'
    livro = {
        'titulo': titulo,
        'autor': autor,
        'ISBN': ISBN,
        'resumo': resumo
    }
    response =requests.post(url, json=livro)
    if response.status_code == 200:
        print('deu certo')
        dados_post = response.json()
        print(dados_post)
    else:
        print('fudeu')

# get_livros()
# post_livro('pequeno principe','gabriele',123456789,'muito legal')