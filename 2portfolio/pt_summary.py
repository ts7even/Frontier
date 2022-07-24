import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import statsmodels.formula.api as smf
import statsmodels.api as sm
import scipy.optimize as sco
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
meanLogReurns = logReturn.mean()
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
regression_stats()



def portfolio_annualised_performance(weights, meanLogReurns, Sigma):
    returns = np.sum(meanLogReurns*weights ) *252
    std = np.sqrt(np.dot(weights.T, np.dot(Sigma, weights))) * np.sqrt(252)
    return std, returns

def neg_sharpe_ratio(weights, meanLogReurns, Sigma, riskFreeRate):
    p_var, p_ret = portfolio_annualised_performance(weights, meanLogReurns, Sigma)
    return -(p_ret - riskFreeRate) / p_var

def max_sharpe_ratio(meanLogReurns, Sigma, riskFreeRate):
    num_assets = len(meanLogReurns)
    args = (meanLogReurns, Sigma, riskFreeRate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.018,0.10)
    bounds = tuple(bound for asset in range(num_assets))
    result = sco.minimize(neg_sharpe_ratio, num_assets*[1./num_assets,], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)
    return result

def portfolio_volatility(weights, meanLogReurns, Sigma):
    return portfolio_annualised_performance(weights, meanLogReurns, Sigma)[0]

def min_variance(meanLogReurns, Sigma):
    num_assets = len(meanLogReurns)
    args = (meanLogReurns, Sigma)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.018,0.10)
    bounds = tuple(bound for asset in range(num_assets))

    result = sco.minimize(portfolio_volatility, num_assets*[1./num_assets,], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)

    return result


df1 = pd.read_csv('source/data_portfolio/pt_summary.csv', index_col=[0])

def display_ef_with_selected(meanLogReurns, Sigma, riskFreeRate):
    max_sharpe = max_sharpe_ratio(meanLogReurns, Sigma, riskFreeRate)
    max_sharpe_allocation = pd.DataFrame({"+SharpeWeight":max_sharpe.x})

    min_vol = min_variance(meanLogReurns, Sigma)
    min_vol_allocation = pd.DataFrame({'-VolWeight':min_vol.x})

    num_port = 100000
    wWeight = np.zeros((num_port,len(meanLogReurns)))
    expectedReturn = np.zeros(num_port)
    expectedVolatility = np.zeros(num_port)
    sharpeRatio = np.zeros(num_port)

    for k in range(num_port):
        # Generate random weight vector
        w = np.array(np.random.random(len(meanLogReurns)))
        w = w / np.sum(w)
        wWeight[k,:] = w
        expectedReturn[k] = np.sum((meanLogReurns * w))
        expectedVolatility[k] = np.sqrt(np.dot(w.T,np.dot(Sigma, w)))
        sharpeRatio[k] = expectedReturn[k]/expectedVolatility[k]

    maxIndex = sharpeRatio.argmax()
    lmx = wWeight[maxIndex,:]
    bruteAllocation = pd.DataFrame({'bruteAllocation': lmx})

    weight1 = pd.concat([max_sharpe_allocation, min_vol_allocation, bruteAllocation], axis=1)
    weight_allocation = pd.concat([df1,weight1], axis=1)
    weight_allocation.reset_index(drop=True, inplace=True)
    weight_allocation.to_csv('source/data_portfolio/pt_summary.csv')
    print(weight_allocation.round(5))

display_ef_with_selected(annualLogReturns, Sigma, riskFreeRate)


