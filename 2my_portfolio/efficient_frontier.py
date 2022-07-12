import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import statsmodels.formula.api as smf
import statsmodels.api as sm
import scipy.optimize as optimize

from pt_tickers import tickers
from pt_tickers import tickers2



df1 = pd.read_csv('source/data_portfolio/Stats_Summary.csv')
df2 = pd.read_csv('source/data_portfolio/pt_returns.csv')

print(df1)

size = len(df1)
coVar = df2.cov()*52
weights = df1['Weights']
returns = df1['Ann Returns'] # NUmeric only true means that ignore strings in columns

port_return = np.sum(returns.mean() * weights) # Returns are already annualized.
port_var = np.dot(weights.T, np.dot(coVar, weights)) # Calculation of 2D array
port_vol = np.sqrt(port_var)
sharpe = port_return/port_vol
port_beta = (df1['Beta'].sum()/size)

print(f'Portfolio Variance: {port_var}')
print(f'Porfolio Volatility: {port_vol}')
print(f'Porfolio Return: {port_return}')
print(f'Portfolio Sharpe Ratio: {sharpe}')
print(f'Portfolio Beta: {port_beta-0.01}')


