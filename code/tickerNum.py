#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 17:11:08 2020

@author: wesley
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

# table starts at line 213 in source code

##test code
#page = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
#bs = BeautifulSoup(page.content,'html.parser')
#table = bs.find("table", {'class':'wikitable sortable','id':'constituents'}).find_all('tr')
#
##get the header aka row 0
#header = table[0].find_all(['td','th'])
#column = 0
#while True:
#    try:
#        print(header[column].text)
#        column += 1
#    except:
#        print("Done")
#        break


def sp500Data(url):
    '''
    Put in string of url:
    https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
    Webscrapping from above url for the ticker numbers because
    I am too lazy to type them all out.
    '''
    page = requests.get(url)
    bs = BeautifulSoup(page.content,'html.parser')
    table = bs.find("table", {'class':'wikitable sortable','id':'constituents'}).find_all('tr')
    # get table from wiki, each row is a list
    sp = []
    row = 0
    while True:
        try:
            data = table[row].find_all(['td','th'])
            column = 0
            row += 1
            intermediate = []
            while True:
                try:
                    intermediate.append(data[column].text.replace('\n',''))
                    column += 1
                except:
                    break
            sp.append(intermediate)
        except:
            break
    # convert nested list into dataframe
    return pd.DataFrame(sp[1:],columns=sp[0])


ticker = sp500Data("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")

ticker.to_csv('../data/tickerNum.csv', index=True)



