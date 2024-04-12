import PySimpleGUI as sg
import troca_senha
import re

sg.theme("Reddit")
layout = [
    [sg.Text("TROCAR SENHA - SGU CARD", font=15)],
    [sg.Text("Usuário", font=7)],
    [sg.InputText(key="usuario", size= 200, font=3)],
    [sg.Text("Senha", font=7)],
    [sg.InputText(key="senha", password_char='*', size= 200)],
    [sg.Text("Confirmar senha", font=7)],
    [sg.InputText(key="confirma_senha", password_char='*', size= 200)],
    [sg.Button("Confirmar", bind_return_key=True), sg.Button("Limpar")],
    [sg.Text("Após clicar em confirmar, aguarde a mensagem de concluído.", key="resultado")]
]
janela = sg.Window("Troca Senha", layout, resizable=True, size=(400, 280))


def open_window(user, password, confirm_password):
    sg.theme("LightBlue6")
    layout2 = [
        [sg.Text("Por favor aguarde.", font=20)]
    ]
    window = sg.Window("Processando...", layout2, modal=True, finalize=True, disable_minimize=True, disable_close=True)
    window.read(10)
    pega_status = troca_senha.troca_senha(user, password, confirm_password)
    window.close()
    return pega_status



while True:
    evento, valores = janela.read()

    if evento == sg.WIN_CLOSED:
        break

    usuario = valores["usuario"]
    senha = valores["senha"]
    confirma_senha = valores["confirma_senha"]

    if evento == "Limpar":
        janela["usuario"].update("")
        janela["senha"].update("")
        janela["confirma_senha"].update("")
        janela["resultado"].update("Após clicar em confirmar, aguarde a mensagem de concluído.")

    elif evento == "Confirmar":
        if valores["usuario"] == "" or valores["senha"] == "" or valores["confirma_senha"] == "":
            janela["resultado"].update("Preencha todos os campos acima")
        elif valores["senha"] != valores["confirma_senha"]:
            janela["resultado"].update("As senhas não conferem")
        elif len(valores["senha"]) < 8 or len(valores["senha"]) > 20:
            janela["resultado"].update("A senha deve conter entre 8 e 20 caracteres")
        elif not re.search(r'[A-Z]', valores["senha"]):
            janela["resultado"].update("A senha deve conter pelo menos uma letra maiúscula")
        elif not re.search(r'[a-z]', valores["senha"]):
            janela["resultado"].update("A senha deve conter pelo menos uma letra minúscula")
        elif not re.search(r'[0-9]', valores["senha"]):
            janela["resultado"].update("A senha deve conter pelo menos um número")
        elif not re.search(r'[^A-Za-z0-9]', valores["senha"]):
            janela["resultado"].update("A senha deve conter pelo menos um caractere especial")
        else:
            '''
            Lista de erros:
            001: Problema ao abrir Card Admin (função get)
            002: Problema ao fazer login, pode ser que a senha tenha expirado
            003: Erro ao pesquisar usuário
            004: Usuário não encontrado, provavelmente está inativo
            005: Erro na tela de trocar senha
            006: Erro não especificado, sendo necessário analisar a execução do código
            '''
            status = open_window(usuario, senha, confirma_senha)
            if status == "Sem erro":
                janela["resultado"].update("Senha alterada com sucesso.")
            elif status == "001":
                janela["resultado"].update("ERRO001: Problema ao abrir sistema.\nEntre em contato com o TI.")
            elif status == "002":
                janela["resultado"].update("ERRO002: Problema ao fazer login.\nEntre em contato com o TI.")
            elif status == "003":
                janela["resultado"].update("ERRO003: Problema ao pesquisar usuário.\nEntre em contato com o TI.")
            elif status == "004":
                janela["resultado"].update("ERRO004: Usuário inativo ou inexistente.\nEntre em contato com o TI.")
            elif status == "005":
                janela["resultado"].update("ERRO005: Problema ao trocar senha.\nEntre em contato com o TI.")
            else:
                janela["resultado"].update("ERRO006: Erro não especificado.\nEntre em contato com o TI.")

janela.close()