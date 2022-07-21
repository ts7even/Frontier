import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import scipy.optimize as sco
from scipy.optimize import minimize
from pt_tickers import tickers3


# lograngian function | Doesnt Work Well

appended_data = []
for t in tickers3:
    stock_info = yf.Ticker(f'{t}').history(start='2022-07-07', end='2022-07-20',interval='1d')
    close = stock_info['Close']
    df = pd.DataFrame({f'{t}': close})
    appended_data.append(df)
appended_data = pd.concat(appended_data, axis=1).dropna()


# Statistics
risk_free_rate = 0.0298
returns = appended_data.pct_change()
mean_returns = returns.mean()
cov_matrix = returns.cov()

# Log Returns Statistics\
log_return = np.log(appended_data/appended_data.shift(1))
mean_log_returns = log_return.mean()
pBar = mean_log_returns
Sigma = log_return.cov()


rMin = 0.02
def Markowiz(rMin, Sigma, pBar):
    N = len(Sigma)
    o = np.ones(N)
    SigmaInv = np.linalg.inv(Sigma)
    a = np.dot(pBar.T,np.dot(SigmaInv, pBar))
    b = np.dot(pBar.T,np.dot(SigmaInv, o))
    c = np.dot(o.T,np.dot(SigmaInv, o))
    return (1/(a*c - b**2)) * np.dot(SigmaInv,((c*rMin - b)*pBar + (a-b*rMin)*o))
opt_weights = Markowiz(rMin, Sigma, pBar)
print(opt_weights)
