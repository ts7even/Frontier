import pandas as pd
import numpy as np 
import yfinance as yf
import json

tickers = json.loads(open('criteria\s&p_tickers.json').read())


def stock_prices():
    # Current Price
    stock_info = yf.Ticker('AAPL').info
    # current_price = stock_info.get('currentPrice')
    historical_price = stock_info.history()
    print(historical_price)


stock_prices()