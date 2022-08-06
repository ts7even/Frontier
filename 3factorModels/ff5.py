import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import statsmodels.formula.api as smf
import statsmodels.api as sm
from pt_tickers import tickers
from pt_tickers import tickers2
from pt_tickers import tickers3
import datetime



df1 = pd.read_csv('source/multifactor/F-F_Research_Data_5_Factors_2x3_daily.CSV')
df2 = df1[(df1['Date']>=20170703)]
df2['Date'] = pd.to_datetime(df2['Date'], format="%Y%m%d")

print(df2)

market_premium = df2['Mkt-RF']
size_premium = df2['SMB']
value_premium = df2['HML']
robust_and_weak_profitability = df2['RMW']
investment_conservative_minus_agressive = df2['CMA']

appended_data = pd.DataFrame()
for t in tickers:
    stock_info = yf.Ticker(f'{t}').history(start='2017-06-30', end='2022-07-01',interval='1d')
    close = stock_info['Close']
    df = pd.DataFrame({f'{t}': close})
    appended_data = pd.concat([appended_data,df],axis=1)
    
    appended_data.rename(columns={'^GSPC':'SP50'}, inplace=True)
    arthematic = appended_data.pct_change()[1:-1]
    df3 = pd.DataFrame(arthematic)
df4 = df2.merge(df3, on='Date')


def multiRegression():
    for t in tickers3:
        X = df4[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']]
        y = df4[f'{t}']
        X1 = sm.add_constant(X)
        model = sm.OLS(y, X1).fit()
        print(model.summary(title=f'{t}'))

        
multiRegression()
