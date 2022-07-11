import pandas as pd
import numpy as np
import scipy as spi 
import yfinance as yf
import statsmodels.formula.api as smf
import statsmodels.api as sm
from pt_tickers import tickers
from pt_tickers import tickers2


def stock_prices():
    appended_data = []

    for t in tickers:
    
        stock_info = yf.Ticker(f'{t}').history(period='1y',interval='1wk')
    
        close = stock_info['Close']

        df = pd.DataFrame({f'{t}': close})
        appended_data.append(df)
    
    appended_data = pd.concat(appended_data, axis=1).dropna()
    appended_data.rename(columns={'^GSPC':'SP50'}, inplace=True)
    sp_ret = appended_data.pct_change(1)
    appended_data.to_csv('source/data_portfolio/pt_prices.csv')
    sp_ret.to_csv('source/data_portfolio/pt_returns.csv')
    print(sp_ret.round(4))




def regression_stats():
    df1 = pd.read_csv('source/data_portfolio/pt_returns.csv')
    total_df = pd.DataFrame()

    for t in tickers2:
        model = smf.ols(f'{t} ~ SP50', data=df1).fit()
        beta = model.params['SP50']
        alpha = model.params['Intercept']
        std_errorA = model.bse['Intercept']
        std_errorB = model.bse['SP50']
        

        resBeta = pd.DataFrame({f'{t}': beta },index=[0])
        resAlpha = pd.DataFrame({f'{t}': alpha},index=[0])
        resStderrA = pd.DataFrame({f'{t}': std_errorA},index=[0])
        resStderrB = pd.DataFrame({f'{t}': std_errorB},index=[0])

        df_con = pd.concat([resBeta, resAlpha, resStderrA, resStderrB],axis=0)
        total_df = pd.concat([total_df, df_con],axis=1)

    tdf = total_df.transpose()
    tdf.columns = ['Beta', 'Alpha', 'StderrA', 'StderrB']
    tdf.to_csv('source/data_portfolio/pt_regression.csv')
    print(tdf.round(5))


 
def regres_criteria():
    df1 = pd.read_csv('source/data_portfolio/pt_regression.csv') # Regression
    df2 = pd.read_csv('source/data_portfolio/pt_returns.csv') # Returns
    df1.rename(columns={ 'Unnamed: 0': 'Ticker'}, inplace=True)


    rf = (3.1156)/100
    cds = (26.90)/10000
    rfr = (rf-cds)
    rm = 0.08

    
    # Appending New Column Calculations
    esteleai_optimal = (df1['Alpha']/df1['StderrA'])
    df1.insert(5, 'Alpha Opt', esteleai_optimal)

    sharpe_ratio = ((df1['Alpha']+df1['Beta'] - rfr)/df1['StderrB'])
    df1.insert(6, 'Sharpe', sharpe_ratio)

    capm = ((rfr + df1['Beta'])*(rm-rfr))
    df1.insert(7, 'CAPM', capm)

    adj_capm = ((rfr + df1['Alpha'] + df1['Beta'])*(rm-rfr))
    df1.insert(8, ' ADJ_CAPM', adj_capm)

    

    # Filtering For Values
    # positive_alpha = df1[(df1['Alpha']>=0.001) & (df1['Sharpe'] >=3)]
    # print(positive_alpha.round(5))
    df1.to_csv('source/data_portfolio/Stats_Summary.csv')
    print(df1)
    

def portfolio_weights():
    # Cost of portfolio $3719.90
    df1 = pd.read_csv('source/data_portfolio/Stats_Summary.csv')

    cost = (3719.90)

    aapl_weight = df1[(df1['Ticker']=='AAPL')]
    aapl_weight = (145.78/3719.90)

    amd_weight = df1[(df1['Ticker']=='AMD')]
    amd_weight = (236.34/3719.90)

    amzn_weight = df1[(df1['Ticker']=='AMZN')]
    amzn_weight = (232.58/3719.90)

    bnd_weight = df1[(df1['Ticker']=='BND')]
    bnd_weight = (225.41/3719.90)

    crwd_weight = df1[(df1['Ticker']=='CRWD')]
    crwd_weight = (381.56/3719.90)
    
    dfac_weight = df1[(df1['Ticker']=='DFAC')]
    dfac_weight = (238.60/3719.90)

    dfas_weight = df1[(df1['Ticker']=='DFAS')]
    dfas_weight = (98.06/3719.90)

    dfus_weight = df1[(df1['Ticker']=='DFUS')]
    dfus_weight = (125.73/3719.90)

    ess_weight = df1[(df1['Ticker']=='ESS')]
    ess_weight = (267.25/3719.90)

    gs_weight = df1[(df1['Ticker']=='GS')]
    gs_weight = (295.53/3719.90)

    jpm_weight = df1[(df1['Ticker']=='JPM')]
    jpm_weight = (227.52/3719.90)

    low_weight = df1[(df1['Ticker']=='LOW')]
    low_weight = (180.94/3719.90)

    msft_weight = df1[(df1['Ticker']=='MSFT')]
    msft_weight = (267.51/3719.90)

    vea_weight = df1[(df1['Ticker']=='VEA')]
    vea_weight = (162.24/3719.90)

    vgk_weight = df1[(df1['Ticker']=='VGK')]
    vgk_weight = (156.03/3719.90)

    voo_weight = df1[(df1['Ticker']=='VOO')]
    voo_weight = (356.40/3719.90)

    vwob_weight = df1[(df1['Ticker']=='VWOB')]
    vwob_weight = (122.42/3719.90)

    sp50_weight = df1[(df1['Ticker']=='SP50')]
    sp50_weight = (0)

    weights = (aapl_weight, amd_weight, amzn_weight, bnd_weight, crwd_weight, dfac_weight,
    dfas_weight, dfus_weight, ess_weight, gs_weight, jpm_weight, low_weight, msft_weight, vea_weight, vgk_weight, voo_weight, vwob_weight, sp50_weight)
    df1.insert(10, 'Weights', weights)
    df1.to_csv('source/data_portfolio/Stats_Summary.csv')
    print(df1)
    
  
# stock_prices()
# regression_stats()
# regres_criteria()   
# portfolio_weights()