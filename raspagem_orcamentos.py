from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time

caminho = r"C:\Program Files\chromedriver-win64\chromedriver-win64\chromedriver.exe"
servico = Service(caminho)
opcoes = webdriver.ChromeOptions()
opcoes.add_argument('--disable-gpu')
opcoes.add_argument('--window-size=1920,1080')
executador = webdriver.Chrome(service= servico, options= opcoes)
url = 'https://masander.github.io/AlimenticiaLTDA-financeiro/#/'
executador.get(url)
time.sleep(5)

coleta = {'Setor': [], 'Eu': [], 'Ano': [], 'Valor_previsto': [], 'Valor_realizado': [] }
elementos = executador.find_elements(By.XPATH, "//table/tbody//tr")
botao = executador.find_elements(By.XPATH, "//div[@class='App']//button[text()='Orçamentos']")

try:
    WebDriverWait(executador, 10).until(
    ec.presence_of_all_elements_located((By.XPATH, '//di'))
)
    print('Elementos encontrados com sucesso')
except TimeoutException:
    print('Tempo de espera excedido')

botao[0].click()


if len(botao) == 0:
    print('Não foi encontrado nenhum elemento')

for elemento in elementos:
    try:
        Setor = elemento.find_element(By.CLASS_NAME, 'td_setor').text.strip()
        Eu = elemento.find_element(By.CLASS_NAME, 'td_mes').text.strip()
        Ano = elemento.find_element(By.CLASS_NAME, 'td_ano').text.strip()
        Valor_previsto = elemento.find_element(By.CLASS_NAME, 'td_valor_previsto').text.strip()
        Valor_realizado = elemento.find_element(By.CLASS_NAME, 'td_valor_realizado').text.strip()
        coleta['Setor'].append(Setor)
        coleta['Eu'].append(Eu)
        coleta['Ano'].append(Ano)
        coleta['Valor_previsto'].append(Valor_previsto)
        coleta['Valor_realizado'].append(Valor_realizado)
    except Exception as e:
            print(f'Erro ao coletar dados: {e}')

executador.quit()
df = pd.DataFrame(coleta)
df.to_excel('hackaton_treino_orcamento.xlsx', index=False)
print(f'Arquivo "consoles.xlsx" salvo com sucesso! ({len(df)} produtos capturados)')






