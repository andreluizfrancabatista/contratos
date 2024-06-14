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
options.add_argument("--disable-extensions")
# options.add_argument("--window-size=1920,1080")
# options.add_argument('--allow-running-insecure-content')
# options.add_argument("--proxy-server='direct://'")
# options.add_argument("--proxy-bypass-list=*")

# Criação do WebDriver do Chrome
wd_Chrome = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

"""# Importando as Bibliotecas"""

"""# Iniciando a Raspagem de Dados"""

# Com o WebDrive a gente consegue a pedir a página (URL)
wd_Chrome.get("https://portaldatransparencia.gov.br/contratos/consulta?ordenarPor=dataFimVigencia&direcao=desc")
# wd_Chrome.get_screenshot_as_file("screenshot.png")

links = []
contratos = wd_Chrome.find_elements(By.CSS_SELECTOR, 'a.linkRendered')
for contrato in contratos:
    links.append(contrato.get_attribute('href'))

info = {
    'Número do Contrato': [],
    'Vigência': [],
    'Contratado': [],
    'CPF/CNPJ': [],
    'CEP':[],
    'Email':[],
    'Telefone':[],
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
    empresa    = rows[0].find_elements(By.CSS_SELECTOR, 'div')[3].find_element(By.CSS_SELECTOR,'a').get_attribute('href')
    # print(f'Número: {type(numero)}\nVigência: {vigencia}\nContratado: {contratado}\nCPF/CNPJ:{cpf_cnpj}')
    objeto     = rows[1].find_element(By.CSS_SELECTOR, 'span').text
    # print(f'Objeto: {objeto}')
    orgao_superior    = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div:nth-child(1)>div:nth-child(1)')[0].find_element(By.CSS_SELECTOR,'span').text
    # print(f'Orgao superior: {orgao_superior}')
    orgao_subordinado = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div:nth-child(1)>div:nth-child(2)')[0].find_element(By.CSS_SELECTOR,'span').text
    # print(f'Orgao subordinado: {orgao_subordinado}')
    unidade_gestora   = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div:nth-child(1)>div:nth-child(3)')[0].find_element(By.CSS_SELECTOR,'span').text
    # print(f'Unidade gestora: {unidade_gestora}')
    modalidade        = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div:nth-child(1)>div:nth-child(4)')[0].find_element(By.CSS_SELECTOR,'span').text
    # print(f'Modalidade: {modalidade}')
    processo_contrat  = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div:nth-child(3)>div:nth-child(1)')[0].find_element(By.CSS_SELECTOR,'span').text
    # print(f'Processo contratação: {processo_contrat}')
    fundamento_legal  = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div:nth-child(3)>div:nth-child(2)')[0].find_element(By.CSS_SELECTOR,'span').text
    # print(f'Fundamento legal: {fundamento_legal}')
    data_assinatura   = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div:nth-child(3)>div:nth-child(3)')[0].find_element(By.CSS_SELECTOR,'span').text
    data_publicacao   = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div:nth-child(3)>div:nth-child(4)')[0].find_element(By.CSS_SELECTOR,'span').text
    # print(f'{data_assinatura}, {data_publicacao}')
    situacao          = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div:nth-child(5)>div:nth-child(1)')[0].find_element(By.CSS_SELECTOR,'span').text
    valor_inicial     = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div:nth-child(5)>div:nth-child(2)')[0].find_element(By.CSS_SELECTOR,'span').text
    valor_final       = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div:nth-child(5)>div:nth-child(3)')[0].find_element(By.CSS_SELECTOR,'span').text
    licitacao         = rows[2].find_elements(By.CSS_SELECTOR, 'div>div>div:nth-child(5)>div:nth-child(4)')[0].find_element(By.CSS_SELECTOR,'span').text
    # print(f'{situacao}, {valor_inicial}, {valor_final}, {licitacao}')

    wd_Chrome.get(empresa)
    dados    = wd_Chrome.find_element(By.CSS_SELECTOR, 'section.dados-tabelados')
    rows     = dados.find_elements(By.CSS_SELECTOR, 'div.row')
    email    = rows[0].find_elements(By.CSS_SELECTOR, 'div')[2].find_element(By.CSS_SELECTOR,'span').text
    telefone = rows[0].find_elements(By.CSS_SELECTOR, 'div')[3].find_element(By.CSS_SELECTOR,'span').text
    cep      = rows[2].find_elements(By.CSS_SELECTOR, 'div')[3].find_element(By.CSS_SELECTOR,'span').text
    # print(f'{email}, {telefone}, {cep}')

    info['Número do Contrato'].append(numero)
    info['Vigência'].append(vigencia)
    info['Contratado'].append(contratado)
    info['CPF/CNPJ'].append(cpf_cnpj)
    info['CEP'].append(cep)
    info['Email'].append(email)
    info['Telefone'].append(telefone)
    info['Objeto'].append(objeto)
    info['Órgão superior'].append(orgao_superior)
    info['Órgão subordinado'].append(orgao_subordinado)
    info['Unidade gestora contratante'].append(unidade_gestora)
    info['Modalidade de contratação'].append(modalidade)
    info['Processo de contratação'].append(processo_contrat)
    info['Fundamento Legal'].append(fundamento_legal)
    info['Data de assinatura'].append(data_assinatura)
    info['Data de publicação'].append(data_publicacao)
    info['Situação'].append(situacao)
    info['Valor inicial do contrato'].append(valor_inicial)
    info['Valor final do contrato'].append(valor_final)
    info['Licitação'].append(licitacao)

wd_Chrome.quit()

df = pd.DataFrame(info)
df.reset_index(inplace=True, drop=True)
df.index = df.index.set_names(['Index'])
df = df.rename(index=lambda x: x + 1)

filename = "dataset_contratos.csv"
df.to_csv(filename, sep=";")