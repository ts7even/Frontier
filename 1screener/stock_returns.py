import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import statsmodels.formula.api as smf
import statsmodels.api as sm
from sp_tickers import tickers



def stock_prices():
    appended_data = []

    for t in tickers:
    
        stock_info = yf.Ticker(f'{t}').history(period='1y',interval='1wk')
    
        close = stock_info['Close']

        df = pd.DataFrame({f'{t}': close})
        appended_data.append(df)
    
    appended_data = pd.concat(appended_data, axis=1).dropna()
    appended_data.rename(columns={'^GSPC': 'SP50'}, inplace=True)
    sp_ret = appended_data.pct_change(1)
    appended_data.to_csv('source/data_screener/sp_prices.csv')
    sp_ret.to_csv('source/data_screener/sp_returns.csv')
    print(sp_ret.round(4))



def regression_stats():
    df1 = pd.read_csv('source/data_screener/sp_returns.csv')
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
    tdf.columns = ['Beta', 'Alpha', 'StderrA', 'StderrB']
    tdf.to_csv('source/data_screener/sp_regression.csv')
    print(tdf.round(5))

# stock_prices()
regression_stats()  
