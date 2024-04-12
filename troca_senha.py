# Importação das bibliotecas a serem usadas no software

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from config import link_sistema, login, senha

'''
A função abaixo vai servir para trocar a senha do usuário dentro do SGU Card.
Utilizando o Selenium (biblioteca de automação Python), o "robô" vai abrir o sistema, infomar login, senha
e fazer o acesso. Depois disso vai seguir o caminho até chegar na tela de pesquisa de usuários, quando isso acontecer,
ele vai receber o usuário desejado como parâmetro, realizar a pesquisa e trocar a senha.
'''


def troca_senha(user, passwd, confirm_passwd):  # Parâmetros: Usuário, Senha e Confirmação da senha
    options = Options()
    options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())

    navegador = webdriver.Chrome(
        service=service,
        options=options,
    )


    erro = []

    try:
        # Entrando no link e fazendo login.
        navegador.get(link_sistema)
        navegador.maximize_window()
        
    except:
        erro.append("001")

    try:

        navegador.find_element(By.XPATH, '//*[@id="login"]').send_keys(login)  # Usuário
        navegador.find_element(By.XPATH, '//*[@id="passwordTemp"]').send_keys(senha)  # Senha
        navegador.find_element(By.XPATH, '//*[@id="Button_DoLogin"]').click()  # Botão de entrar
        WebDriverWait(navegador, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="conteudo"]/table/tbody/tr[34]/td[1]/a')))  # Função de espera, serve para esperar a página carregar

    except:
        erro.append("002")

    try:
        navegador.find_element(By.XPATH, '//*[@id="conteudo"]/table/tbody/tr[34]/td[1]/a').click()  # Acessar página de usuários

        WebDriverWait(navegador, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="conteudo"]/form/table/tbody/tr[5]/td/input')))
        navegador.find_element(By.XPATH, '//*[@id="conteudo"]/form/table/tbody/tr[2]/td[2]/input').send_keys(user)  # Preenche o campo de pesquisa com o parâmetro 'User'
        navegador.find_element(By.XPATH, '//*[@id="conteudo"]/form/table/tbody/tr[5]/td/input').click()  # Botão pesquisar

    except:
        erro.append("003")

    try:
        WebDriverWait(navegador, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="conteudo"]/table/tbody/tr[2]/td[8]/span[1]/a/img')))
        navegador.find_element(By.XPATH, '//*[@id="conteudo"]/table/tbody/tr[2]/td[8]/span[1]/a/img').click()  # Acessa a página de senha do usuário

        WebDriverWait(navegador, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="conteudo"]/form/table/tbody/tr[10]/td/input[2]')))
        navegador.find_element(By.XPATH, '//*[@id="conteudo"]/form/table/tbody/tr[9]/td[2]/input[2]').click()  # Marca o campo 'Bloqueado' como 'Não'

        Select(navegador.find_element(By.ID, 'FG_SITUACAO')).select_by_visible_text('Sim')  # Seleciona a opção de trocar a senha no próximo acesso

        navegador.find_element(By.XPATH, '//*[@id="conteudo"]/form/table/tbody/tr[7]/td[4]/input').send_keys(passwd)  # Campo de senha que recebe o parâmetro 'passwd'
        navegador.find_element(By.XPATH, '//*[@id="conteudo"]/form/table/tbody/tr[8]/td[4]/input').send_keys(confirm_passwd)  # Campo de confirmação que recebe o parâmetro 'confirm_passwd'
        navegador.find_element(By.XPATH, '//*[@id="conteudo"]/form/table/tbody/tr[10]/td/input[2]').click()  # Botão confirmar

    except TimeoutException:
        erro.append("004")

    except:
        erro.append("005")

    erro.append("Sem erro")
    return erro[0]
