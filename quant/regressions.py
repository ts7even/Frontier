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
df.rename(columns={'^GSPC': 'SP50'})

def regression_stats():
    regress_append = []

    for t in tickers:
        model = smf.ols(f'{t} ~ SP50', data=df).fit()
        beta = model.params['SP50']
        alpha = model.params['Intercept']
        std_error = model.bse['Intercept']

        
        res = pd.DataFrame({f'{t} Beta': beta,
                            f'{t} Alpha': alpha,
                            f'{t} ASTDE': std_error
                            },index=[0])
        
        regress_append.append(res)

    total_df = pd.concat(regress_append,axis=1)
    print(total_df)

regression_stats()    