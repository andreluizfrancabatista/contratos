from tqdm import tqdm
import time
import pandas as pd
import sys
import os
import numpy as np

"""# Configuração do Web-Driver"""
# Utilizando o WebDriver do Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Instanciando o Objeto ChromeOptions
options = webdriver.ChromeOptions()

# Passando algumas opções para esse ChromeOptions
# options.add_argument('--headless') # Não sei porque mas está dando erro na página de contratos.
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--start-maximized')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-crash-reporter')
options.add_argument('--log-level=3')
options.add_argument('--disable-gpu')
options.add_argument("--window-size=1920,1080")
options.add_argument('--allow-running-insecure-content')
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--disable-extensions")

# Criação do WebDriver do Chrome
wd_Chrome = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

"""# Importando as Bibliotecas"""


"""# Iniciando a Raspagem de Dados"""

# Com o WebDrive a gente consegue a pedir a página (URL)
wd_Chrome.get(
    "https://portaldatransparencia.gov.br/contratos/consulta?ordenarPor=dataFimVigencia&direcao=desc")
# time.sleep(10)
# wd_Chrome.get_screenshot_as_file("screenshot.png")
links = []
contratos = wd_Chrome.find_elements(By.CSS_SELECTOR, 'a.linkRendered')
for contrato in contratos:
    links.append(contrato.get_attribute('href'))


dados = {
    'Número do Contrato': [],
    'Vigência': [],
    'Contratado': [],
    'CPF/CNPJ': [],
    'Objeto': [],
    'Órgão superior': [],
    'Órgão subordinado': [],
    'Unidade gestora contratante': [],
    'Modalidade de contratação': [],
    'Processo de contratação': [],
    'Fundamento Legal': [],
    'Data de assinatura': [],
    'Data de publicação': [],
    'Situação': [],
    'Valor inicial do contrato': [],
    'Valor final do contrato': [],
    'Licitação': []
}


for link in links:
    wd_Chrome.get(link)
    dados = wd_Chrome.find_element(By.CSS_SELECTOR, 'section.dados-tabelados')
    rows = dados.find_elements(By.CSS_SELECTOR, 'div.row')
    numero     = rows[0].find_elements(By.CSS_SELECTOR, 'div')[0].find_element(By.CSS_SELECTOR,'span').text
    vigencia   = rows[0].find_elements(By.CSS_SELECTOR, 'div')[1].find_element(By.CSS_SELECTOR,'span').text
    contratado = rows[0].find_elements(By.CSS_SELECTOR, 'div')[2].find_element(By.CSS_SELECTOR,'span').text
    cpf_cnpj   = rows[0].find_elements(By.CSS_SELECTOR, 'div')[3].find_element(By.CSS_SELECTOR,'span').text
    # print(f'Número: {numero}\nVigência: {vigencia}\nContratado: {contratado}\nCPF/CNPJ:{cpf_cnpj}')
    objeto     = rows[1].find_element(By.CSS_SELECTOR, 'span').text
    # print(f'Objeto: {objeto}')
    orgao_superior    = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div>div:nth-child(1)')[0].find_element(By.CSS_SELECTOR,'span').text
    # print(f'Orgao superior: {orgao_superior}')
    orgao_subordinado = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div>div:nth-child(2)')[0].find_element(By.CSS_SELECTOR,'span').text
    # print(f'Orgao subordinado: {orgao_subordinado}')
    unidade_gestora   = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div>div:nth-child(3)')[0].find_element(By.CSS_SELECTOR,'span').text
    # print(f'Unidade gestora: {unidade_gestora}')
    modalidade        = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div>div:nth-child(4)')[0].find_element(By.CSS_SELECTOR,'span').text
    # print(f'Modalidade: {modalidade}')
    