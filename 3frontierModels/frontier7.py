import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import scipy.optimize as sco
from scipy.optimize import minimize
from pt_tickers import tickers3
# from pypfopt import EfficientFrontier
# from pypfopt import risk_models
# from pypfopt import expected_returns

''' This is the PyPortOptimization Method for Mean Varainace CLA, and HMA
- CLA: Is the Critical Line Algo

'''

appended_data = pd.DataFrame()
for t in tickers3:
    stock_info = yf.Ticker(f'{t}').history(period='5y',interval='1d')
    close = stock_info['Close']
    df = pd.DataFrame({f'{t}': close})
    appended_data = pd.concat([appended_data,df],axis=1)

# Statistics
risk_free_rate = 0.0298
returns = appended_data.pct_change()[1:]
mean_returns = returns.mean()
cov_matrix = returns.cov()*252
annualize_return = ((1+returns).prod())**(252/len(returns)) -1


# Log Returns Statistics\
log_return = np.log(appended_data/appended_data.shift(1))[1:]
mean_log_returns = log_return.mean()
Sigma = log_return.cov()*252
annulizedLogReturn = ((1+log_return).prod())**(252/len(log_return)) -1

e = np.ones(len(annulizedLogReturn))


# Definig the investable Universe (Inverese of Covariance)
icov = np.linalg.inv(Sigma)
h = np.matmul(e, icov)
g = np.matmul(annulizedLogReturn, icov)
a = np.sum(e*h)
b = np.sum(annulizedLogReturn*h)
c = np.sum(annulizedLogReturn*g) # Quandratic Return 
d = a*c - b**2


# Minumum Variance and Tangency Portfolio
mvp = h/a
mvp_return = b/a
mvp_risk = (1/a)**(1/2)

tangency = g/b # Give weights of the portfolio
tangency_return = c/b
tangency_risk = c**(1/2)/b

print(mvp)