import pandas as pd
import numpy as np 
import yfinance as yf
import json
import requests
import datetime
from sp_tickers import tickers




def stock_prices():
    appended_data = []

    for t in tickers:
    
        stock_info = yf.Ticker(f'{t}').history(period='1y',interval='1wk')
    
        close = stock_info['Close']

        df = pd.DataFrame({f'{t}': close})
        appended_data.append(df)
    
    appended_data = pd.concat(appended_data, axis=1)
    appended_data.to_csv('source/data/s&p_prices.csv')
    print(appended_data)

stock_prices()