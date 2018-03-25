# Sharp Ratio study

Sharp Ratio is defined as stock gain normalized with stock volatility. People use Sharp Ratio to select stocks have high gains, but low  volatility. 

The project tries to address whether Sharp ratio calculated from 6 years of data can be used to predict stock performance in the following 5 years based on the sharp ratio.  

Sharpe ratio = (Mean portfolio return − Risk-free rate)/Standard deviation of portfolio return. 

Risk-free rate equals to 1-year treasury rate of the year, which has been almost zero during last 10 years. It is set to zero in this study.  

DSR (daily sharpe ratio)
DSR =  Average stock['Daily Return'] / standard deviation of stock['Daily Return']

ASR (annual sharp ratio) =  sqrt(252) * DSR 

252 is used as there are 252 trading days per year.   
 
18 stocks were selected from QQQ index (Nasdaq 100 index) and analyzed over 11 year period (2007-01-01 to 2017-12-31).   Each
stock will have 11 sharp ratio numbers corresponding to each of 11 years. Based on average ASR from the first 6 years (2007-2012), I 
created two groups, one has low average ASR (0.260) and the other has high average ASR (0.894).  Then, I calculated average 
ASR of the same two groups in the following 5 years (2013-2017).  Average ASRs of two groups showed very little difference (0.998 vs 0.950, p = 0.777).  This suggests ASR is not good for predicting future ASR. 

I will expand the analysis to study more stocks.    

