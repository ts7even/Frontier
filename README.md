# Frontier Project

## Navigation
- [FINANCE.md](FINANCE.md) - This the table of contents to show all finance concepts used in the Frontier project and its mathematical and theoretical components. 
- [1screener](#Stock-Screener) - This folder is the beta, capm, alpha capm (Alpha Adjusted), and sharpe/sortino ratio for each individual stock in the SP500 index. 
- [2portfolio](#Portfolio-Efficient-Frontier) - This folder is a simulated portfolio (Efficient Frontier) that shows optimal weights in the portfolio including same stats from [1screener]. Currently working on a forward looking model using the Black-Litterman approach to portoflio allocation. 
- [3factorModels](#Fama-French-5-Factor-Model) - This folder is the Fama French 5 factor model that replaces the CAPM. It is a multi-varate regression and expected return of assets.
- [4DeepLearning](#deep-learning-weight-optimization) - This folder consits of weight optimization with tensorflow. The goal of the deep learning weight optimization is to find
hidden correlation that mean-variance, critical line algorithm (CLA), hierarchical risk parity (HRP), cannot explain with historical & quasi random number returns.
- [5ValueAtRisk](#value-at-risk) - This folder show the VAR with ```2portfolio``` can have at any given moment. 
- [rust_frontier](#rust-implementation) - This is a Rust implementation with all concepts above. 


### Stock Screener 
- All stocks in S&P500 with each tickers stats
- Can include other stocks but will make program too slow. This is one reason why it will be implemented in rust


### Portfolio Efficient Frontier
- This is my active portfolio which optimize and allocates certain weights to each asset to reach max sharpe ratio. 
- In [2portfolio](2portfolio) you will find [pt_summary](2portfolio/pt_summary.py) which is the primary code that I'm working on. 


### Fama French 5 Factor Model 
- This is the python fama french 5 factor model that is written in python. 
- Visit [FF5](http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html) to learn more about the FF5 model.
- The file location is in [source/multifactor](source/multifactor) but is too large to commit to github


### Deep Learning Weight Optimization
- Mean Varaiance
- Critical Line Algorithm
- Hierarchical Risk Parity
- Black-Litterman Allocation (BLA)
- Deep Learning Alocation (Random and Historical) 


### Value at Risk
- How much potential loss a portfolio can assume throught out the year & at any given moment. 


### Rust Implementation
- (Work in Progress)



###  Dependencies for Python
```
pandas
numpy
scipy
matplotlib
seaborn
pytorch torch.quasirandom.SobolEngine
yfinance
tensorflow
quantl
statsmodels
```
###  Dependencies for Rust
```
[dependencies]
tensorflow = "0.18.0"
mimalloc = { version = "*", default-features = false }
```
