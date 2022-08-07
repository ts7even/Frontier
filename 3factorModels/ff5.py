import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import statsmodels.formula.api as smf
import statsmodels.api as sm
# from sklearn.preprocessing import linear_model
from pt_tickers import tickers
from pt_tickers import tickers2
from pt_tickers import tickers3
import datetime



df1 = pd.read_csv('source/multifactor/F-F_Research_Data_5_Factors_2x3_daily.CSV')
df2 = df1[(df1['Date']>=20170703)]
df2['Date'] = pd.to_datetime(df2['Date'], format="%Y%m%d")



market_premium = df2['Mkt-RF'].mean()
size_premium = df2['SMB'].mean()
value_premium = df2['HML'].mean()
robust_and_weak_profitability = df2['RMW'].mean()
investment_conservative_minus_agressive = df2['CMA'].mean()

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
    ff5_df = pd.DataFrame()
    for t in tickers3:
        X = df4[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']]
        y = df4[f'{t}']
        X1 = sm.add_constant(X)
        model = sm.OLS(y, X1).fit()
        int_coef = model.params
    print(int_coef)
multiRegression()





# def multiRegression():
#     ff5_df = pd.DataFrame()
#     for t in tickers3:
#         X = df4[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']]
#         y = df4[f'{t}']
#         X1 = sm.add_constant(X)
#         model = sm.OLS(y, X1).fit()
#         intercept = model.params['const']
#         beta_mkrt_rf = model.params['Mkt-RF']
#         beta_smb = model.params['SMB']
#         beta_hml = model.params['HML']
#         beta_rmw = model.params['RMW']
#         beta_cma = model.params['CMA']
#         regress_data = pd.DataFrame({
#             f'{t}':[intercept],
#             f'{t}':[beta_mkrt_rf],
#             f'{t}':[beta_smb],
#             f'{t}':[beta_hml],
#             f'{t}':[beta_rmw],
#             f'{t}':[beta_cma]
#         })
#         ff5_df = pd.concat([ff5_df, regress_data], axis=1)
#     tdf = ff5_df.transpose()
#     tdf.columns = ['Intercept','Mrkt-Rf', 'SMB', 'HML', 'RMW', 'CMA']
#     print(tdf)
# multiRegression()


# def multiRegression():
#     ff5_df = pd.DataFrame()
#     for t in tickers3:
#         X = df4[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']]
#         y = df4[f'{t}']
#         X1 = sm.add_constant(X)
#         model = sm.OLS(y, X1).fit()
#         print(model.summary(title=f'{t}'))
        
# multiRegression()