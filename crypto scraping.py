# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 15:39:09 2018

@author: Suman
"""

import bs4 as bs
import pickle
import requests
import datetime as dt
import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError
import inspect
import os
import crypto_analysis


class load_data(object):
    """
    A class used to get the data for the crypto from various sources
    """
    def __init__(self):
        super(load_data, self).__init__()
        self.crypto_data_dir = "{pkg_path}/{crypto_data}".format(pkg_path=os.path.dirname(inspect.getfile(crypto_analysis)),
                                                            crypto_data="crypto_data")
        self.crypto_list_filepath = "{pkg_path}/{crypto_data}/{crypto_list}".format(pkg_path=os.path.dirname(inspect.getfile(crypto_analysis)),
                                                            crypto_data="crypto_data",
                                                            crypto_list="crypto_list.pickle")

    def yahoo():
        print("Loaded from yahoo!")

    def mem():
        print("loaded from mem")


    def get_top_n_crypto_tickers(self, n=10):
        '''
        Getting a list of names of top n Cryptocurrencies as listed in
        cryptocoincharts website.
        Note : Modularize this source better
        Parameters
        ----------
        n = number of top crypto currency price data to be downloaded locally
        '''
        resp = requests.get('https://cryptocoincharts.info/coins/info')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table',
                         {'class': 'table table-striped table-hover footable sortable'})
        tickers = []
        for row in table.findAll('tr')[1:n]: #1:20 indicates taking only the top 20 cryptocurrncies. The limit is 100 and if you want, lets say 49 top currencies, you change it to 1:49
            ticker = row.findAll('td')[0].text+"-USD" #[0] indicates the column in the table that contains the names of all the cryptos. I'm appending USD to it because that's how it is named in Yahoo finance
            tickers.append(ticker)

        if not os.path.exists(self.crypto_data_dir):
            os.makedirs(self.crypto_data_dir)

        with open(self.crypto_list_filepath,"wb") as f:
            pickle.dump(tickers,f)

        return tickers


    def get_data_from_yahoo(self,
                            reload_crypto=False,
                            start = dt.datetime(2015, 12, 27),
                            end = dt.datetime(2017, 12, 27)):

        if reload_crypto:
            tickers = save_crypto_tickers()
        else:
            with open(self.crypto_list_filepath,"rb") as f:
                tickers = pickle.load(f)

        if not os.path.exists(self.crypto_data_dir):
            os.makedirs(self.crypto_data_dir)

        for ticker in tickers:
            if not os.path.exists('{crypto_data_dir}/{ticker}.csv'.format(crypto_data_dir=self.crypto_data_dir,
                                                                          ticker=ticker)):
                try:
                    df1 = web.DataReader(ticker.strip(), "yahoo", start, end)
                    df1.to_csv('{crypto_data_dir}/{ticker}.csv'.format(crypto_data_dir=self.crypto_data_dir,
                                                                                  ticker=ticker))
                except RemoteDataError:
                    pass #the pickled list and the yahoo list is not the same, when a crypto which is in the pickle list but not in yahoo is encountered, this exception will ensure that a error does not occur
            else:
                print('Already have {}'.format(ticker))