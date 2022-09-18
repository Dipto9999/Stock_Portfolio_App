#######################
### Import Modules. ###
#######################

from constants import *

from market import Market

import datetime as dt
import math

import pandas as pd
import pandas_datareader as web
import sqlite3

import matplotlib.pyplot as plt
import seaborn as sns

from IPython.display import display

#################
### Portfolio ###
#################

class Portfolio() :
    def __init__(self, name, tickers, days) :
        # Table Does Not Exist.
        if (not self.records_exist()) :
            self.init_records(name = name, tickers = tickers, days = days)
        # Table Exists.
        elif (self.records_exist()) :
            self.get_name()
            self.get_tickers()

            self.get_holdings()
            self.get_balances()

            # Calculate Effective Dates for Stock Porfolio.
            delta = dt.datetime.today().date() - self.holdings.index[-1]
            effective_dates = [self.holdings.index[-1] + dt.timedelta(days = (i + 1)) for i in range(delta.days + 1)]

            # Create Updated Holdings DataFrame.
            updated_holdings = pd.DataFrame(index = effective_dates, columns = self.holdings.columns)
            # Initialize Updated Stock Holdings Most Recent Purchase Activity.
            for i, row in updated_holdings.iterrows() :
                updated_holdings.loc[i] = self.holdings.iloc[-1:].values

            # Append Updated Stock Holdings to Holdings DataFrame.
            self.holdings = pd.concat(
                [self.holdings, updated_holdings],
                ignore_index = False
            )
            self.holdings.index.name = 'Date'

            self.set_holdings()

    def __del__(self) :
        return

    @staticmethod
    def delete_records() :
        name = Portfolio.get_name_record()

        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        # Drop Holdings Table From SQLite Database.
        statement = f''' DROP TABLE IF EXISTS {name}_holdings '''
        c.execute(statement)

        # Drop Balances Table From SQLite Database.
        statement = f''' DROP TABLE IF EXISTS {name}_balances '''
        c.execute(statement)

        # Close Connection.
        con.close()

    @staticmethod
    def records_exist() :
        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        # Check If Tables Exist in SQLite Database.
        statement = ''' SELECT COUNT(*) FROM sqlite_master WHERE TYPE = 'table' AND NAME LIKE '%_holdings' '''
        c.execute(statement)
        found = pd.DataFrame(c.fetchall())[0][0]

        statement = ''' SELECT COUNT(*) FROM sqlite_master WHERE TYPE = 'table' AND NAME LIKE '%_balances' '''
        c.execute(statement)
        found &= pd.DataFrame(c.fetchall())[0][0]

        # Close Connection.
        con.close()

        return (found == 1)

    @staticmethod
    def get_name_record() :
        if (not Portfolio.records_exist()) :
            name = 'NA'
        # Table Exists.
        elif (Portfolio.records_exist()) :
            # Connect To Database.
            con = sqlite3.connect('stock_trades.db')
            # Create Cursor.
            c = con.cursor()

            statement = f''' SELECT NAME FROM sqlite_schema WHERE type='table' AND NAME LIKE '%_holdings' '''

            c.execute(statement)

            name = c.fetchall()[0][0].removesuffix('_holdings')

            # Close Connection.
            con.close()

        return name

    def init_records(self, name, tickers, days) :
        self.name = name
        self.tickers = tickers

        # Calculate Effective Dates for Stock Porfolio.
        start = dt.datetime.today() - dt.timedelta(days)
        effective_dates = []
        for number_days in range((dt.datetime.today().date() - start.date()).days + 1) :
            effective_dates.append((start + dt.timedelta(number_days)).date())

        # Create and Initialize Holdings DataFrame.
        self.holdings = pd.DataFrame(columns = tickers, index = effective_dates).fillna(0)
        self.holdings.index.name = 'Date'

        # Create Initial Stock Balances Dictionary.
        self.balances = {}
        for ticker in self.tickers :
            self.balances[ticker] = 0

        self.set_holdings()
        self.set_balances()

    def reset(self, name, tickers, days) :
        self.delete_records()
        self.init_records(name = name, tickers = tickers, days = days)

    def get_name(self) :
        self.name = self.get_name_record()

        return self.name

    def get_tickers(self) :
        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        # Query Holdings Table Column Names.
        statement = f''' PRAGMA table_info({self.name}_holdings) '''
        c.execute(statement)

        columns_df = pd.DataFrame(
            data = c.fetchall(),
            columns = ['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk']
        )

        # Close Connection.
        con.close()

        self.tickers = columns_df['name'][columns_df['name'] != 'Date'].to_list()

        return self.tickers

    def get_holdings(self) :
        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        # Query Holdings Table Data from SQLite Database.
        statement = f''' SELECT * FROM '{self.name}_holdings' '''
        c.execute(statement)

        # Create Holdings Dataframe.
        self.holdings = pd.DataFrame(data = c.fetchall(), columns = ['Date'] + self.tickers)

        # Close Connection.
        con.close()

        self.holdings['Date'] = self.holdings['Date'].map(lambda x : dt.datetime.strptime(x, '%Y-%m-%d').date())
        self.holdings.set_index(keys = self.holdings['Date'], inplace = True)
        self.holdings.drop(columns = ['Date'], inplace = True)

        return self.holdings

    def get_balances(self) :
        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        # Query Balances Table from SQLite Database.
        statement = f''' SELECT * FROM '{self.name}_balances' '''
        c.execute(statement)

        # Create Balances Dictionary.
        self.balances = pd.DataFrame(data = c.fetchall(), columns = self.tickers)
        self.balances = self.balances.to_dict(orient = 'records')[0]

        # Close Connection.
        con.close()

        return self.balances

    def set_holdings(self) :
        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        # Replace Holdings Table on SQLite Database.
        self.holdings.to_sql(
            name = f'{self.name}_holdings',
            con = con,
            if_exists = 'replace',
            index = True,
        )

        # Close Connection.
        con.close()

    def set_balances(self) :
        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        # Create Balances DataFrame.
        balances_df = pd.DataFrame(columns = self.balances.keys())
        balances_df.loc[0] = self.balances.values()

        # Replace Balances Table on SQLite Database.
        balances_df.to_sql(
            name = f'{self.name}_balances',
            con = con,
            if_exists = 'replace',
            index = False,
        )

        # Close Connection.
        con.close()

    def buy_shares(self, ticker, shares, adj_closes, buy_date) :
        # Stock Price Data Unavailable.
        if math.isnan(adj_closes.at[buy_date, ticker]) :
            return 0

        # Add Shares to Effective Dates in Holdings DataFrame.
        for current, row in self.holdings.iterrows() :
            difference = (current - buy_date).days

            if difference >= 0 :
                row[ticker] += shares
        # Add New Deposits to Balances.
        self.balances[ticker] += shares * float(adj_closes.at[buy_date, ticker])

        self.set_holdings()
        self.set_balances()

    def get_buy_date(self, ticker, shares, sell_date) :
        # Check That Holdings for the Effective Dates Exceeds Number of Shares to Sell.
        valid_sell = self.holdings.at[sell_date, ticker] >= shares

        buy_date = (self.holdings.index[0] - dt.timedelta(days = 1))
        buy_date_difference = (buy_date - self.holdings.index[0]).days

        for current_date, row in self.holdings.iterrows() :
            sell_date_difference = (current_date - sell_date).days

            adequate_shares = row[ticker] >= shares
            if (adequate_shares and buy_date_difference < 0) :
                buy_date = current_date
                buy_date_difference = (sell_date - current_date).days

            if sell_date_difference >= 0 :
                valid_sell &= adequate_shares

        if (valid_sell) :
            return buy_date
        else :
            return None

    def max_shares(self, ticker, effective_date) :
        effective_holdings = self.holdings.at[effective_date, ticker]
        current_holdings = self.holdings.at[self.holdings.index[-1], ticker]

        if self.get_buy_date(ticker, effective_holdings, effective_date) is not None :
            valid_shares = effective_holdings
        elif (effective_holdings <= current_holdings) :
            valid_shares = current_holdings
        else :
            valid_shares = self.holdings.loc[effective_date:][ticker].min()

        return valid_shares

    def sell_shares(self, ticker, shares, adj_closes, sell_date) :
        buy_date = self.get_buy_date(ticker, shares, sell_date)

        if (not buy_date) :
            return 0, 0

        # Deduct Number of Shares for Effective Dates.
        for current_date, row in self.holdings.iterrows() :
            sell_date_difference = (current_date - sell_date).days

            # Shares
            if (sell_date_difference >= 0) :
                row[ticker] -= shares

        # Calculate Liquidated Balance From Sold Shares.
        liquidated = shares * float(adj_closes.at[sell_date, ticker])
        # Calculate Initial Deposits Of Sold Shares.
        initial_deposits = shares * float(adj_closes.at[buy_date, ticker])

        effective_profit = liquidated - initial_deposits

        self.balances[ticker] -= initial_deposits

        self.set_holdings()
        self.set_balances()

        return liquidated, effective_profit

    def add_ticker(self, new_ticker) :
        if not (new_ticker in self.tickers) :
            self.tickers.append(new_ticker)

            # Initialize Holdings.
            self.holdings[new_ticker] = [0 for i in range(len(self.holdings.index))]
            self.set_holdings()

            # Initialize Balances.
            self.balances[new_ticker] = 0
            self.set_balances()

        return self.tickers

    def __calculate_balance(self, adj_closes, effective_holdings, date) :
        # Calculate Sum of Current Balances for All Tickers.
        current = 0
        for ticker in effective_holdings.columns :
            current += float(effective_holdings.at[date, ticker]) * float(adj_closes.at[date, ticker])
        return round(current, 2)

    def calculate_balances(self, adj_closes, date) :
        # Calculate Current Balances for Effective Tickers.
        current_balances = {}
        for ticker in self.holdings.columns :
            current_balance = self.__calculate_balance(
                adj_closes = adj_closes,
                effective_holdings = self.holdings[ticker].to_frame(),
                date = date
            )
            if current_balance > 0 :
                current_balances[ticker] = current_balance
        return current_balances

    def __calculate_profit(self, adj_closes, starting_balance, effective_holdings, date) :
        # Calculate Sum of Profits for Effective Shares.
        return round((self.__calculate_balance(adj_closes, effective_holdings, date) - starting_balance), 2)

    def calculate_profits(self, adj_closes, date) :
        # Calculate Profits for Effective Shares.
        profits = {}
        current_balances = self.calculate_balances(adj_closes, date)
        for ticker in current_balances.keys() :
            profits[ticker] = self.__calculate_profit(
                adj_closes = adj_closes,
                starting_balance = self.balances[ticker],
                effective_holdings = self.holdings[ticker].to_frame(),
                date = date
            )
        return profits

    def display_portfolio(self, adj_closes) :
        # Calculate Current Balances and Profits for Tickers.
        last_close = adj_closes.index[-1]
        current_balances = self.calculate_balances(adj_closes = adj_closes, date = last_close)
        profits = self.calculate_profits(adj_closes = adj_closes, date = last_close)

        fig_portfolio, ax = plt.subplots(figsize = (7, 4), dpi = 85)
        fig_portfolio.patch.set_facecolor('#a9a9a9')

        if self.holdings.loc[self.holdings.index[-1]].sum() == 0 :
            ax.set_title("Empty Portfolio", color = "white", fontweight = "bold", size = 15)

            ax.set_facecolor('black')

            # Remove Ticks and Labels on Axes.
            ax.axes.xaxis.set_visible(False)
            ax.axes.yaxis.set_visible(False)

        elif (sum(self.balances.values()) > 0) :
            ax.set_title(f"{self.name}'s Portfolio", color = "white", fontweight = "bold", size = 15)

            ax.set_facecolor('white')

            # Remove Ticks and Labels on Axes.
            ax.axes.xaxis.set_visible(True)
            ax.axes.yaxis.set_visible(True)

            ax.tick_params(axis = 'x', color = 'white')
            ax.tick_params(axis = 'y', color = 'white')

            # Display Pie Chart of Current Balances.
            wedges, texts, autotexts = ax.pie(
                current_balances.values(),
                labels = current_balances.keys(),
                textprops = dict(color = 'black'),
                autopct = '%1.1f%%',
                pctdistance = 0.8
            )

            [text.set_color('white') for text in texts]

            plt.setp(texts, size = 8, weight = 'bold')
            plt.setp(autotexts, size = 8, weight = 'bold')

            chart_center = plt.Circle((0, 0), 0.45, color = 'black')
            plt.gca().add_artist(chart_center)

            # Display Portfolio Preview Label.
            ax.text(
                x = -2, y = 1,
                s = 'Portfolio Preview',
                fontsize = 8,
                fontweight = 'bold',
                color = 'white',
                verticalalignment = 'center',
                horizontalalignment = 'center'
            )

            # Display Current Balances.
            ax.text(
                x = -2, y = 0.85,
                s = f'Total Value : {sum(current_balances.values()):.2f} USD',
                fontsize = 8,
                fontweight = 'semibold',
                color = 'white',
                verticalalignment = 'center',
                horizontalalignment = 'center'
            )

            # Display Profits.
            offset = -0.15
            for ticker, profit in profits.items() :
                if profit > 0 :
                    profit_display = f'{ticker} : +{profit:.2f} USD'
                    text_color = 'green'
                if profit < 0 :
                    profit_display = f'{ticker} : {profit:.2f} USD'
                    text_color = 'red'
                if profit == 0 :
                    profit_display = f'{ticker} : {profit:.2f} USD'
                    text_color = 'white'
                ax.text(
                    x = -2, y = 0.85 + offset,
                    s = profit_display,
                    fontsize = 8,
                    fontweight = 'semibold',
                    color = text_color,
                    verticalalignment = 'center',
                    horizontalalignment = 'center'
                )
                offset -= 0.15

        plt.rcdefaults()

        return fig_portfolio

def test_portfolio() :
    market = Market(
        tickers = ['TSLA', 'MSFT', 'AAPL', 'FB', 'NVDA', 'AMD', 'QCOM', 'CLVS'],
        days = 365
    )

    print(Portfolio.get_name_record())
    portfolio = Portfolio(
        name = 'Jack',
        tickers = ['TSLA', 'MSFT', 'AAPL', 'FB', 'NVDA', 'AMD', 'QCOM', 'CLVS'],
        days = 365
    )
    print(portfolio.get_name())

    portfolio.buy_shares(
        ticker = 'AAPL',
        shares = 14,
        adj_closes = market.get_adjcloses(),
        buy_date = dt.date(2022, 2, 18)
    )

    portfolio.buy_shares(
        ticker = 'CLVS',
        shares = 1352,
        adj_closes = market.get_adjcloses(),
        buy_date = dt.date(2022, 2, 18),
    )

    portfolio.buy_shares(
        ticker = 'AAPL',
        shares = 4,
        adj_closes = market.get_adjcloses(),
        buy_date = dt.date(2022, 2, 24)
    )

    portfolio.buy_shares(
        ticker = 'CLVS',
        shares = 415,
        adj_closes = market.get_adjcloses(),
        buy_date = dt.date(2022, 2, 25)
    )

    portfolio.buy_shares(
        ticker = 'AAPL',
        shares = 5,
        adj_closes = market.get_adjcloses(),
        buy_date = dt.date(2022, 3, 14),
    )

    portfolio.display_portfolio(adj_closes = market.get_adjcloses())

    sell_clvs = portfolio.max_shares(
        ticker = 'CLVS',
        effective_date = dt.date(2022, 4, 6)
    )
    print(f'Max CLVS : {sell_clvs}')

    revenue, effective_profit = portfolio.sell_shares(
        ticker = 'CLVS',
        shares = 1500,
        adj_closes = market.get_adjcloses(),
        sell_date = dt.date(2022, 4, 6)
    )
    print(f'Revenue : {revenue}\nEffective Profit : {effective_profit}')

    sell_clvs = portfolio.max_shares(
        ticker = 'CLVS',
        effective_date = dt.date(2022, 4, 7)
    )
    print(f'Max CLVS : {sell_clvs}')

    portfolio.display_portfolio(market.get_adjcloses())

    portfolio.buy_shares(
        ticker = 'CLVS',
        shares = 500,
        adj_closes = market.get_adjcloses(),
        buy_date = dt.date(2022, 5, 25)
    )

    revenue, effective_profit = portfolio.sell_shares(
        ticker = 'CLVS',
        shares = 600,
        adj_closes = market.get_adjcloses(),
        sell_date = dt.date(2022, 6, 6)
    )
    print(f'Revenue : {revenue}\nEffective Profit : {effective_profit}')

    sell_clvs = portfolio.max_shares(
        ticker = 'CLVS',
        effective_date = dt.date(2022, 4, 7)
    )
    print(f'Max CLVS : {sell_clvs}')

    market.add_ticker('WMT')
    portfolio.add_ticker('WMT')

    portfolio.buy_shares(
        ticker = 'WMT',
        shares = 5,
        adj_closes = market.get_adjcloses(),
        buy_date = dt.date(2022, 3, 14)
    )

    revenue, effective_profit = portfolio.sell_shares(
        ticker = 'WMT',
        shares = 5,
        adj_closes = market.get_adjcloses(),
        sell_date = dt.date(2022, 2, 7)
    )
    print(f'Revenue : {revenue}\nEffective Profit : {effective_profit}')

    portfolio.display_portfolio(adj_closes = market.get_adjcloses())


if __name__ == '__main__' :
    test_portfolio()
