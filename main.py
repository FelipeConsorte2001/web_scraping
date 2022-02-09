import time
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
# from msilib.schema import tables
# from xml.dom.minidom import Element
# from attr import field
import requests

# Pegar HTML a partir da URL 
url = 'https://www.nba.com/stats/players/traditional/?sort=BLK&dir=-1'
top10ranking = {}

rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}


def buildrank(type):
    
    field = rankings[type]['field']
    label = rankings[type]['label']
    driver.find_element(By.XPATH, f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()

    element = driver.find_element(By.XPATH, "//div[@class='nba-stat-table']//table")
    html_content = element.get_attribute('outerHTML')

    # Parsear o conteudo HTML - BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # Estruturar conteudo em um Data Frame - Pandas
    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', label]]
    df.columns = ['pos', 'player', 'team', 'total']

    # Trasformar os dados em um dicionario
    return df.to_dict('records')

option = Options()
option.headless = True
driver = webdriver.Firefox()
driver.get(url)
time.sleep(10)

for i in rankings:
    top10ranking[i] = buildrank(i)

driver.quit()

# Salvar os dados em json
js = json.dumps(top10ranking)
fp = open('dados.json', 'w')
fp.write(js)
fp.close()