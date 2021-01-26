# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Import libraries
import yfinance as yf
import pandas as pd
import numpy as np


# get tickers
ticker = pd.read_csv('./Data/tickerNum.csv', index_col = 0)

tick = ticker['Symbol'].tolist()

# get stock data from Yahoo Finance API -> yfinance


test_hist = yf.download(tick[0],period='5y')
test_hist['return'] = (test_hist['Adj Close'] - test_hist['Adj Close'].shift(1))/test_hist['Adj Close'].shift(1)


test_hist2 = yf.download(tick[1],period='5y')
test_hist2['return'] = (test_hist2['Adj Close'] - test_hist2['Adj Close'].shift(1))/test_hist2['Adj Close'].shift(1)

test_hist2.to_csv('./return_test2',index=True)

test_hist3 = yf.download(tick[2],period='5y')
test_hist3['return'] = (test_hist3['Adj Close'] - test_hist3['Adj Close'].shift(1))/test_hist3['Adj Close'].shift(1)


#Sharpe function attempt

returns = pd.DataFrame({'Return1': test_hist['return'],
                        'Return2': test_hist2['return'],
                        'Return3': test_hist3['return']})
Cov = Returns.cov()
weights = np.asarray([.33,.33,.33])

def sharpe_calc(returns,weights):
    mean_returns = returns.mean()
    portfolio_return = round(np.sum(mean_returns * weights) * 252,2)
    portfolio_std_dev = round(np.sqrt(np.dot(weights.T,np.dot(Cov, weights))) * np.sqrt(252),2)
    sharpe = portfolio_return/portfolio_std_dev
    return sharpe

sharpe_calc(returns,weights)
