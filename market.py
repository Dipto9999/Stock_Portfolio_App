#######################
### Import Modules. ###
#######################

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
        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        # Check If Table Exists.
        statement = ''' SELECT COUNT(*) FROM sqlite_master WHERE TYPE = 'table' AND NAME = 'adj_closes' '''
        c.execute(statement)

        found = pd.DataFrame(c.fetchall())[0][0]

        # Table Does Not Exist.
        if (found == 0) :
            self.tickers = tickers
            start = dt.datetime.today() - dt.timedelta(days)

            # Retrieve Yahoo Stock Prices.
            try :
                self.stock_prices = [
                    web.DataReader(
                        ticker, 'yahoo', start, dt.datetime.today()
                    ) for ticker in self.tickers
                ]
            except :
                self.stock_prices = pd.DataFrame()

            self.adj_closes = {}
            for i in range(len(self.tickers)) :
                self.adj_closes[self.tickers[i]] = self.stock_prices[i]['Adj Close'].apply(lambda x : round(x, 2))

            self.adj_closes = pd.DataFrame.from_dict(self.adj_closes)
            self.dates = [day.date() for day in self.adj_closes.index]
            self.adj_closes = self.adj_closes.reindex(self.dates)

        # Table Exists.
        else :
            # Retrieve Table Column Names.
            statement = ''' PRAGMA table_info(adj_closes) '''
            c.execute(statement)

            columns_df = pd.DataFrame(
                data = c.fetchall(),
                columns = ['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk']
            )

            # Retrieve Table Data.
            statement = ''' SELECT * FROM adj_closes '''
            c.execute(statement)

            self.tickers = columns_df['name'][columns_df['name'] != 'Date'].to_list()

            self.stock_prices = pd.DataFrame(data = c.fetchall(), columns = columns_df['name'].to_list())
            self.stock_prices.set_index(keys = self.stock_prices['Date'], inplace = True)
            self.stock_prices.drop(columns = ['Date'], inplace = True)

            start = dt.datetime.combine(
                dt.datetime.strptime(self.stock_prices.index[-1], '%Y-%m-%d'),
                dt.datetime.min.time()
            )

            # Retrieve Yahoo Stock Prices.
            try :
                self.stock_prices = [
                    web.DataReader(
                        ticker,
                        'yahoo',
                        start,
                        dt.datetime.now()
                    ) for ticker in self.tickers
                ]
            except :
                self.stock_prices = pd.DataFrame()

            self.adj_closes = {}
            for i in range(len(self.tickers)) :
                self.adj_closes[self.tickers[i]] = self.stock_prices[i]['Adj Close'].apply(lambda x : round(x, 2))

            self.adj_closes = pd.DataFrame.from_dict(self.adj_closes)
            self.dates = [day.date() for day in self.adj_closes.index]
            self.adj_closes = self.adj_closes.reindex(self.dates)

        self.adj_closes.to_sql(
            name = 'adj_closes',
            con = con,
            if_exists = 'append',
            index = True,
        )

        statement = ''' SELECT * FROM 'adj_closes' '''
        c.execute(statement)

        # Retrieve Lifetime Data From SQLite Table.
        self.adj_closes = pd.DataFrame(c.fetchall(), columns = ['Date'] + self.adj_closes.columns.tolist())
        self.adj_closes.set_index(keys = self.adj_closes['Date'], inplace = True)
        self.adj_closes.drop(columns = ['Date'], inplace = True)
        self.adj_closes = self.adj_closes[~self.adj_closes.index.duplicated(keep = 'first')]

        self.dates = [dt.datetime.strptime(day, '%Y-%m-%d').date() for day in self.adj_closes.index]
        self.adj_closes.index = self.dates

        # Close Connection.
        con.close()

    def get_adjcloses(self) :
        return self.adj_closes

    def plot_adjcloses(self) :
        plt.figure(figsize = (20, 12))
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
        plt.show()

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
        plt.figure(figsize = (12, 8))

        # First Subplot is Adj Closes.
        ax1 = plt.subplot(211)
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
        ax2 = plt.subplot(212, sharex = ax1)
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

        plt.show()
        plt.rcdefaults()

    def plot_corr(self) :
        self.corr_data = self.adj_closes.pct_change().corr(method = 'pearson').apply(lambda x : round(x * 100, 2))

        plt.figure(figsize = (20, 12))

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

        heatmap.set_title('Stock Correlations', fontsize = 25)
        plt.show()

def test_market() :
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

# test_market()