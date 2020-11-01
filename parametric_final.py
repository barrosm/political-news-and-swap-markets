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

def vol_to_csd(fitted_model):
    CSD = np.sqrt(fitted_model.conditional_volatility)
    return CSD

def parametric_min_value(CSD_array):
    min_value = CSD_array.mean()-(2*CSD_array.std())
    return min_value

def parametric_max_value(CSD_array):
    max_value = CSD_array.mean()+(2*CSD_array.std())
    return max_value

def non_parametric_max_value(CSD_array):
    nonpar_max_value = np.percentile(CSD_array,95)
    return nonpar_max_value

def new_dataframe(CSD_array, maximum_value):
    df_csd = pd.DataFrame(CSD_array)
    df_csd.index = datas
    out_of_interval = df_csd[df_csd > maximum_value]
    return out_of_interval


# Main

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

# Apply and fit models

fitted_dixpre30 = fit_model(apply_model(dixpre30))
fitted_dixpre60 = fit_model(apply_model(dixpre60))
fitted_dixpre90 = fit_model(apply_model(dixpre90))
fitted_dixpre180 = fit_model(apply_model(dixpre180))

fitted_dolxpre30 = fit_model(apply_model(dolxpre30))
fitted_dolxpre60 = fit_model(apply_model(dolxpre60))
fitted_dolxpre90 = fit_model(apply_model(dolxpre90))
fitted_dolxpre180 = fit_model(apply_model(dolxpre180))

fitted_dixdol30 = fit_model(apply_model(dixdol30))
fitted_dixdol60 = fit_model(apply_model(dixdol60))
fitted_dixdol90 = fit_model(apply_model(dixdol90))
fitted_dixdol180 = fit_model(apply_model(dixdol180))

fitted_dixipca30 = fit_model(apply_model(dixipca30))

# Calculate Conditional Standard Deviances

csd_dixpre30 = vol_to_csd(fitted_dixpre30)
csd_dixpre60 = vol_to_csd(fitted_dixpre60)
csd_dixpre90 = vol_to_csd(fitted_dixpre90)
csd_dixpre180 = vol_to_csd(fitted_dixpre180)

csd_dolxpre30 = vol_to_csd(fitted_dolxpre30)
csd_dolxpre60 = vol_to_csd(fitted_dolxpre60)
csd_dolxpre90 = vol_to_csd(fitted_dolxpre90)
csd_dolxpre180 = vol_to_csd(fitted_dolxpre180)

csd_dixdol30 = vol_to_csd(fitted_dixdol30)
csd_dixdol60 = vol_to_csd(fitted_dixdol60)
csd_dixdol90 = vol_to_csd(fitted_dixdol90)
csd_dixdol180 = vol_to_csd(fitted_dixdol180)

csd_dixipca30 = vol_to_csd(fitted_dixipca30)

#Out of Interval 

newDIxPre = pd.DataFrame(index = datas)
newDolxPre = pd.DataFrame(index = datas)
newDIxDol = pd.DataFrame(index = datas)
newDIxIPCA = pd.DataFrame(index = datas)


newDIxPre['30'] = new_dataframe(csd_dixpre30, parametric_max_value(csd_dixpre30))
newDIxPre['60'] = new_dataframe(csd_dixpre60, parametric_max_value(csd_dixpre60))
newDIxPre['90'] = new_dataframe(csd_dixpre90, parametric_max_value(csd_dixpre90))
newDIxPre['180'] = new_dataframe(csd_dixpre180, parametric_max_value(csd_dixpre180))

newDolxPre['30'] = new_dataframe(csd_dolxpre30, parametric_max_value(csd_dolxpre30))
newDolxPre['60'] = new_dataframe(csd_dolxpre60, parametric_max_value(csd_dolxpre60))
newDolxPre['90'] = new_dataframe(csd_dolxpre90, parametric_max_value(csd_dolxpre90))
newDolxPre['180'] = new_dataframe(csd_dolxpre180, parametric_max_value(csd_dolxpre180))

newDIxDol['30'] = new_dataframe(csd_dixdol30, parametric_max_value(csd_dixdol30))
newDIxDol['60'] = new_dataframe(csd_dixdol60, parametric_max_value(csd_dixdol60))
newDIxDol['90'] = new_dataframe(csd_dixdol90, parametric_max_value(csd_dixdol90))
newDIxDol['180'] = new_dataframe(csd_dixdol180, parametric_max_value(csd_dixdol180))

newDIxIPCA['30'] = new_dataframe(csd_dixipca30, parametric_max_value(csd_dixipca30))

#Export to new CSV

newDIxPre.to_csv("DIxPre_Parametric.csv")
newDolxPre.to_csv("DolxPre_Parametric.csv")
newDIxDol.to_csv("DIxDol_Parametric.csv")
newDIxIPCA.to_csv("DIxIPCA_Parametric.csv")

# Initialize Charts
fig = plt.figure(constrained_layout=True, figsize = (10,6))    
spec = gridspec.GridSpec(ncols=2, nrows=2, figure=fig)
f_ax1 = fig.add_subplot(spec[0, 0])
f_ax2 = fig.add_subplot(spec[0, 1])
f_ax3 = fig.add_subplot(spec[1, 0])
f_ax4 = fig.add_subplot(spec[1, 1])
    
fig2 = plt.figure(constrained_layout=True, figsize = (10,6))    
spec2 = gridspec.GridSpec(ncols=2, nrows=2, figure=fig2)
f2_ax1 = fig2.add_subplot(spec2[0, 0])
f2_ax2 = fig2.add_subplot(spec2[0, 1])
f2_ax3 = fig2.add_subplot(spec2[1, 0])
f2_ax4 = fig2.add_subplot(spec2[1, 1])

fig3 = plt.figure(constrained_layout=True, figsize = (10,6))
spec3 = gridspec.GridSpec(ncols=2, nrows=2, figure=fig3)
f3_ax1 = fig3.add_subplot(spec3[0, 0])
f3_ax2 = fig3.add_subplot(spec3[0, 1])
f3_ax3 = fig3.add_subplot(spec3[1, 0])
f3_ax4 = fig3.add_subplot(spec3[1, 1]) 
    
fig4 = plt.figure(constrained_layout=True, figsize = (10,6))
spec4 = gridspec.GridSpec(ncols=2, nrows=2, figure=fig4)
f4_ax1 = fig4.add_subplot(spec4[0, 0])
f4_ax2 = fig4.add_subplot(spec4[0, 1])
f4_ax3 = fig4.add_subplot(spec4[1, 0])
f4_ax4 = fig4.add_subplot(spec4[1, 1]) 

# Plot Charts

# DI x Pre
csd_dixpre30.plot(ax=f_ax1, title = 'DI x Pre Variation 30 days CSD')
csd_dixpre60.plot(ax=f_ax2, color = 'red', title = 'DI x Pre Variation 60 days CSD')
csd_dixpre90.plot(ax=f_ax3, color = 'green', title = 'DI x Pre Variation 90 days CSD')
csd_dixpre180.plot(ax=f_ax4, color = 'black', title = 'DI x Variation 180 days CSD')

f_ax1.axhline(parametric_min_value(csd_dixpre30), ls= '--')
f_ax1.axhline(parametric_max_value(csd_dixpre30), ls= '--')
f_ax1.axhline(csd_dixpre30.mean(), ls= 'dotted')

f_ax2.axhline(parametric_min_value(csd_dixpre60), ls= '--')
f_ax2.axhline(parametric_max_value(csd_dixpre60), ls= '--')
f_ax2.axhline(csd_dixpre60.mean(), ls= 'dotted')

f_ax3.axhline(parametric_min_value(csd_dixpre90), ls= '--')
f_ax3.axhline(parametric_max_value(csd_dixpre90), ls= '--')
f_ax3.axhline(csd_dixpre90.mean(), ls= 'dotted')

f_ax4.axhline(parametric_min_value(csd_dixpre180), ls= '--')
f_ax4.axhline(parametric_max_value(csd_dixpre180), ls= '--')
f_ax4.axhline(csd_dixpre180.mean(), ls= 'dotted')


# Dol x Pre

csd_dolxpre30.plot(ax=f2_ax1, title = 'Dollar x Pre 30 days CSD')
csd_dolxpre60.plot(ax=f2_ax2, color = 'red', title = 'Dollar x Pre 60 days CSD')
csd_dolxpre90.plot(ax=f2_ax3, color = 'green', title = 'Dollar x Pre 90 days CSD')
csd_dolxpre180.plot(ax=f2_ax4, color = 'black', title = 'Dollar x 180 days CSD')

f2_ax1.axhline(parametric_min_value(csd_dolxpre30), ls= '--')
f2_ax1.axhline(parametric_max_value(csd_dolxpre30), ls= '--')
f2_ax1.axhline(csd_dolxpre30.mean(), ls= 'dotted')

f2_ax2.axhline(parametric_min_value(csd_dolxpre60), ls= '--')
f2_ax2.axhline(parametric_max_value(csd_dolxpre60), ls= '--')
f2_ax2.axhline(csd_dolxpre60.mean(), ls= 'dotted')

f2_ax3.axhline(parametric_min_value(csd_dolxpre90), ls= '--')
f2_ax3.axhline(parametric_max_value(csd_dolxpre90), ls= '--')
f2_ax3.axhline(csd_dolxpre90.mean(), ls= 'dotted')

f2_ax4.axhline(parametric_min_value(csd_dolxpre180), ls= '--')
f2_ax4.axhline(parametric_max_value(csd_dolxpre180), ls= '--')
f2_ax4.axhline(csd_dolxpre180.mean(), ls= 'dotted')

# DI x Dollar
csd_dixdol30.plot(ax=f3_ax1, title = 'DI x Dollar 30 days CSD')
csd_dixdol60.plot(ax=f3_ax2, color = 'red', title = 'DI x Dollar 60 days CSD')
csd_dixdol90.plot(ax=f3_ax3, color = 'green', title = 'DI x Dollar 90 days CSD')
csd_dixdol180.plot(ax=f3_ax4, color = 'black', title = 'DI x Dollar 180 days CSD')

f3_ax1.axhline(parametric_min_value(csd_dixdol30), ls= '--')
f3_ax1.axhline(parametric_max_value(csd_dixdol30), ls= '--')
f3_ax1.axhline(csd_dixdol30.mean(), ls= 'dotted')

f3_ax2.axhline(parametric_min_value(csd_dixdol60), ls= '--')
f3_ax2.axhline(parametric_max_value(csd_dixdol60), ls= '--')
f3_ax2.axhline(csd_dixdol60.mean(), ls= 'dotted')

f3_ax3.axhline(parametric_min_value(csd_dixdol90), ls= '--')
f3_ax3.axhline(parametric_max_value(csd_dixdol90), ls= '--')
f3_ax3.axhline(csd_dixdol90.mean(), ls= 'dotted')

f3_ax4.axhline(parametric_min_value(csd_dixdol180), ls= '--')
f3_ax4.axhline(parametric_max_value(csd_dixdol180), ls= '--')
f3_ax4.axhline(csd_dixdol180.mean(), ls= 'dotted')

# DI x Ipca
csd_dixipca30.plot(ax=f4_ax1, title = 'DI x IPCA 30 days CSD')
f4_ax1.axhline(parametric_min_value(csd_dixipca30), ls= '--')
f4_ax1.axhline(parametric_max_value(csd_dixipca30), ls= '--')
f4_ax1.axhline(csd_dixipca30.mean(), ls= 'dotted')

# Save Output

fig.savefig('parametric_results_DIxPRE.png')
fig2.savefig('parametric_results_DOLxPRE.png')
fig3.savefig('parametric_results_DIxDOL.png')
fig4.savefig('parametric_results_DIxIPCA.png')
