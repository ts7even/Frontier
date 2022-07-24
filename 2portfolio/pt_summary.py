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
    print(qdf.round(5))
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
    bound = (0.018,0.0826)
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
    bound = (0.018,0.0826)
    bounds = tuple(bound for asset in range(num_assets))

    result = sco.minimize(portfolio_volatility, num_assets*[1./num_assets,], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)

    return result

def efficient_return(meanLogReurns, Sigma, target):
    num_assets = len(meanLogReurns)
    args = (meanLogReurns, Sigma)

    def portfolio_return(weights):
        return portfolio_annualised_performance(weights, meanLogReurns, Sigma)[1]

    constraints = ({'type': 'eq', 'fun': lambda x: portfolio_return(x) - target},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0,1) for asset in range(num_assets))
    result = sco.minimize(portfolio_volatility, num_assets*[1./num_assets,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    return result


def efficient_frontier(meanLogReurns, Sigma, returns_range):
    efficients = []
    for ret in returns_range:
        efficients.append(efficient_return(meanLogReurns, Sigma, ret))
    return efficients


def display_ef_with_selected(meanLogReurns, Sigma, riskFreeRate):
    max_sharpe = max_sharpe_ratio(meanLogReurns, Sigma, riskFreeRate)
    sdp, rp = portfolio_annualised_performance(max_sharpe['x'], meanLogReurns, Sigma)
    max_sharpe_allocation = pd.DataFrame(max_sharpe.x,index=appended_data.columns,columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i*100,2)for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T
    

    min_vol = min_variance(meanLogReurns, Sigma)
    sdp_min, rp_min = portfolio_annualised_performance(min_vol['x'], meanLogReurns, Sigma)
    min_vol_allocation = pd.DataFrame(min_vol.x,index=appended_data.columns,columns=['allocation'])
    min_vol_allocation.allocation = [round(i*100,2)for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T
    
    an_vol = np.std(logReturn) * np.sqrt(252)
    an_rt = meanLogReurns * 252
    
    print ("-"*80)
    print ("Maximum Sharpe Ratio Portfolio Allocation\n")
    print ("Annualised Return:", round(rp,2))
    print ("Annualised Volatility:", round(sdp,2))
    print ("\n")
    print (max_sharpe_allocation)
    print ("-"*80)
    print ("Minimum Volatility Portfolio Allocation\n")
    print ("Annualised Return:", round(rp_min,2))
    print ("Annualised Volatility:", round(sdp_min,2))
    print ("\n")
    print (min_vol_allocation)
    print ("-"*80)
    print ("Individual Stock Returns and Volatility\n")
    for i, txt in enumerate(appended_data.columns):
        print (txt,":","annuaised return",round(an_rt[i],2),", annualised volatility:",round(an_vol[i],2))
    print ("-"*80)
    

display_ef_with_selected(annualLogReturns, Sigma, riskFreeRate)


