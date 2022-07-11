import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import statsmodels.formula.api as smf
import statsmodels.api as sm
from pt_tickers import tickers
from pt_tickers import tickers2

df1 = pd.read_csv('source/data_portfolio/Stats_Summary.csv')

print(df1)