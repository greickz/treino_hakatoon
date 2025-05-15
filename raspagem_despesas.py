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
url = 'https://masander.github.io/AlimenticiaLTDA-financeiro/'
executador.get(url)
time.sleep(5)

coleta = {'ID_despesa': [],'Dados': [], 'Tipo': [], 'Setor': [], 'Valentia': [], 'Fornecedor': [] }
elementos = executador.find_elements(By.XPATH, "//table/tbody//tr")

try:
    WebDriverWait(executador, 10).until(
    ec.presence_of_all_elements_located((By.XPATH, '//table/tbody//tr'))
)
    print('Elementos encontrados com sucesso')
except TimeoutException:
    print('Tempo de espera excedido')


if len(elementos) == 0:
    print('Não foi encontrado nenhum elemento')

for elemento in elementos:
    try:
        ID_despesa = elemento.find_element(By.CLASS_NAME, 'td_id_despesa').text.strip()
        Dados = elemento.find_element(By.CLASS_NAME, 'td_data').text.strip()
        Tipo = elemento.find_element(By.CLASS_NAME, 'td_tipo').text.strip()
        Setor = elemento.find_element(By.CLASS_NAME, 'td_setor').text.strip()
        Valentia = elemento.find_element(By.CLASS_NAME, 'td_valor').text.strip()
        Fornecedor = elemento.find_element(By.CLASS_NAME, 'td_fornecedor').text.strip()
        coleta['ID_despesa'].append(ID_despesa)
        coleta['Dados'].append(Dados)
        coleta['Tipo'].append(Tipo)
        coleta['Setor'].append(Setor)
        coleta['Valentia'].append(Valentia)
        coleta['Fornecedor'].append(Fornecedor)
    except Exception as e:
            print(f'Erro ao coletar dados: {e}')

executador.quit()
df = pd.DataFrame(coleta)
df.to_excel('hackaton_treino_despesas.xlsx', index=False)
print(f'Arquivo "consoles.xlsx" salvo com sucesso! ({len(df)} produtos capturados)')






