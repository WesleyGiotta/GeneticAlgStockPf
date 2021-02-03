#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 16:23:42 2021

@author: wesley
"""

import os, time
import pandas as pd
import Code.stockPrices as sp

def last_modified_fileinfo(filepath):
	# https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-38.php
	filestat = os.stat(filepath)
	date = time.localtime((filestat.st_mtime))

	# Extract year, month and day from the date
	year = date[0]
	month = date[1]
	day = date[2]
	# Extract hour, minute, second
	hour = date[3]
	minute = date[4]
	second = date[5]
	
	# Year
	strYear = str(year)[0:]

	# Month
	if (month <=9):
	    strMonth = '0' + str(month)
	else:
	    strMonth = str(month)

	# Date
	if (day <=9):
	    strDay = '0' + str(day)
	else:
	    strDay = str(day)

	return (strMonth+"-"+strDay+"-"+strYear+" "+str(hour)+":"+str(minute)+":"+str(second))


def updateData():
    result = None
    print("Last updated on:", last_modified_fileinfo('./data/adjClose.csv'))
    while result is None:
        update = input('Do you want to update stock data (y/n)?')
        if update == 'y':
            print('Updating data...')
            sp.getStockData()
            
            # adjusted closed stock data
            adjClose = pd.read_csv('./data/adjClose.csv', index_col = 0)
            # calculate the return rate
            returns = (adjClose - adjClose.shift(1))/adjClose.shift(1)
            returns = returns.iloc[1:] # drop the na row made by the shift
            print("Done.")
            result = 1
        elif update == 'n':
            print('Fetching data...')
            # adjusted closed stock data
            adjClose = pd.read_csv('./data/adjClose.csv', index_col = 0)
            # calculate the return rate
            returns = (adjClose - adjClose.shift(1))/adjClose.shift(1)
            returns = returns.iloc[1:] # drop the na row made by the shift
            print("Done.")
            result = 1
        else:
            print("Your response should be 'y' or 'n'.")
    # use t-bill for risk-free rate
    # https://www.federalreserve.gov/data.htm
    tbill = pd.read_csv('./data/t_bill.csv', index_col = 0)
    tbill.columns = ['rate']
    rfr = tbill['rate'].mean()/100
    return returns, rfr



