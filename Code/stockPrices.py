#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 17:46:55 2020

@author: wesley
"""

import yfinance as yf #https://pypi.org/project/yfinance/
import pandas as pd

def getStockData():
    # get tickers
    ticker = pd.read_csv('./data/tickerNum.csv', index_col = 0)
    
    tick = ticker['Symbol'].tolist()
    tick.extend(['^GSPC', 'RSP'])
    
    # get stock data from Yahoo Finance API -> yfinance
    # download adjusted closing data from yfiance 
    data = yf.download(tick, period='5y')
    
    # some ideas:
    # https://pythonforfinance.net/2019/07/02/investment-portfolio-optimisation-with-python-revisited/
    # https://pythonforfinance.net/2017/01/21/investment-portfolio-optimisation-with-python/
    # https://towardsdatascience.com/deepdow-portfolio-optimization-with-deep-learning-a3ffdf36eb00
    
    # only want adjusted closed data
    adjClose = data.iloc[:,:507]
    adjClose.to_csv('./data/adjClose.csv', index=True)
    
    returns = pd.read_csv('./data/adjClose.csv', index_col = 0)
    new_header = returns.iloc[0] #grab the first row for the header
    returns = returns[2:] #take the data less the header row
    returns.columns = new_header #set the header row as the df header
    
    # # find na all rows
    # is_NaN = returns.iloc[:,0:1].isnull()
    # row_has_NaN = is_NaN.any(axis=1)
    # rows_with_NaN = returns[row_has_NaN]
    # drop rows with all na
    returns = returns.dropna(axis=0,how='all')
    # drop columns with any na
    returns = returns.dropna(axis=1,how='any')
    
    # save data
    returns.to_csv('./data/adjClose.csv', index=True)









