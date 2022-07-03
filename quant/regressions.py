from statistics import stdev
import pandas as pd
import numpy as np 
import scipy as sp 
import statsmodels.formula.api as smf
import statsmodels.api as sm
import seaborn as sns
from datetime import timedelta, datetime
from sp_tickers2 import tickers


df = pd.read_csv('source/data/sp_returns.csv')
df1 = df.rename(columns={'^GSPC': 'SP50'})

def regression_stats():

    total_df = pd.DataFrame()

    for t in tickers:
        model = smf.ols(f'{t} ~ SP50', data=df1).fit()
        ticker = (f'{t}')
        beta = model.params['SP50']
        alpha = model.params['Intercept']
        std_error = model.bse['Intercept']

        resBeta = pd.DataFrame({f'{t}': beta },index=[0])
        resAlpha = pd.DataFrame({f'{t}': alpha},index=[0])
        resStderr = pd.DataFrame({f'{t}': std_error},index=[0])

        df_con = pd.concat([resBeta, resAlpha, resStderr],axis=0)
        total_df = pd.concat([total_df, df_con],axis=1)

    total_df.to_csv('source/data/sp_regression.csv')
    print(total_df)

regression_stats()    