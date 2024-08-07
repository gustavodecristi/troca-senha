import PySimpleGUI as sg
import senhas
import re

sg.theme("Reddit")
layout = [
    [sg.Text("TROCAR SENHA - SGU CARD", font=15)],
    [sg.Text("Usuário", font=7)],
    [sg.InputText(key="usuario", size= 200, font=3, enable_events=True)],
    [sg.Text("Senha", font=7)],
    [sg.InputText(key="senha", password_char='*', size= 200)],
    [sg.Text("Confirmar senha", font=7)],
    [sg.InputText(key="confirma_senha", password_char='*', size= 200)],
    [sg.Button("Confirmar", bind_return_key=True), sg.Button("Limpar")],
    [sg.Text("Após clicar em confirmar, aguarde a mensagem de concluído.", key="resultado")]
]
janela = sg.Window("Unimed Marília", layout, icon="unimed.ico", resizable=True, size=(400, 280))



while True:
    evento, valores = janela.read()
    
    if evento == sg.WIN_CLOSED:
        janela.close()
        break

    elif evento == "Limpar":
        janela["usuario"].update("")
        janela["senha"].update("")
        janela["confirma_senha"].update("")
        janela["resultado"].update("Após clicar em confirmar, aguarde a mensagem de concluído.")

    elif evento == "usuario":
        # Converte o texto digitado para maiúsculas enquanto o usuário digita
        janela["usuario"].update(valores["usuario"].upper())

    elif evento == "Confirmar":
        
        # Valida preenchimento dos campos
        if valores["usuario"] == "" or valores["senha"] == "" or valores["confirma_senha"] == "":
            janela["resultado"].update("Preencha todos os campos acima")
            
        # Valida usuário
        elif senhas.consulta_usuario(valores["usuario"]) == 0:
            janela["resultado"].update("Usuário não encontrado")
        
        # Valida requisitos de senha
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
        elif valores["senha"] in senhas.consulta_senhas(valores["usuario"]):
            janela["resultado"].update("Esta senha já foi utilizada anteriormente e não deve ser utilizada novamente")
            
        else:
            troca_senhas(valores["usuario"], valores["senha"])
            janela["resultado"].update("Senha alterada com sucesso!")
            

            