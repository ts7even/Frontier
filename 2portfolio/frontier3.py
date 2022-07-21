import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import scipy.optimize as sco
from scipy.optimize import minimize
from pt_tickers import tickers3

# This is the SCIPY Optimization

appended_data = pd.DataFrame()
for t in tickers3:
    stock_info = yf.Ticker(f'{t}').history(period='5y',interval='1d')
    close = stock_info['Close']
    df = pd.DataFrame({f'{t}': close})
    appended_data = pd.concat([appended_data,df],axis=1)


# Statistics
risk_free_rate = 0.0298
returns = appended_data.pct_change()
mean_returns = returns.mean()
cov_matrix = returns.cov()

# Log Returns Statistics\
log_return = np.log(appended_data/appended_data.shift(1))
mean_log_returns = log_return.mean()
Sigma = log_return.cov()


# Efficent Markowiz Frontier with SciPy | Not working right now
rMin = 0.02
def negativeSR(w):
    # w = np.array(w)
    # R = np.sum(mean_log_returns*w)
    # V = np.sqrt(np.dot(w.T,np.dot(Sigma, w)))
    # SR = R/V
    return np.sqrt(np.dot(w.T,np.dot(Sigma, w)))


def checkMinimumReq(w):
    RHS = rMin - np.sum(mean_log_returns*w)
    return RHS

def CheckSumToOne(w):
    return np.sum(w) - 1


# size = len(mean_log_returns)
w0 = np.array([0.05882,0.05882,0.05882,0.05882,0.05882,0.05882,0.05882,0.05882,0.05882,0.05882,0.05882,0.05882,0.05882,0.05882,0.05882,0.05882,0.05882])
bounds = ((0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1))
constraints = ({'type': 'eq', 'fun':checkMinimumReq}, {'type': 'eq', 'fun':CheckSumToOne})
w_opt = minimize(negativeSR,w0,method='SLSQP',bounds=bounds,constraints=constraints)
tens = w_opt.x
print(tens)