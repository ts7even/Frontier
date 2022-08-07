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
print(df2)

risk_free_rate = df2['RF'].mean()
market_premium = df2['Mkt-RF'].mean()
size_premium = df2['SMB'].mean()
value_premium = df2['HML'].mean()
robust_and_weak_profitability = df2['RMW'].mean()
investment_conservative_minus_agressive = df2['CMA'].mean()


# For the Returns, Probabily need to calculate the excess returns by subtracting the risk free rate.
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
        print(model.summary(title=f'{t}'))
        int_coef = pd.DataFrame({f'{t}':model.params})
        ff5_df = pd.concat([ff5_df, int_coef], axis=1)
    ff5_result = ff5_df.transpose()
    return ff5_result


def ff5_expectedReturn():
    ff5_er = multiRegression()
    five_factor_er = (((risk_free_rate + ff5_er['Mkt-RF'])*market_premium) + 
    (ff5_er['SMB']*size_premium) + (ff5_er['HML']*value_premium) + (ff5_er['RMW']*robust_and_weak_profitability) + 
    (ff5_er['CMA']*investment_conservative_minus_agressive))**(252/(len(df4)))
    print(five_factor_er)

ff5_expectedReturn()

