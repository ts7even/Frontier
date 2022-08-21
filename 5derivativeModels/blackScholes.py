import pandas as pd
import numpy as np 
from scipy.stats import norm # Normal Distribution


# Variables 
r = 0.0286  # Risk-Free Rate
S = 36.78   # Underline asset price
K = 40.00   # Strike Price
T = 240/365 # Time to Expiration Also is the numerator 252 or 365 for options?
sigma = 0.25 # Volatility aka Risk
Type = input("Type 'Call' or 'Put' for Option Type: ")


def blackScholes(r, S, K, T, sigma, Type):
    "Calculate Black Scholes option price for a call or put european option"

    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/ (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try: 
        if Type == "Call":
            price = S*norm.cdf(d1, 0, 1) - K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
        elif Type == "Put":
            price = K*np.exp(-r*T)*norm.cdf(-d2, 0, 1) - S*norm.cdf(-d1, 0, 1)
        return price
    except:
        print("Make sure you type in 'Call' or 'Put' (Case Sensitive) ")

optionPrice = blackScholes(r, S, K, T, sigma, Type).round(2)   

print(f"Option Price is: {optionPrice} ") 