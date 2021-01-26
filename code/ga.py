#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 13:46:48 2020

@author: wesley
"""

# genetic algorithm

import random
import pandas as pd
#import numpy as np
import code.children as ch
import code.utilityFunc as uf

# 1.pick initial population

# adjusted closed stock data
adjClose = pd.read_csv('../data/adjClose.csv', index_col = 0)
# calculate the return rate
returns = (adjClose - adjClose.shift(1))/adjClose.shift(1)
returns = returns.iloc[1:] # drop the na row made by the shift

# use t-bill for risk-free rate
tbill = pd.read_csv('../data/t_bill.csv', index_col = 0)
tbill.columns = ['rate']
rfr = tbill['rate'].mean()/100

# randomly pick the stocks for the portfolio and percent to spend on each
portfs, weights = uf.pickPfWt(returns)

# number the kids past the 240 originals (0-239)
kids = 240

# 2.select mating pool based on threshold fitness

# calculate sharpe ratio for each portfolio
sharpe = pd.DataFrame()
for key, key2 in zip(portfs, weights):
    sharpe = sharpe.append({'keys':[key,key2],'ratio':uf.sharpe_calc(portfs[key], weights[key2], rfr)},
                  ignore_index=True)


# sort by biggest sharpe ratio with top 50th percentile surviving
sharpe = sharpe.sort_values('ratio')
fail = sharpe.iloc[:120,:]

# delete failing portfolios
#   using my_dict.pop('key', None) can be faster
for key in fail['keys']:
    if key[0] in portfs:
        del portfs[key[0]]
    if key[1] in weights:
        del weights[key[1]]
    
# 3.a.child crossover


# loop after this part for generations

# pair the parents
key_list = list(portfs.keys())
key_num = [item for subitem in key_list for item in subitem.split('_') if item.isdigit()]
random.seed(777)
random.shuffle(key_num)
it = iter(key_num)


for parent in it:
    parent2 = next(it)
    wt1, wt2 = ch.crossover_wt(weights['w_%s' % parent], weights['w_%s' % parent2])
    pf1, pf2, wt1, wt2 = ch.crossover_pf(portfs['pf_%s' % parent], 
                                         portfs['pf_%s' % parent2],
                                         returns, kids, wt1, wt2)
    portfs['pf_%s' % kids] = pf1
    portfs['pf_%s' % (kids + 1)] = pf2
    weights['w_%s' % kids] = wt1
    weights['w_%s' % (kids + 1)] = wt2
    kids += 2


# randomize the order of the coulmns for next iteration
#   necessary b/c crossover takes first 10 percent each time
for key, key2 in zip(portfs, weights):
    # make list of column names
    pfCols = portfs[key].columns.tolist()
    print(key, len(pfCols))
    # combine lists, randomize, and separate
    c = list(zip(pfCols, weights[key2]))
    random.shuffle(c)
    pfCols, weights[key2] = zip(*c) # returns tuple, I think
    print(key, len(pfCols))
    # implement changes to columns
    portfs[key] = portfs[key].loc[:,pfCols] # issue
    print(key, len(portfs[key].columns))


# 3.b.child mutation

# for now lets only change the stock not the weights
# also only mutate half of the children
# this mutates parents too need to fix
mutate_list = list(portfs.keys())[::2]
for key in mutate_list:
    portfs[key] = ch.mutateStock(portfs[key], returns)



# randomize the order of the coulmns for next iteration
#   necessary b/c crossover takes first 10 percent each time
for key, key2 in zip(portfs, weights):
    # make list of column names
    pfCols = portfs[key].columns.tolist()
    # combine lists, randomize, and separate
    c = list(zip(pfCols, weights[key2]))
    random.shuffle(c)
    pfCols, weights[key2] = zip(*c)
    # implement changes to columns
    portfs[key] = portfs[key].loc[:,pfCols]
    
# 4.restart at 2 until stop and pick winner(s)

# pick winner
# calculate sharpe ratio for each portfolio
sharpe = pd.DataFrame()
for key, key2 in zip(portfs, weights):
    print(key,key2)
    sharpe = sharpe.append({'keys':[key,key2],'ratio':uf.sharpe_calc(portfs[key], weights[key2], rfr)},
                  ignore_index=True)
    

# sort by biggest sharpe ratio with top 50th percentile surviving
sharpe = sharpe.sort_values('ratio')
success = sharpe.iloc[120:,:]


# these should be equal if code works
def testing():
    print(len(portfs['pf_252'].columns))
    print(len(weights['w_252']))

testdf = portfs['pf_602'] # 252, 602, 683
testwt = weights['w_602']

testdf, testwt = uf.stockShuffle(testdf, testwt)

testli2 = testdf.columns.tolist()

testli = ~testdf.columns.duplicated(keep=False)

testli = testli.tolist()

testtf = 0

for i in range(len(testli)):
    if testli[i] == False:
        if testtf % 2 == 0:
            testli[i] = True
            testtf += 1
        else:
            testtf += 1
            
testdrop = testdf.loc[:,testli]     
               
for key, key2 in zip(portfs, weights):
    if len(portfs[key].columns.tolist()) != len(weights[key2]):
        print(key, len(portfs[key].columns.tolist()), len(weights[key2]))
        

# shuffle using df.sample
testdf.sample(frac=1,random_state=1,axis=1)
testswt = pd.Series(testwt)    
testswt.sample(frac=1,random_state=1)
       
testdf2 = pd.DataFrame(np.array(testwt).reshape(1,len(testwt)))
    
testdf_noDup = testdf.loc[:,~testdf.columns.duplicated()]
testdf3 = testdf_noDup.loc[:,testli2] 

     
