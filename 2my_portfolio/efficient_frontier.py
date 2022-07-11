import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import statsmodels.formula.api as smf
import statsmodels.api as sm

from pt_tickers import tickers
from pt_tickers import tickers2



df1 = pd.read_csv('source/data_portfolio/Stats_Summary.csv')
df1 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')] # Remove this when you fix optimal weights in summary
df2 = pd.read_csv('source/data_portfolio/pt_returns.csv')
#print(df1)



coVar = df2.cov()*52
weights = df1['Weights']
returns = df2.mean(numeric_only=True) # NUmeric only true means that ignore strings in columns

port_return = np.sum(returns.mean() * weights)*52
port_var = np.dot(weights.T, np.dot(coVar, weights)) # Calculation of 2D array
port_vol = np.sqrt(port_var)
sharpe = port_return/port_vol
# print(port_var)
# print(port_vol)
# print(returns)
print(port_return)
print(sharpe)
