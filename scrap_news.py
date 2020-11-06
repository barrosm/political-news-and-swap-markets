import time
import numpy as np
import pandas as pd
import holidays
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date 
from datetime import timedelta


def dia_da_semana(dia):
    if date9.weekday() == 0:
        dia = "/segunda-feira-"
    elif date9.weekday() == 1:
        dia = "/terca-feira-"
    elif date9.weekday() == 2:
        dia = "/quarta-feira-"
    elif date9.weekday() == 3:
        dia = "/quinta-feira-"
    elif date9.weekday() == 4:
        dia = "/sexta-feira-"
    elif date9.weekday() == 5:
        dia = "/sabado-"
    elif date9.weekday() == 6:
        dia = "/domingo-"
    return(dia)

def mes_por_extenso(mes):
    if date9.month == 1:
        mes = "-de-janeiro"
    elif date9.month == 2:
        mes = "-de-fevereiro"
    elif date9.month == 3:
        mes = "-de-marco" 
    elif date9.month == 4:
        mes = "-de-abril"
    elif date9.month == 5:
        mes = "-de-maio"
    elif date9.month == 6:
        mes = "-de-junho"
    elif date9.month == 7:
        mes = "-de-julho"
    elif date9.month == 8:
        mes = "-de-agosto"
    elif date9.month == 9:
        mes = "-de-setembro"
    elif date9.month == 10:
        mes = "-de-outubro"
    elif date9.month == 11:
        mes = "-de-novembro"
    elif date9.month == 12:
        mes = "-de-dezembro"
    return(mes)

def gera_link(data,mes_extenso,dia_semana):
    
    mes_numero = ""
    if data > date_new_format:
        if data.month < 10:
            mes_numero = "0"+str(data.month)
        else:
            mes_numero = str(data.month)
        
        if data.day == 1:
            dia_link = "/0"+str(data.day)
            link = "https://g1.globo.com/resumo-do-dia/noticia/"+str(data.year)+"/"+mes_numero+"/0"+str(data.day)+dia_semana+str(data.day)+"o"+mes_extenso+".ghtml"
        elif data.day <10:
            link = "https://g1.globo.com/resumo-do-dia/noticia/"+str(data.year)+"/"+mes_numero+"/0"+str(data.day)+dia_semana+str(data.day)+mes_extenso+".ghtml"
        else: 
            link = "https://g1.globo.com/resumo-do-dia/noticia/"+str(data.year)+"/"+mes_numero+"/"+str(data.day)+dia_semana+str(data.day)+mes_extenso+".ghtml"
    elif data > date_old_format:
        link = "https://g1.globo.com/resumo-do-dia/noticia"+dia_semana+str(data.day)+mes_extenso+".ghtml"
    else:
        link = "https://g1.globo.com/resumo-do-dia/noticia"+dia_semana+str(data.day)+mes_extenso+".ghtml"
    return link

def gera_link2(data,mes_extenso,dia_semana):
    link = "https://g1.globo.com/resumo-do-dia/noticia"+dia_semana+str(data.day)+mes_extenso+".ghtml"
    return link
def gera_link3(data,mes_extenso,dia_semana):
    link = "https://g1.globo.com/resumo-do-dia/noticia"+dia_semana+str(data.day)+mes_extenso+"-de-"+str(data.year)+".ghtml"
    return link
def gera_link4(data,mes_extenso,dia_semana):
    link = "https://g1.globo.com/resumo-do-dia/noticia"+dia_semana.replace("-feira","")+str(data.day)+mes_extenso+"-de-"+str(data.year)+".ghtml"
    return link

def busca_resumo(sopa)
    res = soup.find('main').find('div', attrs={'class': 'mc-article-body'}).find('div', attrs={'class': 'mc-column content-text active-extra-styles active-capital-letter'})#.find('p')
    return res
# Inicialização de variáveis


lista = list()
resumos = []
relevantes = []
hoje = date.today()
data_fim = date(2017,2,1)
date2 = hoje.strftime("%d/%m/%Y")     #formato da data na URL
date3 = hoje - timedelta(days=1)
date4 = date3.strftime("%d/%m/%Y")
date9 = date(2018,1,3)                         #cópia
date10 = date9.strftime("%d/%m/%Y")
date_new_format = date(2018,7,18)
date_old_format = date(2018,4,20)
dia = ""
mes = ""
ano = ""
contador = 0
feriados = holidays.Brazil()
feriados.append(date(2018,4,30))

#Inicia Browser
driver = webdriver.Chrome()
driver.get("https://g1.globo.com/resumo-do-dia/")

#Loop
while date9 > date(2017,2,1):
    if date9.weekday() < 5 and date9 not in feriados:
        dia = dia_da_semana(date9.weekday())
        mes = mes_por_extenso(date9.month)
        if date9 > date_new_format:
            link = gera_link(date9,mes,dia)
        elif date9 > date_old_format:
            link = gera_link2(date9,mes,dia)
        else:
            link = gera_link3(date9,mes,dia)
        driver.get(link)
        encontrado = True
        time.sleep(1)
        soup=BeautifulSoup(driver.page_source)                #Pega todo o código fonte
        
        try:
            resumo = busca_resumo(soup)
        except AttributeError:
            link = gera_link3(date9,mes,dia)
            driver.get(link)
            soup=BeautifulSoup(driver.page_source)
            try:
                resumo = busca_resumo(soup)
            except AttributeError: 
                link = gera_link2(date9,mes,dia)
                driver.get(link)
                soup=BeautifulSoup(driver.page_source)
                try:
                    resumo = busca_resumo(soup)
                except AttributeError:
                    link = gera_link4(date9,mes,dia)
                    driver.get(link)
                    soup=BeautifulSoup(driver.page_source)
                    try:
                        resumo = busca_resumo(soup)
                    except AttributeError:
                        encontrado = False
                        
                
        
        try:
            resumo2 = resumo.text
        except AttributeError:
            encontrado = False
        if encontrado:
            resumos.append(date9)
            resumos.append(resumo2)
            
            
    
       
    date9 = date9 - timedelta(days=1)     #avança/retorna 1 dia
    date10 = date9.strftime("%d/%m/%Y")

dj =np.array(resumos)

size = int(len(dj)/2)
dk = dj.reshape(size,2)

df2 = pd.DataFrame(dk)

#print(df2)
df2.to_csv('noticias17.csv') 
