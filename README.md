# Frontier Project

## Navigation
- [FINANCE.md](FINANCE.md) - This markdown file show all finance concepts used in the Frontier project and its mathematical and theoretical components. 
- [1screener](#Stock-Screener) - This folder is the beta, capm, alpha capm (Alpha Adjusted), and sharpe ratio for each individual stock in the SP500 index. 
- [2portfolio](#Portfolio-Efficient-Frontier) - This folder is a simulated portfolio (Efficient Frontier) that shows optimal weights in the portfolio including same stats from [1screener]. 
- [3factorModels](#Fama-French-5-Factor-Model) - This folder is the Fama French 5 factor model that replaces the CAPM. It is a multi-varate regression and expected return of assets.
- [4DeepLearning](#deep-learning-weight-optimization) - This folder consits of weight optimization with tensorflow. The goal of the deep learning weight optimization is to find
hidden correlation that mean-variance, critical line algorithm (CLA), hierarchical risk parity (HRP), and Black-Litterman Allocation (BLA) cannot explain with historical & quasi random number returns.
- [5ValueAtRisk](#value-at-risk) - This folder show the VAR with ```2portfolio``` can have at any given moment. 
- [rust_frontier](#rust-implementation) - This is a Rust implementation with all concepts above. 


### Stock Screener 
- 


### Portfolio Efficient Frontier
- This is my active portfolio and trying to optimize with Scipy Optimize and appending it to the Summary stats. 
- In ```2my_portfolio``` you will find ```pt_summary``` which is the primary code that I'm working on. 


### Fama French 5 Factor Model 


### Deep Learning Weight Optimization

### Value at Risk

### Rust Implementation




## Dependencies
pandas
numpy
scipy
matplotlib
seaborn
pytorch torch.quasirandom.SobolEngine
yfinance
tensorflow
quantl



