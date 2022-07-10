from statistics import stdev
import pandas as pd
import numpy as np 
import scipy as sp 
import statsmodels.formula.api as smf
import statsmodels.api as sm
import seaborn as sns
from datetime import timedelta, datetime
from sp_tickers import tickers





df1 = pd.read_csv('source/data_screener/sp_returns.csv')
def regression_stats():

    total_df = pd.DataFrame()

    for t in tickers:
        model = smf.ols(f'{t} ~ SP50', data=df1).fit()
        beta = model.params['SP50']
        alpha = model.params['Intercept']
        std_errorA = model.bse['Intercept']
        std_errorB = model.bse['SP50']
        

        resBeta = pd.DataFrame({f'{t}': beta },index=[0])
        resAlpha = pd.DataFrame({f'{t}': alpha},index=[0])
        resStderrA = pd.DataFrame({f'{t}': std_errorA},index=[0])
        resStderrB = pd.DataFrame({f'{t}': std_errorB},index=[0])

        df_con = pd.concat([resBeta, resAlpha, resStderrA, resStderrB],axis=0)
        total_df = pd.concat([total_df, df_con],axis=1)

    tdf = total_df.transpose()
    # df3 = tdf.rename(columns={0:'Beta', 1:'Alpha', 2:'STDERR'})
    tdf.columns = ['Beta', 'Alpha', 'StderrA', 'StderrB']
    tdf.to_csv('source/data_screener/sp_regression.csv')
    print(tdf.round(5))


regression_stats()  