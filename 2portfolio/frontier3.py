import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import scipy.optimize as sco
from scipy.optimize import minimize
from pt_tickers import tickers3










# This is the SciPy Optimization

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