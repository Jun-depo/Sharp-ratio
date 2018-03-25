
# coding: utf-8

# Sharp Ratio is defined as stock gain normalized with stock volatility. People use Sharp Ratio to select stocks have high gains, but low volatility.
# 
# The project tries to address whether Sharp ratio calculated from 6 years of data can be used to predict stock performance in the following 5 years based on the sharp ratio. 
# 
# 18 stocks were selected from Nasdaq 100 index and analyzed in this sproject over 11 year period of time (2007-01-01 to 2017-12-31). 

# In[2]:


import pandas as pd


# In[3]:


import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import quandl


# In[4]:


# This file contains 2014-06-09 split-adjustment.  
aapl=pd.read_csv('aapl.csv')


# In[5]:


aapl.head()


# In[6]:


#qqq19 contains first 19 stocks (based on alphabetic order) (obtained sev)
qqq19 = ["ATVI", "ADBE", "ALXN", "ALGN", "GOOGL", "GOOG", "AMZN", "AAL", "AMGN", "ADI", 
       "AMAT", "ADSK", "ADP", "BIDU", "BIIB", "BMRN", "AVGO", "CA", "AAPL"]
qqq19_wiki = []

for i in qqq19:
    a = "WIKI/"+i
    qqq19_wiki.append(a)
qqq19_wiki


# In[7]:


#'WIKI/ATVI' is the format used by quandl to ATVI stock data.  


# In[8]:


# need to input API key to run the code.  
dd ={}
for i in qqq19_wiki:
    dd[i] = quandl.get(i, start_date='2007-01-01',end_date='2018-01-01', api_key='put your API key')


# In[9]:


dd.keys()


# In[10]:


nam = []
for i in qqq19:
    nam.append(i.lower())
nam


# In[11]:


### Save as csv files, don't have to import data from Quandl every time running the code.    
for i in range(19):
    dd[qqq19_wiki[i]].to_csv(nam[i]+'.csv')


# In[12]:


dict ={}

for i in range(19):
    dict[nam[i]] = pd.read_csv(nam[i]+'.csv', index_col='Date')
    


# In[13]:


print(nam[0], nam[18])


# In[17]:


# dict[nam[0]]['Close'] contains closing price data of atvi
data18 = dict[nam[0]]['Close']
data18.tail()


# In[18]:


# concatenate the closing stock price data for all 19 stocks
for i in range(1,19):
    data18 = pd.concat([data18, dict[nam[i]]['Close']], axis=1)


# In[19]:


# change column names to corresponding stock names 
data18.columns = [ 
 'atvi',
 'adbe',
 'alxn',
 'algn',
 'googl',
 'goog',
 'amzn',
 'aal',
 'amgn',
 'adi',
 'amat',
 'adsk',
 'adp',
 'bidu',
 'biib',
 'bmrn',
 'avgo',
 'ca', 'aapl']


# In[20]:


data18.head()


# In[21]:


data18.plot(figsize=(12, 10))
# The plot showes GOOGL, AAPL and BIDU containing sharp drops of stock prices, likely due to stock splits.  
#The stock prices need to be split-adjusted. 


# In[22]:


# 1 GOOGL stock becomes 1 GOOGL plus GOOG on '2014-03-27', distributed on '2014-04-03'

data18[data18.index > '2014-03-31'].head(5)


# In[23]:


# Need to adjust googl price prior to '2014-04-03'. Compare googl price on '2014-04-02' and '2014-04-03' 


# In[24]:


# Try to do the adjustment outside the whole dataframe. So if something goes wrong, it would not affect 
# the whole dataframe. 
googl = data18['googl']
googl.head()


# In[25]:


googl[googl.index < '2014-04-03'] = googl[googl.index < '2014-04-03'] / 2


# In[26]:


googl[googl.index < '2014-04-03'].tail()
# The split adjustment seems to be correct.


# In[27]:


# assigned the adjustment into the whole dataframe
data18.loc[(data18.index < '2014-04-03'),'googl'] = googl[googl.index < '2014-04-03']


# In[28]:


data18[data18.index < '2014-04-08']['googl'].tail()
# data prior to '2014-04-03' got adjusted.  


# In[29]:


# 'goog' price more less mirrors 'googl' price. The column will be dropped. 
data18.drop('goog', inplace=True, axis=1)


# In[30]:


data18.head(2)


# In[31]:


aapl = data18['aapl']


# In[32]:


# 2014-06-06 was the last trading before 1-to-7 split
aapl[aapl.index < '2014-06-07'] = aapl[aapl.index < '2014-06-07'] / 7


# In[33]:


aapl.plot()
# appl prices are split-adjusted.


# In[34]:


# Assign the split into the dataframe data18
data18.loc[(data18.index < '2014-06-07'),'aapl'] = aapl[aapl.index < '2014-06-07']


# In[35]:


data18.head(2)


# In[36]:


data18['aapl'] = data18['aapl'].round(2)


# In[37]:


data18.head(2)


# In[38]:


# BIDU had 1 to 10 stock split on 2010-05-12.  Prices prior to 2010-05-12 need to be adjusted by 1/10.
data18[data18.index > '2010-05-09' ]['bidu'].head()


# In[39]:


data18.loc[(data18.index < '2010-05-12'),'bidu'] = data18.loc[(data18.index < '2010-05-12'),'bidu'] / 10


# In[40]:


data18[data18.index > '2010-05-09' ]['bidu'].head()
# prices were adjusted.


# In[41]:


data18['bidu'] = data18['bidu'].round(2)


# In[42]:


data18.head(2)


# In[43]:


stocks18 = ['atvi',
 'adbe',
 'alxn',
 'algn',
 'googl',
 'amzn',
 'aal',
 'amgn',
 'adi',
 'amat',
 'adsk',
 'adp',
 'bidu',
 'biib',
 'bmrn',
 'avgo',
 'ca',
 'aapl']
# matching column names of data18


# In[44]:


data18.info()
# There are 2768 index (datetime) entries.  Some columns contain less than 2768 non-null values,
# suggesting missing values in the data set 


# In[45]:


# check if any null values in the data set. atvi, adbe, amzn, bidu, aapl contain one missing value on '2017-08-07'
data18[data18['aapl'].isnull()]


# In[46]:


data18[(data18.index) > '2017-08-03'].head(3)


# In[47]:


# From Yahoo Finance, AMZN close price was 992.27 on 2017-08-07
data18.loc[data18['aapl'].isnull(), 'amzn'] = 992.27


# In[48]:


data18[(data18.index) > '2017-08-03'].head(3)
#amzn price is corrected on 2017-08-07


# In[49]:


# more corrections for NaN values on 2017-08-07
data18.loc[data18['aapl'].isnull(), 'atvi'] = 62.51
data18.loc[data18['aapl'].isnull(), 'adbe'] = 148.44
data18.loc[data18['aapl'].isnull(), 'bidu'] = 227.16
data18.loc[data18['aapl'].isnull(), 'aapl'] = 158.81


# In[50]:


data18[(data18.index) > '2017-08-03'].head(3)


# In[51]:


# Daily return = price of that day - price of the prvious date. The raw will be NaN, due no price data 
# on the previous date. Built in function pct_change(1) was used to calculate the daily return. 
# "1" in pct_change(1) indictes 1 previous data point   
data18['atvi daily return'] = data18['atvi'].pct_change(1)


# In[52]:


# atvi daily return column displays correct result
data18.head()


# In[53]:


# avgo contains many missing values, due the stock was IPO in 2009 as shown in the plot below.
data18['avgo'].plot(figsize=(12, 6))


# In[54]:


# Create dataframe for daily return data of the stocks.
data_day_ret = pd.DataFrame({'A':[]})
for i in data18.columns:
    data_day_ret[i+' day_ret'] = data18[i].pct_change(1)


# In[55]:


#remove 'A" from the DataFrame 
data_day_ret.drop('A', axis=1, inplace=True)


# In[57]:


data_day_ret.info()


# In[58]:


data_day_ret.head(3)


# In[59]:


# Remove the last column 'atvi daily return day_ret' due to it was added earlier, it becomes daily change 
# of atvi daily return. The correct atvi daily return is in the first column as 'atvi day_ret' 
data_day_ret.drop('atvi daily return day_ret', axis=1, inplace=True)


# In[60]:


data_day_ret.head(3)


# In[61]:


# Calculating average 2007 daily return.  The first row null values were excluded through datetime index selection
data_day_ret[(data_day_ret.index > '2007-01-03') & (data_day_ret.index < '2008-01-01')].mean(axis=0)


# In[64]:


# Sharp Ratio (SR) = mean of daily return / std of daily return 
# SR2007 is Sharp Ratio for 2007.
m2007 = data_day_ret[(data_day_ret.index > '2007-01-03') & (data_day_ret.index < '2008-01-01')].mean(axis=0)
std2007 = data_day_ret[(data_day_ret.index > '2007-01-03') & (data_day_ret.index > '2008-01-01')].std(axis=0)
SR2007 =  m2007/std2007    


# In[65]:


# Annualized Sharp Ratio of 2007. 252 is the number of trading days per year.
ASR2007 = (252**0.5)*SR2007


# In[66]:


ASR2007


# In[71]:


## creating a dictionary which contains annualized sharp ratio data
ASR = {}
years = ['2007-01-03', '2008-01-01', '2009-01-01', '2010-01-01', '2011-01-01', '2012-01-01', '2013-01-01', 
         '2014-01-01', '2015-01-01', '2016-01-01', '2017-01-01', '2018-01-01']

for i in range(11):
    ASR[i] = (252**0.5)* data_day_ret[(data_day_ret.index > years[i]) & (data_day_ret.index < years[i+1])].mean(axis=0)/data_day_ret[(data_day_ret.index > years[i]) & (data_day_ret.index < years[i+1])].std(axis=0) 
    # 252^0.5 X each year daily return / std of each year daily return (inside forloop)  


# In[72]:


ASR


# In[73]:


# convert the dictionary to pandas dataframe
ASR_df = pd.DataFrame(ASR)


# In[74]:


# Assign column names
ASR_df.columns = ['2007 ASR', '2008 ASR', '2009 ASR', '2010 ASR', '2011 ASR', '2012 ASR', '2013 ASR', '2014 ASR',
      '2015 ASR', '2016 ASR', '2017 ASR']


# In[75]:


ASR_df.reset_index()


# In[76]:


ASR_df['stock name'] = ['atvi',
 'adbe',
 'alxn',
 'algn',
 'googl',
 'amzn',
 'aal',
 'amgn',
 'adi',
 'amat',
 'adsk',
 'adp',
 'bidu',
 'biib',
 'bmrn',
 'avgo',
 'ca',
 'aapl']


# In[77]:


ASR_df.set_index('stock name', inplace=True)


# In[78]:


ASR_df.to_csv('qqq18_ab.csv', encoding="UTF-8")


# In[79]:


ASR_df


# In[80]:


ASR_df['ASR mean'] = ASR_df.mean(axis=1)


# In[81]:


ASR_df['ASR std'] = ASR_df.std(axis=1)


# In[82]:


ASR_df


# In[83]:


ASR_df2 = ASR_df.transpose()


# In[84]:


ASR_df2.to_csv('qqq18_ab_tran.csv', encoding="UTF-8")


# In[85]:


ASR_df2


# In[86]:


ASR_df2.plot(figsize=(12, 9))
# ASR values have no obvious organized pattern. 


# In[87]:


ASR_df2.sort_values(by='ASR mean', axis=1)
# 'ASR mean' is in the second last row, sorted in the ascending order from the left to the right.


# In[91]:


# plotting ASR of ca, aal, amgn 
ASR_df2.loc[['2007 ASR', '2008 ASR', '2009 ASR', '2010 ASR', '2011 ASR', '2012 ASR', '2013 ASR', '2014 ASR',
      '2015 ASR', '2016 ASR', '2017 ASR'], ['ca', 'aal', 'amgn']].plot(figsize=(12, 9))
plt.ylabel('Annual Sharp Ratio (ASR)', fontsize=12)


# In[92]:


# plotting ASR of amzn, aapl, avgo 
ASR_df2.loc[['2007 ASR', '2008 ASR', '2009 ASR', '2010 ASR', '2011 ASR', '2012 ASR', '2013 ASR', '2014 ASR',
      '2015 ASR', '2016 ASR', '2017 ASR'], ['amzn', 'aapl', 'avgo']].plot(figsize=(12, 9))
plt.ylabel('Annual Sharp Ratio (ASR)', fontsize=12)


# In[93]:


ASR_df2.reset_index()


# In[94]:


fir6year_ave = ASR_df2.iloc[0:6].mean(axis=0)


# In[95]:


last5year_ave = ASR_df2.iloc[6:11].mean(axis=0)


# In[96]:


fir6year_ave.plot.bar(figsize=(8,6), fontsize=13)
plt.xlabel('Stock names', fontsize=14)
plt.ylabel('Annual Sharp Ratio (ASR)', fontsize=14)
plt.title('Average Annual Sharp Ratio from 2007-2012')
plt.tight_layout()


# In[97]:


last5year_ave.plot.bar(figsize=(8,6), fontsize=13)
plt.xlabel('Stock names', fontsize=14)
plt.ylabel('Annual Sharp Ratio (ASR)', fontsize=14)
plt.title('Average Annual Sharp Ratio from 2013-2017')
plt.tight_layout()


# In[98]:


import seaborn as sns


# In[112]:


# data points aren't not following clear linear pattern
plt.scatter(x=fir6year_ave, y=last5year_ave)
plt.xlabel('Average ASR from 2007-2012')
plt.ylabel('Average ASR from 2013-2017')


# In[113]:


fir6year_ave.sort_values()


# In[114]:


sort_by_first6 = fir6year_ave.sort_values()


# In[115]:


sort_by_first6 = pd.concat([sort_by_first6,last5year_ave], axis=1, join='inner')


# In[116]:


sort_by_first6.columns = ['2007-2012 ASR', '2013-2017 ASR']


# In[117]:


sort_by_first6


# In[118]:


sort_by_first6.iloc[0:9]['2007-2012 ASR']


# In[134]:


sort_by_first6.iloc[0:9]['2007-2012 ASR'].mean()


# In[135]:


sort_by_first6.iloc[9:18]['2007-2012 ASR'].mean()


# In[139]:


sort_by_first6.iloc[0:9]['2013-2017 ASR'].mean()


# In[140]:


sort_by_first6.iloc[9:18]['2013-2017 ASR'].mean()


# In[146]:


plt.figure(figsize=(12, 6))
sns.boxplot(data=[sort_by_first6.iloc[0:9]['2007-2012 ASR'],sort_by_first6.iloc[9:18]['2007-2012 ASR'], sort_by_first6.iloc[0:9]['2013-2017 ASR'], 
                   sort_by_first6.iloc[9:18]['2013-2017 ASR']], orient='v', width=0.6)
plt.xticks(range(4), ("lower 9 ASR during 2007-2012","higher 9 ASR during 2007-2012", "lower 9 ASR during 2013-2017", "higher 9 ASR during 2013-2017"))
plt.ylabel('ASR', fontsize=14)
plt.title('The relationship between ASR performance in Year 07-12 and ASR performance in Year 13-17')
plt.tight_layout()

# ASR values of low performers (group1) and high performers (group2) are rather diffferent during 2007-2012

# The difference between 2 groups during 2013-2017 is very small, suggesting that selecting stocks 
# sharp ratio is not good indicator for the future stock performance.       


# In[147]:


from scipy import stats


# In[150]:


stats.ttest_ind(sort_by_first6.iloc[0:9]['2007-2012 ASR'],sort_by_first6.iloc[9:18]['2007-2012 ASR'],equal_var=False )
# The difference between low ASR and high ASR group in 2007-2012 is very significant statistically (p=1.44 X10^-5).   


# In[151]:


stats.ttest_ind(sort_by_first6.iloc[0:9]['2013-2017 ASR'],sort_by_first6.iloc[9:18]['2013-2017 ASR'], equal_var=False)
# The difference in average ASR of The two groups are statistically insignificant (p=0.777)

