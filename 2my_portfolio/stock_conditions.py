import pandas as pd
import numpy as np 
import scipy as sp


''' 
All Stock Have to meet the criteria of

1. Positive Cashflows
2. Strong Financials (Reinvestment Rate, ROI ect from Aswath)
3. Company in good position (Max Debt to Equity Ratio) Finacially Solvent
4. Has to have a positive alpha potential in a regression.
5. Good Indicators such as EPS, PE, EV/EBITDA, compared to its competitors and industry
6. No Stock that is over 10% of portfolio.
7. Know something that others dont. 
8. Quantify Everything. 
9. No dying industries in portfolio. Like coal mines
10. No Derivatives ultil you know how to price them. 
'''


df1 = pd.read_csv('source/data/sp_regression.csv') # Regression
df2 = pd.read_csv('source/data/sp_returns.csv') # Returns

df1.rename(columns={ 'Unnamed: 0': 'Ticker'}, inplace=True)


 
def regres_criteria():
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

    


    positive_alpha = df1[(df1['Alpha']>=0.001) & (df1['Sharpe'] >=3)]
    print(positive_alpha.round(5))
    df1.to_csv('source/data/Stats_Summary.csv')

regres_criteria()    
