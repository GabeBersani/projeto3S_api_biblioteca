from operator import truediv

from oauthlib.uri_validate import authority

from funcoes import *
import flet as ft
from flet import AppBar, Text, View, ElevatedButton
from flet.core.colors import Colors
from sqlalchemy import select


def main(page: ft.Page):
    # Configurações
    page.title = "Exemplo de Rotas"
    page.theme_mode = ft.ThemeMode.DARK  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    # livros = []

    # salvar usuario
    def salvar_livro(e):
        if titulo.value == "" or autor.value == "" or ISBN.value == "" or resumo.value == "":
            page.overlay.append(msg_erro)
            msg_erro.open = True
            page.update()
        else:
            livro = Livros(
                titulo=titulo.value,
                autor=autor.value,
                ISBN=ISBN.value,
                resumo=resumo.value,
            )
            livro.save()
            titulo.value = ""
            autor.value = ""
            ISBN.value = ""
            resumo.value = ""
            msg_sucesso.open = True
            page.update()

    # salvar usuario
    def salvar_usuario(e):
        if nome.value == "" or CPF.value == "" or endereco.value == "":
            page.overlay.append(msg_erro)
            msg_erro.open = True
            page.update()
        else:
            usuario = Usuarios(
                nome=nome.value,
                CPF=CPF.value,
                endereco=endereco.value,
            )
            usuario.save()
            nome.value = ""
            CPF.value = ""
            endereco.value = ""
            msg_sucesso.open = True
            page.update()

    # salvar emprestimo
    def salvar_emprestimo(e):
        if (data_emprestimo.value == "" or data_devolucao.value == "" or livro_emprestado.value == "" or usuario_emprestado.value == ""
                or id_usuario.value == "" or id_livro.value == ""):
            page.overlay.append(msg_erro)
            msg_erro.open = True
            page.update()
        else:
            emprestimo = Emprestimos(
                data_emprestimo=data_emprestimo.value,
                data_devolucao=data_devolucao.value,
                livro_emprestado=livro_emprestado.value,
                usuario_emprestado=usuario_emprestado.value,
                id_usuario=id_usuario.value,
                id_livro=id_livro.value,
            )
            Emprestimos.save()
            data_emprestimo.value = ""
            data_devolucao.value = ""
            livro_emprestado.value = ""
            usuario_emprestado.value = ""
            id_usuario.value = ""
            id_livro.value = ""
            msg_sucesso.open = True
            page.update()




    # lista de livros
    def exibir_lista_livros(e):
        lv_livro.controls.clear()

        book = select(Livros)
        livros = db_session.execute(book).scalars().all()

        for l in livros:
            lv_livro.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(l.titulo),
                    subtitle=ft.Text(l.autor),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="Detalhes do livro"
                            ),
                        ],
                        on_select=lambda _, liv=l: ver_detalhes(liv.titulo, liv.autor, liv.ISBN, liv.resumo),
                    )

                )
            )
        page.update()

    def ver_detalhes(titulo, autor, ISBN, resumo):
        txt.value = (f"Titulo: {titulo}; \nAutor: {autor}; \nISBN: {ISBN}; \nResumo: {resumo}.")
        page.go("/listar_detalhes")



    def gerencia_rota(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Home"), bgcolor=Colors.PINK),
                    ElevatedButton(text="Cadastro de livro", on_click=lambda _: page.go("/cadastro_liv"), color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                    ElevatedButton(text="Cadastro de usuario", on_click=lambda _: page.go("/lista"), color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                    ElevatedButton(text="Emprestimo", on_click=lambda _: page.go("/lista"), color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                    ElevatedButton(text="Lista de livros", on_click=lambda _: page.go("/lista"), color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                    ElevatedButton(text="Lista de usuarios", on_click=lambda _: page.go("/lista"), color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                    ElevatedButton(text="Lista de emprestimos", on_click=lambda _: page.go("/lista"), color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                ]
            )
        )


        if page.route == "/cadastro_liv":
            cadastro_liv(e)
            page.views.append(
                View(
                    "/cadastro_liv",
                    [
                        AppBar(title=Text("Cadastro de Livros"), bgcolor=Colors.PINK),
                        titulo,
                        autor,
                        ISBN,
                        resumo,
                        ElevatedButton(text="Salvar Livro", on_click=salvar_livro, color=ft.CupertinoColors.SYSTEM_PINK,
                                       width=375),
                        ElevatedButton(text="Exibir Livros", on_click=lambda _: page.go("/lista_de_livros"),
                                       color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                    ]
                )
            )

            if page.route == "/lista_de_livros":
                exibir_lista(e)
                page.views.append(
                    View(
                        "/lista",
                        [
                            AppBar(title=Text("Lista de Livros"), bgcolor=Colors.PINK),
                            get_livros()
                        ]
                    )
                )

            if page.route == "/listar_detalhes":
                page.views.append(
                    View(
                        "/listar_detalhes",
                        [
                            AppBar(title=Text("Lista de Livros"), bgcolor=Colors.PINK),
                            txt,
                            ElevatedButton(text="Voltar", on_click=lambda _: page.go("/lista_de_livro"), color=ft.CupertinoColors.SYSTEM_PINK, width=375)
                        ]
                    )
                )
            page.update()

    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Campos
    # usuario
    nome = ft.TextField(label="Nome")
    endereco = ft.TextField(label="Endereço")
    CPF = ft.TextField(label="CPF")

    # emprestivo
    data_emprestimo = ft.TextField(label="Data emprestimo")
    data_devolucao = ft.TextField(label="Data devolução")
    livro_emprestado = ft.TextField(label="Livro emprestado")
    usuario_emprestado = ft.TextField(label="Usuario emprestado")
    id_usuario = ft.TextField(label="ID Usuario")
    id_livro = ft.TextField(label="ID Livro")

    # livros
    titulo = ft.TextField(label="Titulo")
    autor = ft.TextField(label="Autor")
    ISBN = ft.TextField(label="ISBN")
    resumo = ft.TextField(label="Resumo")


    txt = ft.Text(value="")
    lv_livro = ft.ListView(
        height=500,
        spacing=1,
        divider_thickness=1,
    )

    msg_sucesso = ft.SnackBar(content=Text("Livro cadastrado!"), bgcolor=Colors.GREEN)
    msg_erro = ft.SnackBar(content=Text("Não deixe campos vazio!"), bgcolor=Colors.RED)

    page.overlay.append(msg_sucesso)
    page.overlay.append(msg_erro)
    page.on_route_change = gerencia_rota()
    page.on_view_pop = voltar

    page.go(page.route)


# Comando que executa o aplicativo
# Deve estar sempre colado na linha
ft.app(main)
