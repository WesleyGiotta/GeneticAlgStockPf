#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 10:23:28 2021

@author: wesley
"""


import code.geneticAlg as ga
import code.dataUpdate as du
        
if __name__ == '__main__':
    returns, rfr = du.updateData()
    portf, weights, sharpe, bestVal = ga.geneticAlg(returns, rfr, gen = 10)
    bestPortf = sharpe.loc[sharpe['ratio'].idxmax()]
    stocks = portf[bestPortf['keys'][0]].columns.tolist()
    weights = weights[bestPortf['keys'][1]]
    for s, w in zip(stocks, weights):
        print(s, round(w, 4))
    
    
    
    
