#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:21:56 2021

@author: wesley
"""

import matplotlib.pyplot as plt
import numpy as np

# ^GSPC stock index 
gspcReturns = round(returns['^GSPC'].mean() * 252,2)
gspcStd = round(returns['^GSPC'].std() * np.sqrt(252),2)
#pf_std_dev = round(np.sqrt(np.dot(list_wt,np.dot(returns.cov(), list_wt))) * np.sqrt(252),2)
gspcsharpe = (gspcReturns - rfr)/gspcStd


plt.plot(bestVal['gen'],bestVal['ratio'], label='Genetic Alg.')
plt.axhline(y=gspcsharpe, color='g', linestyle='-', label='^GSPC')
plt.xlabel('Generations')
plt.ylabel('Sharpe Ratio')
plt.legend()


plt.plot(bestVal['gen'],bestVal['returns'], label='Genetic Alg.')
plt.axhline(y=gspcReturns, color='g', linestyle='-', label='^GSPC')
plt.xlabel('Generations')
plt.ylabel('Expected Percent Returns')
plt.legend()
