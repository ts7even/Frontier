import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import statsmodels.formula.api as smf
import statsmodels.api as sm
import scipy.optimize as minimize

from pt_tickers import tickers
from pt_tickers import tickers2

# Port Optimization Lograngian Function

df1 = pd.read_csv('source/data_portfolio/Stats_Summary.csv')
df2 = pd.read_csv('source/data_portfolio/pt_returns.csv')

print(df1)

rfr = 0.0312
size = len(df1)
coVar = df2.cov()*52
weights = df1['Weights']
returns = df1['Ann Returns'] # NUmeric only true means that ignore strings in columns

port_return = np.sum(returns.mean() * weights) # Returns are already annualized.
port_var = np.dot(weights.T, np.dot(coVar, weights)) # Calculation of 2D array
port_vol = np.sqrt(port_var)
sharpe = ((port_return-rfr)/port_vol)
port_beta = (df1['Beta'].sum()/size)

# print(f'Portfolio Variance: {port_var}')
# print(f'Porfolio Volatility: {port_vol}')
# print(f'Porfolio Return: {port_return}')
# print(f'Portfolio Sharpe Ratio: {sharpe}')
# print(f'Portfolio Beta: {port_beta-0.01}')


rMin = 0.02

def riskFunction(port_var):
    return port_var

toup_bounds = (0,1)
bounds =((toup_bounds, )*size)

def checkMinimumReturn(weights):
    rMin - np.sum(returns*weights)
    return RHS

def checkSumToOne(weights):    
    return np.sum(weights) -1




constraints = ({'type':'eq', 'fun': checkMinimumReturn}, {'type':'eq', 'fun': checkSumToOne})
w_opt = minimize(riskFunction, weights, method='SLSQP',bounds=bounds,constraints=constraints)

w_scipy = w_opt.x
print(w_scipy)