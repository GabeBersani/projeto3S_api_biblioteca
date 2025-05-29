from operator import truediv

from oauthlib.uri_validate import authority
from models import local_session, Usuarios, Livros, Emprestimos
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

    livros = []
    usuarios = []
    emprestimos = []

    # salvar livro
    def salvar_livro(e):
        if titulo.value == "" or autor.value == "" or ISBN.value == "" or resumo.value == "":
            page.overlay.append(msg_erro)
            msg_erro.open = True
            page.update()
        else:
            resposta = post_livro(titulo.value,autor.value,ISBN.value,resumo.value)

            if "erro" in resposta:
                msg_erro.open = True
            else:
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
        print("aqui99999")
        teste = get_livros()
        for l in teste:
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

    def exibir_lista_usuario(e):
        get_usuarios()
        for u in usuarios:
            usu_usuarios.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(u.nome),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="Detalhes do usuario"
                            ),
                        ],
                        on_select=lambda _, usu=u: ver_detalhes_usu(usu.nome, usu.CPF, usu.endereco),
                    )

                )
            )
        page.update()

    def ver_detalhes_usu(nome, CPF, endereco):
        txt_usu.value = (f"Nome: {nome}; \nCPF: {CPF}; \nEndereço: {endereco}.")
        page.go("/listar_detalhes_usu")


    def exibir_lista_emprestimo(e):
        get_emprestimos()
        for p in emprestimos:
            emp_emprestimos.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK),
                    title=ft.Text(p.data_emprestimo),
                    subtitle=ft.Text(p.data_devolucao),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="Detalhes Emprestimo"
                            ),
                        ],
                        on_select=lambda _, emp=p: ver_detalhes_empres(emp.data_emprestimo, emp.data_devolucao,
                                                                       emp.livro_emprestado, emp.usuario_emprestado,
                                                                       emp.id_usuario, emp.id_livro),
                    )

                )
            )
        page.update()

    def ver_detalhes_empres(data_emprestimo, data_devolucao, livro_emprestado, usuario_emprestado, id_usuario, id_livro):
        txt_empres.value = (f"Data de emprestimo: {data_emprestimo}; \nData de devolição: {data_devolucao}; \nLivro: "
                            f"{livro_emprestado}; \nUsuario: {usuario_emprestado}; \nId usuario:{id_usuario}; "
                            f"\nId livro:{id_livro}.")

        page.go("/listar_detalhes_usu")



    def gerencia_rota(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Home"), bgcolor=Colors.PINK),
                    ElevatedButton(text="Cadastro de livro", on_click=lambda _: page.go("/cadastro_liv"), color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                    ElevatedButton(text="Cadastro de usuario", on_click=lambda _: page.go("/cadastro_usu"), color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                    ElevatedButton(text="Emprestimo", on_click=lambda _: page.go("/emprestimo"), color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                    ElevatedButton(text="Lista de livros", on_click=lambda _: page.go("/lista_liv"), color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                    ElevatedButton(text="Lista de usuarios", on_click=lambda _: page.go("/lista_usu"), color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                    ElevatedButton(text="Lista de emprestimos", on_click=lambda _: page.go("/lista_emprestimo"), color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                ]
            )
        )
        page.update()


        if page.route == "/cadastro_liv":
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
                        ElevatedButton(text="Exibir Livros", on_click=lambda _: page.go("/lista_liv"),
                                       color=ft.CupertinoColors.SYSTEM_PINK, width=375),
                    ]
                )
            )
            page.update()

            if page.route == "/lista_liv":
                print("tela de livros")
                exibir_lista_livros(e)
                page.views.append(
                    View(
                        "/lista_liv",
                        [
                            AppBar(title=Text("Lista de Livros"), bgcolor=Colors.PINK),
                            lv_livro
                        ]
                    )
                )
                # page.update()

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



            if page.route == "/cadastro_usu":
                post_usuarios(nome.value, CPF.value, endereco.value)
                page.views.append(
                    View(
                        "/cadastro_usu",
                        [
                            AppBar(title=Text("Cadastro de Usuario"), bgcolor=Colors.PINK),
                            nome,
                            CPF,
                            endereco,
                            ElevatedButton(text="Salvar Usuario", on_click=salvar_usuario,
                                           color=ft.CupertinoColors.SYSTEM_PINK,
                                           width=375),
                        ]
                    )
                )
                page.update()

                if page.route == "/lista_usu":
                    exibir_lista_usuario(e)
                    page.views.append(
                        View(
                            "/lista_usu",
                            [
                                AppBar(title=Text("Lista de Usuarios"), bgcolor=Colors.PINK),
                                usu_usuarios
                            ]
                        )
                    )
                    page.update()

                if page.route == "/listar_detalhes_usu":
                    page.views.append(
                        View(
                            "/listar_detalhes_usu",
                            [
                                AppBar(title=Text("Lista de Usuarios"), bgcolor=Colors.PINK),
                                txt_usu,
                                ElevatedButton(text="Voltar", on_click=lambda _: page.go("/lista_usu"),
                                               color=ft.CupertinoColors.SYSTEM_PINK, width=375)
                            ]
                        )
                    )
                page.update()

                if page.route == "/emprestimo":
                    post_emprestimos(data_emprestimo.value, data_devolucao.value, livro_emprestado.value, usuario_emprestado.value,
                                     id_usuario.value, id_livro.value)
                    page.views.append(
                        View(
                            "/emprestimo",
                            [
                                AppBar(title=Text("Emprestimos"), bgcolor=Colors.PINK),
                                data_emprestimo,
                                data_devolucao,
                                livro_emprestado,
                                usuario_emprestado,
                                id_usuario,
                                id_livro,
                                ElevatedButton(text="Salvar emprestimo", on_click=salvar_emprestimo,
                                               color=ft.CupertinoColors.SYSTEM_PINK,
                                               width=375),
                            ]
                        )
                    )
                    page.update()


                    if page.route == "/lista_emprestimo":
                        exibir_lista_livros(e)
                        page.views.append(
                            View(
                                "/lista_emprestimo",
                                [
                                    AppBar(title=Text("Lista de Emprestimos"), bgcolor=Colors.PINK),
                                    emp_emprestimos
                                ]
                            )
                        )
                        page.update()

                    if page.route == "/listar_detalhes_emprestimo":
                        page.views.append(
                            View(
                                "/listar_detalhes_emprestimo",
                                [
                                    AppBar(title=Text("Lista de emprestimos"), bgcolor=Colors.PINK),
                                    txt_empres,
                                    ElevatedButton(text="Voltar", on_click=lambda _: page.go("/lista_emprestimo"),
                                                   color=ft.CupertinoColors.SYSTEM_PINK, width=375)
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

    txt_usu = ft.Text(value="")
    usu_usuarios = ft.ListView(
        height=500,
        spacing=1,
        divider_thickness=1,
    )

    txt_empres = ft.Text(value="")
    emp_emprestimos = ft.ListView(
        height=500,
        spacing=1,
        divider_thickness=1,
    )


    msg_sucesso = ft.SnackBar(content=Text("Livro cadastrado!"), bgcolor=Colors.GREEN)
    msg_erro = ft.SnackBar(content=Text("Não deixe campos vazio!"), bgcolor=Colors.RED)

    page.overlay.append(msg_sucesso)
    page.overlay.append(msg_erro)
    page.on_route_change = gerencia_rota
    page.on_view_pop = voltar

    page.go(page.route)


# Comando que executa o aplicativo
# Deve estar sempre colado na linha
ft.app(main)
