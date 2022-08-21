import pandas as pd
import numpy as np 
from scipy.stats import norm # Normal Distribution


# Variables 
r = 0.01  # Risk-Free Rate
S = 30   # Underline asset price
K = 40   # Strike Price
T = 240/365 # Time to Expiration 
sigma = 0.30 # Volatility aka Risk
Type = input("Type 'Call' or 'Put' for European Option Type: ")

# cdf is the cumulative distribution function
# pdf is the probability distribution function


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



def delta(r, S, K, T, sigma, Type): # Rate of change of the option value with respect to the underline asset price. 
    "Calculate Delta for a call or put european option"

    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/ (sigma*np.sqrt(T))
    try: 
        if Type == "Call":
            delta = norm.cdf(d1, 0, 1)
        elif Type == "Put":
            delta = -norm.cdf(-d1, 0, 1)
        return delta
    except:
        print("Make sure you type in 'Call' or 'Put' (Case Sensitive) ")


def gamma(r, S, K, T, sigma, Type): # Rate of change of Delta value with respect to the underline asset price. 
    "Calculate Gamma for a call or put european option"

    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/ (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try: 
        gamma = S*norm.pdf(d1, 0, 1)/(S*sigma*np.sqrt(T))
        return gamma
    except:
        print("Make sure you type in 'Call' or 'Put' (Case Sensitive) ")


def vegas(r, S, K, T, sigma, Type): # Vega measures the sensitivity to volatility. Derivative of the option value to derivative to option volatility
    "Calculate Gamma for a call or put european option"

    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/ (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try: 
        vegas = S*norm.pdf(d1, 0, 1)*np.sqrt(T)
        return vegas*0.01
    except:
        print("Make sure you type in 'Call' or 'Put' (Case Sensitive) ")



def theta(r, S, K, T, sigma, Type): # Sensitivity of the value of the derivative to the passage of time per day
    "Calculate Delta for a call or put european option"
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/ (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try: 
        if Type == "Call":
            theta = -S*norm.pdf(d1, 0, 1)*sigma/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*norm.cdf(d2, 0, 1)
        elif Type == "Put":
            theta = -S*norm.pdf(d1, 0, 1)*sigma/(2*np.sqrt(T)) + r*K*np.exp(-r*T)*norm.cdf(-d2, 0, 1)
        return theta/365
    except:
        print("Make sure you type in 'Call' or 'Put' (Case Sensitive)")


def rho(r, S, K, T, sigma, Type): # Sensitivity to the interest rate 
    "Calculate Delta for a call or put european option"
    d1 = (np.log(S/K) + (r + sigma**2/2)*T)/ (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try: 
        if Type == "Call":
            rho = K*T*np.exp(-r*T)*norm.cdf(d2, 0, 1)
        elif Type == "Put":
            rho = -K*T*np.exp(-r*T)*norm.cdf(-d2, 0, 1)
        return rho*0.01
    except:
        print("Make sure you type in 'Call' or 'Put' (Case Sensitive)")

optionPrice = blackScholes(r, S, K, T, sigma, Type).round(2)
delta_calc = delta(r, S, K, T, sigma, Type).round(3)
gamma_calc = gamma(r, S, K, T, sigma, Type).round(3)  
vega_calc = vegas(r, S, K, T, sigma, Type).round(3)
theta_calc = theta(r, S, K, T, sigma, Type).round(3)
rho_calc = rho(r, S, K, T, sigma, Type).round(3)
print(f"Option Price is: {optionPrice} ")
print(f"Delta: {delta_calc} ") 
print(f"Gamma: {gamma_calc} ") 
print(f"Vega: {vega_calc} ") 
print(f"Theta: {theta_calc} ") 
print(f"Rho: {rho_calc} ") 