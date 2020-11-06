import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numbers
import math
import numpy as np
import scipy as sp                                                       
import scipy.stats  
import statsmodels.api as sm
from arch import arch_model
from statsmodels.stats import diagnostic
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss

def start_arrays(dataframe, maturity):
    array = dataframe[maturity]
    return array

def apply_model(array):
    model = arch_model(array, rescale = False)
    return model

def fit_model(applied_model):
    fitted = applied_model.fit()
    return fitted

def adf_test(started_array):
    resultadf = adfuller(started_array)
    print('ADF Statistic: %f' % resultadf[0])
    print('p-value: %f' % resultadf[1])
    print('Critical Values:')
    for key, value in resultadf[4].items():
        print('\t%s: %.3f' % (key, value))

    if resultadf[0] < resultadf [4]["5%"]:
            print ("ADF Stationary")
    else:
        print("ADF Non Stationary")
    

def kpss_test(started_array):
    resultkpss = kpss(started_array)
    print('kpss stats',resultkpss[0])
    print('kpss pvalue',resultkpss[1])
    print('kpss critical',resultkpss[3])
    if resultkpss[0]<resultkpss[3]['5%']:
        print("kpss stationary")
    else:
        print('kpss non stationary')
    if resultkpss[1] > 0.05:
        print('kpss stationary')
    else:
        print('kpss non stationary')
    

def ljungbox_test(fitted_model):
    print("Ljung-Box test: ", diagnostic.acorr_ljungbox(fitted_model.resid,(1,1)))
    
          
def shapiro_test(fitted_model):
    print("Shapiro-Wilk test: ", sp.stats.shapiro(fitted_model.resid))
          
          
# Read Data
df1 = pd.read_csv("dixpre_daily_variationV2.csv") 
df2 = pd.read_csv("dollarxpreV2.csv")
df3 = pd.read_csv("dixdollarV2.csv")
df4 = pd.read_csv("dixipcaV2.csv")

datas = df1['data']

# Adjust DI x Pre Values
df1['30'] = df1['30']*100
df1['60'] = df1['60']*100
df1['90'] = df1['90']*100
df1['180'] = df1['180']*100


# Start Arrays
dixpre30 = start_arrays(df1,'30')
dixpre60 = start_arrays(df1,'60')
dixpre90 = start_arrays(df1,'90')
dixpre180 = start_arrays(df1,'180')

dolxpre30 = start_arrays(df2,'30')
dolxpre60 = start_arrays(df2,'60')
dolxpre90 = start_arrays(df2,'90')
dolxpre180 = start_arrays(df2,'180')

dixdol30 = start_arrays(df3,'30')
dixdol60 = start_arrays(df3,'60')
dixdol90 = start_arrays(df3,'90')
dixdol180 = start_arrays(df3,'180')
    
dixipca30 = start_arrays(df4,'30')
          
lists = [dixpre30,dixpre60,dixpre90,dixpre180,dolxpre30,dolxpre60,dolxpre90,dolxpre180,dixdol30,dixdol60,dixdol90,dixdol180,dixipca30]
names = ["DI x Pre 30", "DI x Pre 60", "DI x Pre 90", "DI x Pre 180", "Dollar x Pre 30", "Dollar x Pre 60", "Dollar x Pre 90", "Dollar x Pre 180", "DI x Dollar 30", "DI x Dollar 60", "DI x DOllar 90", "DI x Dollar 180", "DI x IPCA 30"]

for item in range(13):
    print("***************************************************************************************")
    print("***************************************************************************************")
    print(names[item])
    modelo = fit_model(apply_model(lists[item]))
    adf_test(lists[item])
    kpss_test(lists[item])
    ljungbox_test(modelo)
    shapiro_test(modelo)
