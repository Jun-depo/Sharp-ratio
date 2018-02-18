# Sharp Ration Correlation study

The project tries to address whether Sharp-ratio derived from given stocks of one year can be used to predict stock 
sharp-rate of the next year .  

Sharpe ratio = (Mean portfolio return − Risk-free rate)/Standard deviation of portfolio return. 
Risk-free rate equals to 1-year treasury rate of the year.

DSR (daily sharpe ratio)
DSR =  stock['Daily Return'].mean() / stock['Daily Return'].std()
DSR doesn't contain 1-year treasury rate adjustment

ASR (annual sharp ratio) =  sqrt(252) * stock['Daily Return'].mean() - (1-year treasury rate) / stock['Daily Return'].std()
252 is used as there are 252 trading days per year
 
Initially, 20 stocks selected from QQQ will be analyzed over 11 year period (2007-01-01 to 2018-01-01).   Each stock have 
11 sharp ratio numbers corresponding to 11 year data.  Each SAR will be paired with the next year ASR of the same stock, then 
analyzed for their correlation (more detail description will be provided).  Each stock will have 10 pairs. There will be 
total 200 pairs. 

I will also use normalized sharp ratio (ASR offset by QQQ ASR or SPY ASR) to eliminate general stock market up and down.

Eventually, I will expand the analysis to more stocks.   

