#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:21:56 2021

@author: wesley
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import Code.utilityFunc as uf

import Code.geneticAlg as ga
import Code.dataUpdate as du

# get returns data
returns, rfr = du.updateData()
# split training and test i.e. 
# run genetic alg. on 4 years and see how it does in the 5th year
returns_train = returns[:'2020-01-23']
returns_test = returns['2020-01-24':]
# genetic alg 
portf, weights, sharpe, bestVal = ga.geneticAlg(returns_train, rfr, gen = 100)

# Best portfolio from genetic alg.
bestPortf = sharpe.loc[sharpe['ratio'].idxmax()]
stocks = portf[bestPortf['keys'][0]].columns.tolist()
    
# ^GSPC S&P 500 index 
gspcReturns = round(returns_train['^GSPC'].mean() * 252,2)
gspcStd = round(returns_train['^GSPC'].std() * np.sqrt(252),2)
#pf_std_dev = round(np.sqrt(np.dot(list_wt,np.dot(returns.cov(), list_wt))) * np.sqrt(252),2)
gspcsharpe = (gspcReturns - rfr)/gspcStd

# FAANG
faangCol = ['FB','AMZN', 'AAPL', 'NFLX', 'GOOG']
faangDF = returns_train.loc[:,faangCol]
faangSh = uf.sharpe_calc(faangDF, [0.2,0.2,0.2,0.2,0.2], rfr)

# plot sharpe ratios
plt.plot(bestVal['gen'],bestVal['ratio'], label='Genetic Alg.')
plt.axhline(y=gspcsharpe, color='g', linestyle='-', label='^GSPC')
plt.axhline(y=faangSh, color='r', linestyle='-', label='FAANG')
plt.title('Sharpe Ratio Growth Over Generations')
plt.xlabel('Number of Generations')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.savefig('./graphics/sharpeVs.png', dpi=150)

# =============================================================================
# 
# =============================================================================

# calculate how much you would make by investing 
# $10,000 - 1 year ago (1/24/21 - 1/24/20)
# assume you can buy fractions of stocks
# adjusted closed stock data
adjClose = pd.read_csv('./data/adjClose.csv', index_col = 0)
# 1 year ish
adjClose = adjClose['2020-01-24':'2021-01-24']

# Best portfolio variables called: stocks and weights
gspcMoney = adjClose.loc[:,['^GSPC']]
faangMoney = adjClose.loc[:,faangCol]
bestPFMoney = adjClose.loc[:,stocks]

# nominal return investment
gspcRe = round((10000/gspcMoney.iloc[0,0]) * gspcMoney.iloc[-1,0], 2)

faangRe = 0
for i in range(len(faangMoney.columns)):
    faangRe += round((2000/faangMoney.iloc[0,i]) * faangMoney.iloc[-1,i], 2)

bestPFRe = 0
weights = weights[bestPortf['keys'][1]]
moneyWeight = [x * 10000 for x in weights]
for i in range(len(bestPFMoney.columns)):
    bestPFRe += round((moneyWeight[i]/bestPFMoney.iloc[0,i]) * bestPFMoney.iloc[-1,i], 2)

# return money
money = [10000, gspcRe, faangRe, bestPFRe]
names = ['Initial', 'GSPC', 'FAANG', 'Genetic Alg.']
plt.bar(names,money)
plt.title('1 Year Return')
plt.ylabel('Dollars ($)')
plt.tight_layout()
plt.savefig('./graphics/moneyReturn.png', dpi=150)






