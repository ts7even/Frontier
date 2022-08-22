import pandas as pd
import numpy as np 
from functools import wraps
from time import time


""" Arbitrage
Type 1: Zero Cost investment 
Type 2: Cost Investment

    * American Call Option: You dont want to excercise early unless you have to (When negative interest when borrowing rates, Dividends, and uncertainty)
    * American Call Option can be valued using black-scholes if no dividends
    * Put Option: You want to excercise early

"""



"Law of One Price: When Portfolio A and Portfolio B are equal at the Start."


# One Period Binomial Model 
# S0 = Two posible outcomes stock goes up and stock goes down.


# Paramaters 
S0 = 95        # Initial Stock Price
K = 100         # Strike Price
T = 1           # Time to Maturity in years
r = 0.06        # Annual Risk Free Rate
N = 3          # Number of Time Steps | How many nodes in the Binomial Model?
u = 1.1         # Up-factor in Binomial model 
d = 1/u         # Downfactor recombing tree
Type = 'Put'    # Call or Put Option



def binomial_american_tree(K, T, S0, r, N, u, d, Type):
    dt = T/N
    q = (np.exp(r*dt) -d)/(u-d)
    disc = np.exp(-r*dt)

    # Prices at Maturity
    S = S0 * d**(np.arange(N, -1, -1)) * u**(np.arange(0, N+1, 1))

    # Option Payoff
    if Type == 'Put':
        C = np.maximum(0, K - S)
    else:
        C = np.maximum(0, S - K)

    # Backwards Recursion through the Tree 
    for i in np.arange(N-1,-1,-1):
        S = S0 * d**(np.arange(i, -1, -1)) * u**(np.arange(0, i+1, 1))
        C[:i+1] = disc * (q*C[1:i+2] + (1-q)*C[0:i+1])
        C = C[:-1]
        if Type == 'Put':
            C = np.maximum(C, K - S)
        else:
            C = np.maximum(C, S - K)
    return C[0]

put_option_price = binomial_american_tree(K, T, S0, r, N, u, d, Type)    
print(f"Binomial Option Price:\n{put_option_price}")