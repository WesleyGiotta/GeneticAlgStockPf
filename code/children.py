#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 17:55:07 2020

@author: wesley
"""
import pandas as pd
import random
import code.utilityFunc as uf

# 3.a.child crossover

def crossover_pf(parent1, parent2, returns, sed, mrate, wt1, wt2):
    """Takes two dataframes and returns two dataframes that are made by 
        swapping the first 10 percent of coulmns."""
    genes1 = round(len(parent1.columns) * 0.1)
    genes2 = round(len(parent2.columns) * 0.1)
    kid1 = pd.concat([parent1.iloc[:,:genes1].reset_index(drop=True), 
                      parent2.iloc[:,genes2:].reset_index(drop=True)],axis=1)
    kid2 = pd.concat([parent1.iloc[:,genes1:].reset_index(drop=True), 
                      parent2.iloc[:,:genes2].reset_index(drop=True)],axis=1)
    # shuffle
    kid1, wt1 = uf.stockShuffle(kid1, wt1)
    kid2, wt2 = uf.stockShuffle(kid2, wt2)
    # mutate one kid
    random.seed(sed)
    mutate = random.choices([0,1], [1 - mrate, mrate], k=2)
    if mutate[0] == 1:
        kid1 = mutateStock(kid1, returns, sed)
    if mutate[1] == 1:
        kid2 = mutateStock(kid2, returns, sed)
    # shuffle again
    kid1, wt1 = uf.stockShuffle(kid1, wt1)
    kid2, wt2 = uf.stockShuffle(kid2, wt2)
    # # remove potential duplicates -> might keep -> just bigger weight
    # kid1 = kid1.loc[:,~kid1.columns.duplicated()]
    # kid2 = kid2.loc[:,~kid2.columns.duplicated()]
    return kid1, kid2, wt1, wt2


def crossover_wt(weight1, weight2):
    """Takes two lists and returns two lists that are made by 
        swapping the first 10 percent of the list."""
    genes1 = round(len(weight1) * 0.1)
    genes2 = round(len(weight2) * 0.1)
    kid1 = weight1[:genes1] + weight2[genes2:]
    kid2 = weight1[genes1:] + weight2[:genes2]
    # # remove potential duplicates -> might keep -> just bigger weight
    # kid1 = uf.list_dup(kid1)
    # kid2 = uf.list_dup(kid2)
    # scale weights such that they sum to one
    kid1 = [x / sum(kid1) for x in kid1]
    kid2 = [x / sum(kid2) for x in kid2]
    return kid1, kid2


# 3.b.child mutation

def mutateStock(df, returns, sed):
    """Takes one dataframe (one from each child pair) and changes
        first 10 percent of the stocks to randomly decided stocks."""
    mutate_len = round(len(df.columns) * 0.1)
    mutate_genes = returns.iloc[:,:489].sample(mutate_len, random_state=sed, axis=1)
    mutant_kid = pd.concat([df.iloc[:,mutate_len:].reset_index(drop=True),
                            mutate_genes.reset_index(drop=True)],axis=1)
    return mutant_kid



