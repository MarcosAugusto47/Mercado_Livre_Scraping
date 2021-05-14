import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re
PATH = "C:/Users/marco/anaconda3/chromedriver"

driver = webdriver.Chrome(PATH)
driver.maximize_window()
url = "https://lista.mercadolivre.com.br"
driver.get(url)

produtos_list = []
precos_list = []
pesquisa = driver.find_element_by_xpath('/html/body/header/div/form/input')
pesquisa.clear()
pesquisa.send_keys(input("O que você procura?"))
pesquisa.send_keys(Keys.RETURN)

NUMERO_PAGINAS = int(input('Digite o número de páginas para fazer a busca:'))

for j in (range(1, NUMERO_PAGINAS + 1)):
    url = driver.current_url
    driver.get(url)
    
    produtos = driver.find_elements_by_tag_name("h2")
    precos = driver.find_elements_by_xpath('//div[@class="ui-search-price ui-search-price--size-medium ui-search-item__group__element"]//div[@class="ui-search-price__second-line"]')
    
    produtos = [item.text for item in produtos]
    precos = [item.text for item in precos]
    
    produtos_list = produtos_list + produtos
    precos_list = precos_list + precos
    
    if (j == 1):
        x_path = '//*[@id="root-app"]/div/div[1]/section/div[4]/ul/li[11]/a'
    else:
        x_path = '//*[@id="root-app"]/div/div[1]/section/div[4]/ul/li[12]/a'

    
    try:
        botao = driver.find_element_by_xpath(x_path)
    
    except:
        botao = driver.find_element_by_xpath(re.sub("4", "3", x_path))
    
    driver.execute_script("arguments[0].click();", botao)  
df = pd.DataFrame(list(zip(produtos_list, precos_list)), columns = ['Produtos', 'Preços'])
df['Preços'] = df['Preços'].str.replace("[\nOF]", "")

df