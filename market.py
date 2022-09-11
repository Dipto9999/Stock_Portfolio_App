#######################
### Import Modules. ###
#######################

from constants import *

import datetime as dt

import pandas as pd
import pandas_datareader as web
import sqlite3

import matplotlib.pyplot as plt
import seaborn as sns

from IPython.display import display

##############
### Market ###
##############

class Market() :
    def __init__(self, tickers, days) :
        # Table Does Not Exist.
        if (not self.records_exist()) :
            self.init_records(tickers = tickers, days = days)
        # Table Exists.
        elif (self.records_exist()) :
            self.get_tickers()
            self.get_adjcloses()

            start = dt.datetime.combine(
                self.dates[-1],
                dt.datetime.min.time()
            )

            # Retrieve Yahoo Stock Prices.
            try :
                stock_prices = [
                    web.DataReader(
                        ticker,
                        'yahoo',
                        start,
                        dt.datetime.now()
                    ) for ticker in self.tickers
                ]
            except :
                return

            # Create Updated Adjusted Closes DataFrame.
            self.stock_prices = []
            updated_closes = {}
            for i in range(len(self.tickers)) :
                self.stock_prices.append(pd.DataFrame(stock_prices[i].iloc[lambda x : x.index >= start]))
                updated_closes[self.tickers[i]] = self.stock_prices[i]['Adj Close'].apply(lambda x : round(x, 2))

            updated_closes = pd.DataFrame.from_dict(updated_closes)
            updated_dates = [effective_datetime.date() for effective_datetime in updated_closes.index]

            # Update Adjusted Closes Indices.
            updated_closes.index = pd.Index(updated_dates, name = 'Date')

            # Append Updated Stock Holdings to Holdings DataFrame.
            self.adj_closes = pd.concat(
                [self.adj_closes, updated_closes],
                ignore_index = False
            )
            self.adj_closes = self.adj_closes[~self.adj_closes.index.duplicated(keep = 'first')]

            self.get_dates()

        self.set_adjcloses()

    def __del__(self) :
        return

    @staticmethod
    def delete_records() :
        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        # Drop Purchases Table from SQLite Database.
        statement = ''' DROP TABLE IF EXISTS adj_closes '''
        c.execute(statement)

        # Close Connection.
        con.close()

    @staticmethod
    def records_exist() :
        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        # Check If Table Exists in SQLite Database.
        statement = ''' SELECT COUNT(*) FROM sqlite_master WHERE TYPE = 'table' AND NAME = 'adj_closes' '''
        c.execute(statement)

        found = pd.DataFrame(c.fetchall())[0][0]

        # Close Connection.
        con.close()

        return (found == 1)

    @staticmethod
    def get_ticker_records() :
        if (not Market.records_exist()) :
            tickers = STANDARD_TICKERS
        elif (Market.records_exist()) :
            # Connect To Database.
            con = sqlite3.connect('stock_trades.db')
            # Create Cursor.
            c = con.cursor()

            # Query Adjusted Closes Table Column Names.
            statement = ''' PRAGMA table_info(adj_closes) '''
            c.execute(statement)

            columns_df = pd.DataFrame(
                data = c.fetchall(),
                columns = ['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk']
            )

            # Close Connection.
            con.close()

            tickers = columns_df['name'][columns_df['name'] != 'Date'].to_list()

        return tickers

    @staticmethod
    def get_creation_date() :
        # Table Does Not Exist.
        if (not Market.records_exist()) :
            start = (dt.datetime.today() - dt.timedelta(MAX_DAYS + 1)).date()

            # Retrieve Yahoo Stock Prices.
            try :
                stock_prices = [
                    web.DataReader(
                        ticker, 'yahoo', start, dt.datetime.today()
                    ) for ticker in STANDARD_TICKERS
                ]
            except :
                return

            # Create Adjusted Closes DataFrame.
            adj_closes = {}
            for i in range(len(STANDARD_TICKERS)) :
                adj_closes[STANDARD_TICKERS[i]] = stock_prices[i]['Adj Close'].apply(lambda x : round(x, 2))
            adj_closes = pd.DataFrame.from_dict(adj_closes)

            creation_date = adj_closes.index[0].date()

        elif (Market.records_exist()) :
            tickers = Market.get_ticker_records()

            # Connect To Database.
            con = sqlite3.connect('stock_trades.db')
            # Create Cursor.
            c = con.cursor()

            statement = ''' SELECT * FROM 'adj_closes' '''
            c.execute(statement)

            # Query Adjusted Closes Table Data From SQLite Database and Create Adjusted Closes DataFrame.
            adj_closes = pd.DataFrame(c.fetchall(), columns = ['Date'] + tickers)

            # Close Connection.
            con.close()

            creation_date = dt.datetime.strptime(adj_closes['Date'].values[0], '%Y-%m-%d').date()

        return creation_date

    def init_records(self, tickers, days) :
        self.tickers = tickers
        start = dt.datetime.today() - dt.timedelta(days + 1)

        # Retrieve Yahoo Stock Prices.
        try :
            stock_prices = [
                web.DataReader(
                    ticker, 'yahoo', start, dt.datetime.today()
                ) for ticker in self.tickers
            ]
        except :
            return

        # Set Adjusted Close Stock Prices.
        self.stock_prices = []
        self.adj_closes = {}

        for i in range(len(self.tickers)) :
            self.stock_prices.append(pd.DataFrame(stock_prices[i].iloc[lambda x : x.index >= start]))
            self.adj_closes[self.tickers[i]] = self.stock_prices[i]['Adj Close'].apply(lambda x : round(x, 2))

        # Create Adjusted Closes DataFrame.
        self.adj_closes = pd.DataFrame.from_dict(self.adj_closes)
        # Reindex DataFrame As Type datetime.date.
        self.dates = [day.date() for day in self.adj_closes.index]
        self.adj_closes = self.adj_closes.reindex(self.dates)

        self.set_adjcloses()

    def reset(self, tickers, days) :
        self.delete_records()
        self.init_records(tickers = tickers, days = days)

    def get_tickers(self) :
        self.tickers = self.get_ticker_records()

        return self.tickers

    def get_adjcloses(self) :
        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        statement = ''' SELECT * FROM 'adj_closes' '''
        c.execute(statement)

        # Query Adjusted Closes Table Data From SQLite Database and Create Adjusted Closes DataFrame.
        self.adj_closes = pd.DataFrame(c.fetchall(), columns = ['Date'] + self.tickers)
        self.adj_closes.set_index(keys = self.adj_closes['Date'], inplace = True)
        self.adj_closes.drop(columns = ['Date'], inplace = True)
        self.adj_closes = self.adj_closes[~self.adj_closes.index.duplicated(keep = 'first')]

        # Close Connection.
        con.close()

        # Reindex DataFrame with Dates.
        self.get_dates()

        return self.adj_closes

    def get_dates(self) :
        if isinstance(self.adj_closes.index[-1], str) :
            self.dates = [dt.datetime.strptime(day, '%Y-%m-%d').date() for day in self.adj_closes.index]
        elif isinstance(self.adj_closes.index[-1], dt.date) :
            self.dates = self.adj_closes.index

        # Set Adjusted Closes Indices.
        self.adj_closes.index = pd.Index(self.dates, name = 'Date')

        return self.dates

    def set_adjcloses(self) :
        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        # Create or Update Table for Adjusted Closes on SQLite Database.
        self.adj_closes.to_sql(
            name = 'adj_closes',
            con = con,
            if_exists = 'replace',
            index = True,
        )

        # Close Connection.
        con.close()

    def add_ticker(self, new_ticker) :
        if not (new_ticker in self.tickers) :
            # Retrieve Yahoo Stock Prices for New Ticker and Add Column to Adjusted Closes DataFrame.
            self.tickers.append(new_ticker)
            self.stock_prices.append(web.DataReader(new_ticker, 'yahoo', self.dates[0], dt.datetime.now()))
            self.adj_closes[new_ticker] = self.stock_prices[-1]['Adj Close'].apply(lambda x : round(x, 2))

            self.set_adjcloses()

        return self.tickers

    def plot_adjcloses(self) :
        fig_adjcloses = plt.figure(figsize = (20, 12))
        plt.yscale('log')

        for ticker in self.adj_closes.columns :
            lineplot = plt.plot(
                self.adj_closes[ticker],
                linewidth = 2.5,
                label = ticker
            )
        plt.legend(bbox_to_anchor = (1.05, 1), loc = 2, borderaxespad = 0, fontsize = 12.5).set_title('Tickers', prop = {'size' : 17.5})

        plt.xlabel('Date', fontsize = 17.5)
        plt.ylabel('Adjusted Close ($log_{10}$)', fontsize = 17.5)
        plt.title('Market Prices', fontsize = 25)

        return fig_adjcloses

    def plot_rsi(self, ticker, days) :
        ticker_prices = self.adj_closes[ticker]

        delta = ticker_prices.diff(1)
        delta.dropna(inplace = True)

        positive = delta.copy()
        positive[positive < 0] = 0 # Keep positive deltas.

        negative = delta.copy()
        negative[negative > 0] = 0 # Keep negative deltas.

        average_gain = positive.rolling(window = days).mean()
        average_loss = abs(negative.rolling(window = days).mean())
        rsi = (100.0 - (100.0 / (1.0 + average_gain / average_loss))).rename('RSI').to_frame()

        stock_df = pd.merge(ticker_prices, rsi, left_index = True, right_index = True)
        stock_df.rename(columns = {ticker : 'Adj Closes'}, inplace = True)

        plt.style.use("dark_background")
        fig_rsi = plt.figure(figsize = (12, 8))

        # First Subplot is Adj Closes.
        ax1 = fig_rsi.add_subplot(211)
        ax1.plot(
            stock_df.index, stock_df['Adj Closes'],
            linewidth = 2.5, color = 'lightgray'
        )

        ax1.grid(True, color = '#555555')
        ax1.tick_params(axis = 'x', colors = 'white')
        ax1.tick_params(axis = 'y', colors = 'white')
        ax1.set_axisbelow(True)

        ax1.set_facecolor('black')
        ax1.set_title(str(ticker) + ': Adjusted Close Price', color = 'white', fontweight = 'bold')

        # Second Subplot is RSI.
        ax2 = fig_rsi.add_subplot(212, sharex = ax1)
        ax2.plot(
            stock_df.index, stock_df['RSI'],
            linewidth = 2.5, color = 'lightgray'
        )

        # RSI Line Markings.
        for i in range(0, 110, 10) :
            if (i == 0 or i == 100) : # Red If RSI = 0, RSI = 100.
                ax2.axhline(i, linestyle = '--', alpha = 0.5, color = '#ff0000')
            elif (i == 10 or i == 90) : # Yellow If RSI = 10, RSI = 90.
                ax2.axhline(i, linestyle = '--', alpha = 0.5, color = '#ffaa00')
            elif (i == 20 or i == 80) : # Green If RSI = 20, RSI = 80.
                ax2.axhline(i, linestyle = '--', alpha = 0.5, color = '#00ff00')
            elif (i == 30 or i == 70) : # Lightgray If RSI = 30 (i.e. Oversold), RSI = 70 (i.e. Overbought).
                ax2.axhline(i, linestyle = '--', alpha = 1, color = '#cccccc');

        ax2.grid(False)
        ax2.tick_params(axis = 'x', colors = 'white')
        ax2.tick_params(axis = 'y', colors = 'white')
        ax2.set_yticks([i for i in range(0, 110, 10) if i <= 30 or i >= 70])
        ax2.set_axisbelow(True)

        ax2.set_facecolor('black')
        ax2.set_title('RSI Value', color = 'white', fontweight = 'bold')

        plt.rcdefaults()

        return fig_rsi

    def plot_corr(self) :
        self.corr_data = self.adj_closes.pct_change().corr(method = 'pearson').apply(lambda x : round(x * 100, 2))

        fig_corr = plt.figure(figsize = (20, 12))

        heatmap = sns.heatmap(
            data = self.corr_data,
            annot = self.corr_data.values, annot_kws = {'fontsize' : 12.5},
            cmap = 'YlGnBu',
            cbar = True,
            linewidth = 2, linecolor = 'black',
            square = True
        )

        heatmap.set_xlabel('Stocks', fontsize = 18)
        heatmap.set_ylabel('Stocks', fontsize = 18)

        heatmap.figure.axes[-1].set_ylabel('Percentage (%)', size = 18)

        heatmap.set_title('Price Correlations', fontsize = 25)

        return fig_corr

def test_market() :
    tickers = Market.get_ticker_records()
    creation_date = Market.get_creation_date()

    market = Market(
        tickers = ['TSLA', 'MSFT', 'AAPL', 'FB', 'NVDA', 'AMD', 'QCOM', 'CLVS'],
        days = 365
    )

    market.plot_adjcloses()
    market.plot_rsi(
        ticker = 'TSLA',
        days = 15
    )
    market.plot_corr()

    market.add_ticker('WMT')

    market.plot_adjcloses()
    market.plot_rsi(
        ticker = 'WMT',
        days = 15
    )
    market.plot_corr()

    # market.delete_records()

# test_market()
