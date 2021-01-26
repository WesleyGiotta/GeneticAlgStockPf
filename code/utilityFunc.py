#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 21:40:08 2021

@author: wesley
"""
import numpy as np
import random

def list_dup(L):
    """Takes list and returns a list without duplicates."""
    seen = set()
    seen2 = set()
    seen_add = seen.add
    seen2_add = seen2.add
    for item in L:
        if item in seen:
            seen2_add(item)
        else:
            seen_add(item)
    return list(seen)


# function to generate weights (precent of budget) for each stock 
def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
        List converted to pd.Series."""

    dividers = sorted([random.uniform(0,total) for i in range(0,n-1)])
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

# https://stackoverflow.com/questions/3589214/generate-random-numbers-summing-to-a-predefined-value
# https://stackoverflow.com/questions/8064629/random-numbers-that-add-to-100-matlab/8068956#8068956
# https://stackoverflow.com/questions/18659858/generating-a-list-of-random-numbers-summing-to-1


# randomly pick the stocks for the portfolio and percent to spend on each
def pickPfWt(df, pop = 240, randSeed = 0):
    """Takes subsets of dataframe and puts in dictionary. Randomly generates 
        lists of weights for the subsets and puts in separate dictionary."""
    portfs = {}
    weights = {}
    s = randSeed
    for i in range(pop):
        random.seed(s)
        # number of stocks for each portfolio
        n = random.randint(15, 50)
        portfs['pf_%s' % i] = df.iloc[:,:489].sample(n,random_state=s,axis=1)
        weights['w_%s' % i] = constrained_sum_sample_pos(n, 1)
        s += 1
    return portfs, weights, pop


# check for accuracy
def sharpe_calc(returns, list_wt, rfr):
    """Calculate sharpe ratio returns is a DataFrame,
        list_wt is a list, rfr is a float."""
    mean_returns = returns.mean()
    pf_return = round(np.sum(mean_returns * list_wt) * 252,2)
    pf_std_dev = round(np.sqrt(np.dot(list_wt,np.dot(returns.cov(), list_wt))) * np.sqrt(252),2)
    sharpe = (pf_return - rfr)/pf_std_dev
    return sharpe


# randomize stock order in portfolio
def stockShuffle(df1, df2):
    """Takes two dictionaries and jointly randomizes them.
        Make sure df1 -> portfs[key] and df2 -> weights[key2]."""
    # make list of column names
    pfCols = df1.columns.tolist()
    # combine lists, randomize, and separate
    c = list(zip(pfCols, df2))
    random.shuffle(c)
    pfCols, wt = zip(*c)
    df2 = list(wt) # convert tuple to list
    # implement changes to columns
    noDup = df1.loc[:,~df1.columns.duplicated()]
    df1 = noDup.loc[:,pfCols]
    return df1, df2





