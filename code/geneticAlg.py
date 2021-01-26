#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 19:55:32 2021

@author: wesley
"""
    
# genetic algorithm

import random
import pandas as pd
import numpy as np
import code.children as ch
import code.utilityFunc as uf

# # adjusted closed stock data
# adjClose = pd.read_csv('../data/adjClose.csv', index_col = 0)
# # calculate the return rate
# returns = (adjClose - adjClose.shift(1))/adjClose.shift(1)
# returns = returns.iloc[1:] # drop the na row made by the shift

# # use t-bill for risk-free rate
# # https://www.federalreserve.gov/data.htm
# tbill = pd.read_csv('../data/t_bill.csv', index_col = 0)
# tbill.columns = ['rate']
# rfr = tbill['rate'].mean()/100
    
def geneticAlg(returns, rfr, gen = 20, pop = 240, mrate = 0.2, randSeed = 0):    
    # initial population
    # randomly pick the stocks for the portfolio and percent to spend on each
    # kids is the number of initial population and will be used to 
    #   assign id to each portfolio
    portfs, weights, kids = uf.pickPfWt(returns, pop, randSeed) 
    # calculate sharpe ratio for each portfolio
    sharpe = pd.DataFrame()
    for key, key2 in zip(portfs, weights):
        sharpe = sharpe.append({'keys':[key,key2],'ratio':uf.sharpe_calc(portfs[key], weights[key2], rfr)},
                      ignore_index=True)
    # best sharpe ratio value
    shmax = sharpe.loc[sharpe['ratio'].idxmax()]
    print('Generation: 0')
    print('Best sharpe ratio: ' + str(shmax['ratio']))
    # save best values for analysis
    bestVal = pd.DataFrame()
    mean_returns = portfs[shmax['keys'][0]].mean()
    list_wt = weights[shmax['keys'][1]]
    max_return = round(np.sum(mean_returns * list_wt) * 252,2)
    bestVal = bestVal.append({'gen':0, 'ratio':shmax['ratio'], 
                              'returns':max_return},ignore_index=True)
    # generations
    generation = gen
    while generation > 0:
        # select mating pool based on threshold fitness
        # sort by biggest sharpe ratio with top 50th percentile surviving
        sharpe = sharpe.sort_values('ratio')
        fail = sharpe.iloc[:int(pop/2),:]
        # delete failing portfolios
        #   using my_dict.pop('key', None) can be faster
        for key in fail['keys']:
            if key[0] in portfs:
                del portfs[key[0]]
            if key[1] in weights:
                del weights[key[1]]
        # pair the parents
        key_list = list(portfs.keys())
        key_num = [item for subitem in key_list for item in subitem.split('_') if item.isdigit()]
        random.seed(777)
        random.shuffle(key_num)
        it = iter(key_num)
        # children
        for parent in it:
            parent2 = next(it)
            wt1, wt2 = ch.crossover_wt(weights['w_%s' % parent], 
                                       weights['w_%s' % parent2])
            pf1, pf2, wt1, wt2 = ch.crossover_pf(portfs['pf_%s' % parent], 
                                                 portfs['pf_%s' % parent2],
                                                 returns, kids, mrate, wt1, wt2)
            portfs['pf_%s' % kids] = pf1
            portfs['pf_%s' % (kids + 1)] = pf2
            weights['w_%s' % kids] = wt1
            weights['w_%s' % (kids + 1)] = wt2
            kids += 2
        # generation end
        generation -= 1
        # calculate sharpe ratio for each portfolio to find best
        sharpe = pd.DataFrame()
        for key, key2 in zip(portfs, weights):
            sharpe = sharpe.append({'keys':[key,key2],'ratio':uf.sharpe_calc(portfs[key], weights[key2], rfr)},
                          ignore_index=True)
        # best sharpe ratio value
        shmax = sharpe.loc[sharpe['ratio'].idxmax()]
        print('Generation: ' + str(gen - generation))
        print('Best sharpe ratio: ' + str(shmax['ratio']))
        # save best values for analysis
        mean_returns = portfs[shmax['keys'][0]].mean()
        list_wt = weights[shmax['keys'][1]]
        max_return = round(np.sum(mean_returns * list_wt) * 252,2)
        bestVal = bestVal.append({'gen':gen-generation, 'ratio':shmax['ratio'], 
                                  'returns':max_return},ignore_index=True)

    return portfs, weights, sharpe, bestVal

        

#testdf, testwt, testsh, testbv = geneticAlg(returns, rfr, gen = 100)







