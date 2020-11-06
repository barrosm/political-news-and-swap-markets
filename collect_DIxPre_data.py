### !/usr/bin/env python

"""scrap_bmf.py: Webscraping Taxas Referenciais BMF"""

__author__      = "Mauricio Mendes"
__copyright__   = "Copyright 2020, Porto Alegre, RS, Brasil"

from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date 
from datetime import timedelta
import numpy as np
import pandas as pd
import time
import csv
import holidays
import matplotlib.pyplot as plt


#Inicializar datas
hoje = date.today()
date2 = hoje.strftime("%d/%m/%Y")     #formato da data na URL
date3 = hoje - timedelta(days=4)
date4 = date3.strftime("%d/%m/%Y")
date9 = date(2017,2,1)                         #cópia
date10 = date9.strftime("%d/%m/%Y")

#Inicializar listas
row_list = list()
di = []
feriados = holidays.Brazil()
d30 = None
d60 = None
d90 = None
d180 = None
d360 = None
d1800 = None
d3600 = None
d10800 = None

#Inicializar browser
driver = webdriver.Chrome()
driver.get("http://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp")

#Loop
while date9 < date(2020,10,3):
    if date9.weekday() < 5 and date9 not in feriados:                                                  #Verifica se é dia útil
        
        driver.get("http://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/TxRef1.asp?Data="+date10+"&Data1=20201015&slcTaxa=PRE" ) #Acessa o link 
        encontrado = True
        soup=BeautifulSoup(driver.page_source)                                                         #Pega todo o código fonte
        try:
            rows = soup.find('table', attrs={'class': 'tabConteudo'}).find('tbody').find_all('tr')         #procura a tabela
        except AttributeError:
            encontrado = False
        if encontrado == True:
            for row in rows:
                cells = row.find_all('td')                    #busca o div do item
                rn = [i.text.replace("\n","") for i in cells] #copia cada texto 
                row_list.append(rn)                           #adiciona na lista de linhas
    
    
        for i in row_list:
            if i[0] == "30" or i[0] == 29 or i[0] == 31 or i[0] == 32:
                d30 = float(i[1].replace(",", "."))
            elif i[0] == "60":
                d60 = float(i[1].replace(",", "."))
            elif i[0] == "90":
                d90 = float(i[1].replace(",", "."))
            elif i[0] == "180":
                d180 = float(i[1].replace(",", "."))
            elif i[0] == "360":
                d360 = float(i[1].replace(",", "."))
            elif i[0] == "1800":
                d1800 = float(i[1].replace(",", "."))
            elif i[0] == "3600" or i[0] == "3601" or i[0] == "3602":
                d3600 = float(i[1].replace(",", "."))
            elif i[0] == "10800":
                d10800 = float(i[1].replace(",", "."))
   
    di.append(date9)                      #adiciona os itens na lista
    di.append(d30)
    di.append(d60)
    di.append(d90)
    di.append(d180)
    di.append(d360)
    di.append(d1800)
    di.append(d3600)
    di.append(d10800)
    
    date9 = date9 + timedelta(days=1)     #avança/retorna 1 dia
    date10 = date9.strftime("%d/%m/%Y")
    

dj =np.array(di)                          #array para formato numpy
size = len(dj)/9
dk = dj.reshape(int(size),9)           #formatar o array
df2 = pd.DataFrame(dk, columns=['data','30','60','90','180','360','1800','3600','10800'])                    #converte para dataframe
print(df2)
df2.to_csv('dixpreV2.csv')           #converte e salva o csv

ax = plt.gca()                                      #plota o grafico
df2.plot(kind='line', x = 'data', y='30',ax=ax)
df2.plot(kind='line', x = 'data', y='60',ax=ax)
df2.plot(kind='line', x = 'data', y='90',ax=ax)
df2.plot(kind='line', x = 'data', y='180',ax=ax)
df2.plot(kind='line', x = 'data', y='360',ax=ax)
df2.plot(kind='line', x = 'data', y='1800',ax=ax)
df2.plot(kind='line', x = 'data', y='3600',ax=ax)
df2.plot(kind='line', x = 'data', y='10800',ax=ax)
plt.savefig('dixpre.png')
