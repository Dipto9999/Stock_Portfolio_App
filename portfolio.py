#######################
### Import Modules. ###
#######################

from numpy import False_
from market import Market

import datetime as dt

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
    def __init__(self, adj_closes, tickers, days) :
        self.adj_closes = adj_closes

        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        # Check If Tables Exist.
        statement = ''' SELECT COUNT(*) FROM sqlite_master WHERE TYPE = 'table' AND NAME = 'purchases' '''
        c.execute(statement)
        found = pd.DataFrame(c.fetchall())[0][0]

        statement = ''' SELECT COUNT(*) FROM sqlite_master WHERE TYPE = 'table' AND NAME = 'balances' '''
        c.execute(statement)
        found &= pd.DataFrame(c.fetchall())[0][0]

        # Table Does Not Exist.
        if (found == 0) :
            self.tickers = tickers
            start = dt.datetime.today() - dt.timedelta(days)
            # today().date()
            effective_dates = []
            for number_days in range((dt.datetime.today().date() - start.date()).days) :
                effective_dates.append((start + dt.timedelta(number_days)).date())

            self.purchases = pd.DataFrame(columns = tickers, index = effective_dates).fillna(0)
            self.purchases.index.name = 'Date'

            self.balances = {}
            for ticker in self.tickers :
                self.balances[ticker] = 0

            self.purchases.to_sql(
                name = 'purchases',
                con = con,
                if_exists = 'replace',
                index = True,
            )

            balances_df = pd.DataFrame(columns = self.balances.keys())
            balances_df.loc[0] = self.balances.values()

            balances_df.to_sql(
                name = 'balances',
                con = con,
                if_exists = 'replace',
                index = False,
            )

        # Table Exists.
        else :
            # Retrieve Table Column Names.
            statement = ''' PRAGMA table_info(purchases) '''
            c.execute(statement)

            columns_df = pd.DataFrame(
                data = c.fetchall(),
                columns = ['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk']
            )

            # Retrieve Table Data.
            statement = ''' SELECT * FROM purchases '''
            c.execute(statement)

            self.purchases = pd.DataFrame(data = c.fetchall(), columns = columns_df['name'].to_list())
            self.purchases['Date'] = self.purchases['Date'].map(lambda x : dt.datetime.strptime(x, '%Y-%m-%d').date())
            self.purchases.set_index(keys = self.purchases['Date'], inplace = True)
            self.purchases.drop(columns = ['Date'], inplace = True)

            self.tickers = self.purchases.columns.tolist()

            delta = dt.datetime.today().date() - self.purchases.index[-1]
            effective_dates = [self.purchases.index[-1] + dt.timedelta(days = (i + 1)) for i in range(delta.days + 1)]

            # Duplicate Most Recent Purchase Activity.
            updated_purchases = pd.DataFrame(index = effective_dates, columns = self.purchases.columns)
            for i, row in updated_purchases.iterrows() :
                updated_purchases.loc[i] = self.purchases.iloc[-1:].values

            self.purchases = pd.concat(
                [self.purchases, updated_purchases],
                ignore_index = False
            )

            self.purchases.index.name = 'Date'

            statement = ''' SELECT * FROM balances '''
            c.execute(statement)

            tickers = columns_df['name'][columns_df['name'] != 'Date'].to_list()

            self.balances = pd.DataFrame(data = c.fetchall(), columns = tickers)
            self.balances = self.balances.to_dict(orient = 'records')[0]

        self.purchases.to_sql(
            name = 'purchases',
            con = con,
            if_exists = 'replace',
            index = True,
        )

        # Close Connection.
        con.close()

    def __set_balances(self) :
        # Connect To Database.
        con = sqlite3.connect('stock_trades.db')
        # Create Cursor.
        c = con.cursor()

        balances_df = pd.DataFrame(columns = self.balances.keys())
        balances_df.loc[0] = self.balances.values()

        balances_df.to_sql(
            name = 'balances',
            con = con,
            if_exists = 'replace',
            index = False,
        )

        # Close Connection.
        con.close()

    def purchase_stock(self, ticker, shares, date) :
        for current, row in self.purchases.iterrows() :
            difference = (current - date).days

            if difference >= 0 :
                row[ticker] += shares

        self.balances[ticker] += shares * float(self.adj_closes.at[date, ticker])
        print(self.balances)
        self.__set_balances()

    def __calculate_balance(self, effective_purchases, date) :
        current = 0
        for ticker in effective_purchases.columns :
            current += float(effective_purchases.at[date, ticker]) * float(self.adj_closes.at[date, ticker])
        return round(current, 2)

    def calculate_balances(self, date) :
        current_balances = {}
        for ticker in self.purchases.columns :
            current_balance = self.__calculate_balance(
                effective_purchases = self.purchases[ticker].to_frame(),
                date = date
            )
            if current_balance > 0 :
                current_balances[ticker] = current_balance
        return current_balances

    def __calculate_profit(self, starting_balance, effective_purchases, date) :
        return round((self.__calculate_balance(effective_purchases, date) - starting_balance), 2)

    def calculate_profits(self, date) :
        profits = {}
        current_balances = self.calculate_balances(date)
        for ticker in current_balances.keys() :
            profits[ticker] = self.__calculate_profit(
                starting_balance = self.balances[ticker],
                effective_purchases = self.purchases[ticker].to_frame(),
                date = date
            )
        return profits

    def display_portfolio(self, date) :
        current_balances = self.calculate_balances(date)
        profits = self.calculate_profits(date)
        print(profits)

        fig, ax = plt.subplots(figsize = (16, 8))
        fig.patch.set_facecolor('#a9a9a9')
        ax.set_title('Stock Portfolio', color = 'white', fontweight = 'bold', size = 20)

        ax.tick_params(axis = 'x', color = 'white')
        ax.tick_params(axis = 'y', color = 'white')

        wedges, texts, autotexts = ax.pie(
            current_balances.values(),
            labels = current_balances.keys(),
            textprops = dict(color = 'black'),
            autopct = '%1.1f%%',
            pctdistance = 0.8
        )

        [text.set_color('white') for text in texts]

        plt.setp(texts, size = 10, weight = 'bold')
        plt.setp(autotexts, size = 10, weight = 'bold')

        chart_center = plt.Circle((0, 0), 0.45, color = 'black')
        plt.gca().add_artist(chart_center)

        # Portfolio Preview Label

        ax.text(
            x = -2, y = 1,
            s = 'Portfolio Preview',
            fontsize = 14,
            fontweight = 'bold',
            color = 'white',
            verticalalignment = 'center',
            horizontalalignment = 'center'
        )

        # Current Balances

        ax.text(
            x = -2, y = 0.85,
            s = f'Total : {sum(current_balances.values()):.2f} USD',
            fontsize = 12,
            fontweight = 'semibold',
            color = 'white',
            verticalalignment = 'center',
            horizontalalignment = 'center'
        )

        # Profits

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
                fontsize = 12,
                fontweight = 'semibold',
                color = text_color,
                verticalalignment = 'center',
                horizontalalignment = 'center'
            )
            offset -= 0.15

        plt.show()
        plt.rcdefaults()

def test_portfolio() :
    market = Market(
        tickers = ['TSLA', 'MSFT', 'AAPL', 'FB', 'NVDA', 'AMD', 'QCOM', 'CLVS'],
        days = 365
    )

    portfolio = Portfolio(
        adj_closes = market.get_adjcloses(),
        tickers = ['TSLA', 'MSFT', 'AAPL', 'FB', 'NVDA', 'AMD', 'QCOM', 'CLVS'],
        days = 365
    )

    portfolio.purchase_stock(
        ticker = 'AAPL',
        shares = 14,
        date = dt.date(2022, 2, 18)
    )

    portfolio.purchase_stock(
        ticker = 'CLVS',
        shares = 1352,
        date = dt.date(2022, 2, 18)
    )

    portfolio.purchase_stock(
        ticker = 'AAPL',
        shares = 4,
        date = dt.date(2022, 2, 24)
    )

    portfolio.purchase_stock(
        ticker = 'CLVS',
        shares = 415,
        date = dt.date(2022, 2, 25)
    )

    portfolio.purchase_stock(
        ticker = 'AAPL',
        shares = 5,
        date = dt.date(2022, 3, 14)
    )

    portfolio.display_portfolio(date = dt.date(2022, 4, 6))

test_portfolio()
