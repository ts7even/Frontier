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


# df3 = df1.rename(columns={0:'Beta', 0.1:'Alpha', 0.2:'STDERR'})
# df3.drop(index=df3.index[0], axis=0, inplace=True)

 
def regres_criteria():
    positive_alpha = df1[(df1['Alpha']>=0.001)]
    negative_alpha = df1[(df1['Alpha']<=0.000)]
    print(negative_alpha)
    

regres_criteria()    
