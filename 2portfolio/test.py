import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import statsmodels.formula.api as smf
import statsmodels.api as sm
from pt_tickers import tickers
from pt_tickers import tickers2
from pt_tickers import tickers3
'''This is a rewrite of Summary to make it better.'''

appended_data = pd.DataFrame()
for t in tickers:
    stock_info = yf.Ticker(f'{t}').history(period='5y',interval='1d')
    close = stock_info['Close']
    df = pd.DataFrame({f'{t}': close})
    appended_data = pd.concat([appended_data,df],axis=1)
    
    appended_data.rename(columns={'^GSPC':'SP50'}, inplace=True)
    pt_ret = appended_data.pct_change()[1:]
    pt_log = np.log(appended_data/appended_data.shift(1))
    

# Log Returns 
logReturn = np.log(appended_data/appended_data.shift(1))
annualLogReturns = ((1+logReturn).prod())**(252/len(logReturn)) -1
Sigma = logReturn.cov()*252
#Number of Assets 
num_assets = len(tickers3)
    
# Market Statistics
riskFreeRate = 0.0298
marketReturn = 0.10
marketRiskPremium = (marketReturn-riskFreeRate)
def regression_stats():
    df1 = logReturn

    total_df = pd.DataFrame()
    for t in tickers2:
        model = smf.ols(f'{t} ~ SP50', data=df1).fit()
        beta = model.params['SP50']
        alpha = model.params['Intercept']
        std_errorA = model.bse['Intercept']
        std_errorB = model.bse['SP50']
        resBeta = pd.DataFrame({f'{t}': [beta] })
        resAlpha = pd.DataFrame({f'{t}': [alpha]})
        resStderrA = pd.DataFrame({f'{t}': [std_errorA]})
        resStderrB = pd.DataFrame({f'{t}': [std_errorB]})
        df_con = pd.concat([resBeta, resAlpha, resStderrA, resStderrB],axis=0)
        total_df = pd.concat([total_df, df_con],axis=1)

    tdf = total_df.transpose()
    tdf.columns = ['Beta', 'Alpha', 'StderrA', 'StderrB']

    # Other Calculations
    capm = ((riskFreeRate + tdf['Beta'])*(marketRiskPremium))
    adjCapm = ((riskFreeRate + tdf['Alpha'] +tdf['Beta'])*(marketRiskPremium))
    stats = pd.DataFrame({
        'AnnLogReturns': annualLogReturns,
        'CAPM': capm,
        'ADJ CAPM': adjCapm,
    })
    qdf = pd.concat([tdf, stats],axis=1)
    qdf.index.name = 'Tickers'
    qdf.reset_index(drop=False, inplace=True)
    qdf.to_csv('source/data_portfolio/pt_summary.csv')
    print(qdf.round(5))
regression_stats()

