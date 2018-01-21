# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 16:55:54 2017

@author: Suman
"""

############################################################################

'''Loading packages and setting a directory'''

###########################################################################

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import os
import bs4 as bs
import pickle
import requests
from pandas_datareader._utils import RemoteDataError
import numpy as np
from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

directoryname = "C:\\Users\\Suman\\Desktop\\Columbia\\Winter Break\\Crypto" #insert the file address where you want everything to be stored
os.chdir(directoryname)


############################################################################

'''Getting a list of names of Cryptocurrencies'''

###########################################################################
# We pickle the list so that we can save it and dont need to hit the cryptocoin website each time

#This piece of Code requests the cryptocoincharts for a list of the top 100 currencies
def save_crypto_tickers():
    resp = requests.get('https://cryptocoincharts.info/coins/info')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'table table-striped table-hover footable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:60]: #1:20 indicates taking only the top 20 cryptocurrncies. The limit is 100 and if you want, lets say 49 top currencies, you change it to 1:49
        ticker = row.findAll('td')[0].text+"-USD" #[0] indicates the column in the table that contains the names of all the cryptos. I'm appending USD to it because that's how it is named in Yahoo finance
        tickers.append(ticker)
        
    with open("cryptotickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        
    return tickers

save_crypto_tickers()

############################################################################

'''Getting all pricing data in the cryptolist'''

###########################################################################

def get_data_from_yahoo(reload_crypto=False):
    
    if reload_crypto:
        tickers = save_crypto_tickers()
    else:
        with open("cryptotickers.pickle","rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('crypto_dfs'):
        os.makedirs('crypto_dfs')

    start = dt.datetime(2015, 12, 27) #set the date from which you want the data
    end = dt.datetime(2017, 12, 27) #set the date to which the data is considered
    
    for ticker in tickers:
        if not os.path.exists('crypto_dfs/{}.csv'.format(ticker)):
            try:
                df1 = web.DataReader(ticker.strip(), "yahoo", start, end)
                df1.to_csv('crypto_dfs/{}.csv'.format(ticker))
            except RemoteDataError:
                pass #the pickled list and the yahoo list is not the same, when a crypto which is in the pickle list but not in yahoo is encountered, this exception will ensure that a error does not occur
        else:
            print('Already have {}'.format(ticker))

get_data_from_yahoo()

############################################################################

'''Combining all crypto prices into one DataFrame'''

###########################################################################


def compile_data():
    with open("cryptotickers.pickle","rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()
    
    for count,ticker in enumerate(tickers):
        try:
            df1 = pd.read_csv('crypto_dfs/{}.csv'.format(ticker))
            df1.set_index('Date', inplace=True)
    
            df1.rename(columns={'Adj Close':ticker}, inplace=True)
            df1.drop(['Open','High','Low','Close','Volume'],1,inplace=True)
            df1 = df1.pct_change()[1:]
    
            if main_df.empty:
                main_df = df1
            else:
                main_df = main_df.join(df1, how='outer')
    
            if count % 10 == 0:
                print(count)
        except:
            pass
    print(main_df.head())
    main_df.to_csv('crypto_returns.csv')


compile_data()

############################################################################

'''Creating correlation table for Relationships'''

###########################################################################

def visualize_data():
    df = pd.read_csv('crypto_returns.csv')
    #df['AAPL'].plot()
    #plt.show()
    df_corr = df.corr()
    print(df_corr.head())
    df_corr.to_csv('crypto_corr.csv')
    
    data1 = df_corr.values
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)

    heatmap1 = ax1.pcolor(data1, cmap=plt.cm.RdYlGn)
    fig1.colorbar(heatmap1)

    ax1.set_xticks(np.arange(data1.shape[1]) + 0.5, minor=False)
    ax1.set_yticks(np.arange(data1.shape[0]) + 0.5, minor=False)
    ax1.invert_yaxis()
    ax1.xaxis.tick_top()
    column_labels = df_corr.columns
    row_labels = df_corr.index
    ax1.set_xticklabels(column_labels)
    ax1.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap1.set_clim(-1,1)
    plt.tight_layout()
    #plt.savefig("correlations.png", dpi = (300))
    plt.show()
    
visualize_data()

############################################################################

'''Machine Learning'''

###########################################################################


def process_data_for_labels(ticker):
    hm_days = 7
    df = pd.read_csv('crypto_returns.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)
    
    for i in range(1,hm_days+1):
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
        
    df.fillna(0, inplace=True)
    return tickers, df

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.09
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0

from collections import Counter

def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)

    df['{}_target'.format(ticker)] = list(map( buy_sell_hold,
                                               df['{}_1d'.format(ticker)],
                                               df['{}_2d'.format(ticker)],
                                               df['{}_3d'.format(ticker)],
                                               df['{}_4d'.format(ticker)],
                                               df['{}_5d'.format(ticker)],
                                               df['{}_6d'.format(ticker)],
                                               df['{}_7d'.format(ticker)] ))
    
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:',Counter(str_vals))
    
    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)
    
    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)
    
    X = df_vals.values
    y = df['{}_target'.format(ticker)].values
    
    return X,y,df

def do_ml(ticker):
    X, y, df = extract_featuresets(ticker)

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,
                                                        y,
                                                        test_size=0.25)

    #clf = neighbors.KNeighborsClassifier()

    clf = VotingClassifier([('lsvc',svm.LinearSVC()),
                            ('knn',neighbors.KNeighborsClassifier()),
                            ('rfor',RandomForestClassifier())])


    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('accuracy:',confidence)
    predictions = clf.predict(X_test)
    print('predicted class counts:',Counter(predictions))
    print()
    print()
    return confidence

do_ml('NEO-USD')