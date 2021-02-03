#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 10:23:28 2021

@author: wesley
"""

import Code.geneticAlg as ga
import Code.dataUpdate as du
        
if __name__ == '__main__':
    returns, rfr = du.updateData()
    while True:
        x = input("How many generations?\n")
        try:
            isinstance(int(x), int) is True
        except:
            print('Please type in a whole number greater than zero.')
        else:
            x = int(x)
            break
    portf, weights, sharpe, bestVal = ga.geneticAlg(returns, rfr, gen = x)
    bestPortf = sharpe.loc[sharpe['ratio'].idxmax()]
    stocks = portf[bestPortf['keys'][0]].columns.tolist()
    weights = weights[bestPortf['keys'][1]]
    print('The stocks and weights from the best portfolio:')
    for s, w in zip(stocks, weights):
        print(s.ljust(9), round(w, 4))
    
    
    
    
