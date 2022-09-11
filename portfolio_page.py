########################################
############## Modules #################
########################################

from default_page import *
from portfolio import Portfolio
from market import Market

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import datetime as dt

######################################
############## Classes ###############
######################################

class PortfolioPage(DefaultPage) :
    def __init__(self, frame, master, market, portfolio) :
        super(PortfolioPage, self).__init__(frame, master, market, portfolio)

        # Create Frames.
        self.display_portfolio_frame = tk.Frame(self)

        self.buy_stocks_frame = BuyFrame(master = self, market = market, portfolio = portfolio)
        self.sell_stocks_frame = SellFrame(master = self, market = market, portfolio = portfolio)

        # Position Frames.
        self.display_portfolio_frame.grid(row = 0, column = 0, rowspan = 2, padx = 5, pady = (5,10))
        self.buy_stocks_frame.grid(row = 0, column = 1, padx = 5, pady = (5,10))
        self.sell_stocks_frame.grid(row = 1, column = 1, padx = 5, pady = (5,10))

        self.display_portfolio_frame.configure(bg = 'white')
        self.buy_stocks_frame.configure(bg = 'white')
        self.sell_stocks_frame.configure(bg = 'white')

        self.display_portfolio(adj_closes = self.market.get_adjcloses())

    def display_portfolio(self, adj_closes) :
        if hasattr(self, "current_portfolio") :
            self.current_portfolio.get_tk_widget().destroy()

        self.fig_portfolio = self.portfolio.display_portfolio(adj_closes)

        self.current_portfolio = FigureCanvasTkAgg(self.fig_portfolio, self.display_portfolio_frame)
        self.current_portfolio.get_tk_widget().pack(side = tk.LEFT, fill = tk.BOTH)

        self.sell_stocks_frame.update_shares(
            ticker = self.sell_stocks_frame.ticker.get(),
            date = dt.datetime.strptime(self.sell_stocks_frame.transaction_date.get(),'%Y-%m-%d').date()
        )

class TransactionFrame(DefaultFrame) :
    def __init__(self, master, market, portfolio) :
        super(TransactionFrame, self).__init__(master)

        self.market = market
        self.portfolio = portfolio

        self.portfolio_tickers = self.portfolio.get_tickers()
        self.dates = self.market.get_dates().tolist()

        # Create Frames.
        self.transaction_frame = tk.Frame(self)
        self.confirmation_frame = tk.Frame(self)

        # Position Frames.
        self.transaction_frame.grid(row = 0, column = 0, rowspan = 2, padx = 5, pady = (5,10))
        self.confirmation_frame.grid(row = 1, column = 1, rowspan = 1, padx = 5, pady = (5,10))

        # Create Label Widgets.
        self.transaction_label = tk.Label(self.transaction_frame, text = 'Transaction',
            bg = master.heading_label_bg, fg = 'black', font = master.heading_label_font, borderwidth = 2, relief = 'solid', anchor = tk.W)

        self.ticker_label = tk.Label(self.transaction_frame, text = 'Ticker : ',
            bg = master.general_label_bg, fg = 'black', font = master.general_label_font, borderwidth = 1, relief = 'solid', anchor = tk.W)
        self.shares_label = tk.Label(self.transaction_frame, text = 'Shares : ',
            bg = master.general_label_bg, fg = 'black', font = master.general_label_font, borderwidth = 1, relief = 'solid', anchor = tk.W)
        self.date_label = tk.Label(self.transaction_frame, text = 'Date : ',
            bg = master.general_label_bg, fg = 'black', font = master.general_label_font, borderwidth = 1, relief = 'solid', anchor = tk.W)

        # Create Spinbox Entry Widgets.

        self.ticker = tk.Spinbox(
            self.transaction_frame, values = self.portfolio_tickers,
            bg = self.general_entry_bg, fg = 'black', font = self.general_entry_font, borderwidth = 2, relief = 'sunken'
        )
        self.transaction_date = tk.Spinbox(
            self.transaction_frame, values = tuple(self.market.get_dates()),
            bg = self.general_entry_bg, fg = 'black', font = self.general_entry_font, borderwidth = 2, relief = 'sunken'
        )
        self.shares = tk.Spinbox(
            self.transaction_frame,
            values = None,
            bg = self.general_entry_bg, fg = 'black', font = self.general_entry_font, borderwidth = 2, relief = 'sunken',
        )

        # Create Button Widget.
        self.submitButton = tk.Button(self.confirmation_frame, text = 'Submit', bg = master.button_bg, fg = 'white',
            font = master.button_font, borderwidth = 2, relief = 'raised',
            command = lambda : self.confirm_transaction(
                        ticker = self.ticker.get(),
                        shares = int(self.shares.get()),
                        date = dt.datetime.strptime(self.transaction_date.get(),'%Y-%m-%d').date()
            )
        )

        # Position Widgets.
        self.transaction_label.grid(row = 0, column = 0, padx = 5, pady = (0, 5), sticky = tk.W)

        self.ticker_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.W)
        self.ticker.grid(row = 1, column = 1, padx = (0, 5), pady = 5, sticky = tk.W)

        self.shares_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tk.W)
        self.shares.grid(row = 2, column = 1, padx = (0, 5), pady = 5, sticky = tk.W)

        self.date_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = tk.W)
        self.transaction_date.grid(row = 3, column = 1, padx = (0, 5), pady = 5, sticky = tk.W)

        self.submitButton.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = tk.W)

    def get_possible_shares(self) :
        return [i for i in range(1, 10 + 1, 1)]

    def confirm_transaction(self, ticker, shares, date) :
        if not hasattr(self, "confirm_transaction_window") or not self.confirm_transaction_window.winfo_exists() :
            self.confirm_transaction_window = ConfirmTransactionWindow(
                master = self.master,
                home_page = self,
                message = f'You will Transaction {shares} shares of {ticker}.',
                ticker = ticker,
                shares = shares,
                date = date
            )

class BuyFrame(TransactionFrame) :
    def __init__(self, master, market, portfolio) :
        super(BuyFrame, self).__init__(master, market, portfolio)

        # Configure Label Widget.
        self.transaction_label.config(text = 'Buy')

        # Configure Spinbox Widget.
        self.shares.config(values = self.get_possible_shares())

    def confirm_transaction(self, ticker, shares, date) :
        if not hasattr(self, "confirm_buy_window") or not self.confirm_buy_window.winfo_exists() :
            self.confirm_buy_window = ConfirmBuyWindow(
                master = self.master,
                home_page = self,
                ticker = ticker,
                shares = shares,
                date = date
            )

class SellFrame(TransactionFrame) :
    def __init__(self, master, market, portfolio) :
        super(SellFrame, self).__init__(master, market, portfolio)

        shares_kwargs = {
            'ticker' : self.ticker.get(),
            'effective_date' : dt.datetime.strptime(self.transaction_date.get(),'%Y-%m-%d').date()
        }

        # Configure Label Widget.
        self.transaction_label.config(text = 'Sell')

        # Configure Spinbox Widget.
        self.shares.config(values = self.get_possible_shares(**shares_kwargs))

        # Update Possible Shares When Date and Ticker Changes.
        self.ticker.bind("<Button-1>", self.update_ticker)
        self.transaction_date.bind("<Button-1>", self.update_date)

    def get_possible_shares(self, **kwargs) :
        max_shares = self.portfolio.max_shares(ticker = kwargs['ticker'], effective_date = kwargs['effective_date'])

        return [i for i in range(max_shares + 1)]

    def update_shares(self, ticker, date) :
        shares_kwargs = {
            'ticker' : ticker,
            'effective_date' : date
        }

        self.shares.delete(0, tk.END)
        self.shares.config(values = self.get_possible_shares(**shares_kwargs))

    def update_ticker(self, event) :
        index = self.portfolio_tickers.index(self.ticker.get())

        if (event.x >= 145) :
            if (event.y < 12 and index < (len(self.portfolio_tickers) - 1)) :
                index += 1
            elif (index > 0) :
                index -= 1
            self.update_shares(
                ticker = self.portfolio_tickers[index],
                date = dt.datetime.strptime(self.transaction_date.get(),'%Y-%m-%d').date()
            )

    def update_date(self, event) :
        index = self.dates.index(dt.datetime.strptime(self.transaction_date.get(),'%Y-%m-%d').date())

        if (event.x >= 145) :
            if (event.y < 12 and index < (len(self.dates) - 1)) :
                index += 1
            elif (index > 0) :
                index -= 1
            self.update_shares(
                ticker = self.ticker.get(),
                date = self.dates[index]
            )

    def confirm_transaction(self, ticker, shares, date) :
        if not hasattr(self, "confirm_sell_window") or not self.confirm_sell_window.winfo_exists() :
            self.confirm_sell_window = ConfirmSellWindow(
                master = self.master,
                home_page = self,
                ticker = ticker,
                shares = shares,
                date = date
            )

class ConfirmTransactionWindow(ConfirmationWindow) :
    def __init__(self, master, message, home_page, ticker, shares, date) :
        super(ConfirmTransactionWindow, self).__init__(
            master = master,
            message = message
        )

        self.home_page = home_page

        self.confirmButton.config(
            command = lambda : self.confirm(
                ticker = ticker,
                shares = shares,
                adj_closes = self.home_page.market.get_adjcloses(),
                date = date
            )
        )

    def confirm(self, ticker, shares, adj_closes, date) :
        self.destroy()

class ConfirmBuyWindow(ConfirmTransactionWindow) :
    def __init__(self, master, home_page, ticker, shares, date) :
        super(ConfirmBuyWindow, self).__init__(
            master = master,
            message = f'You will buy {shares} shares of {ticker}.',
            home_page = home_page,
            ticker = ticker,
            shares = shares,
            date = date
        )

    def confirm(self, ticker, shares, adj_closes, date) :
        self.master.portfolio.buy_shares(ticker, shares, adj_closes, date)
        self.master.display_portfolio(adj_closes)
        self.destroy()

class ConfirmSellWindow(ConfirmTransactionWindow) :
    def __init__(self, master, home_page, ticker, shares, date) :
        super(ConfirmSellWindow, self).__init__(
            master = master,
            message = f'You will sell {shares} shares of {ticker}.',
            home_page = home_page,
            ticker = ticker,
            shares = shares,
            date = date
        )

    def confirm(self, ticker, shares, adj_closes, date) :
        self.master.portfolio.sell_shares(ticker, shares, adj_closes, date)
        self.master.display_portfolio(adj_closes)
        self.destroy()