########################################
############## Modules #################
########################################

from default_page import *
from portfolio import Portfolio
from market import Market

import datetime as dt

######################################
############## Classes ###############
######################################

class LandingPage(DefaultPage) :
    def __init__(self, frame, master, market, portfolio, name) :
        super(LandingPage, self).__init__(frame, master)

        self.market = market
        self.portfolio = portfolio

        ###########################
        ### New Portfolio Frame ###
        ###########################

        # Create Frames.
        self.new_portfolio_frame = tk.Frame(self)

        # Position Frames.
        self.new_portfolio_frame.pack(padx = 5, pady = (5,10))

        # Create Label Widgets.
        self.new_portfolio_label = tk.Label(self.new_portfolio_frame, text = 'New Portfolio',
            bg = self.heading_label_bg, fg = 'black', font = self.heading_label_font, borderwidth = 2, relief = 'solid', anchor = tk.W)
        self.first_name_label = tk.Label(self.new_portfolio_frame, text = 'First Name : ',
            bg = self.general_label_bg, fg = 'black', font = self.general_label_font, borderwidth = 1, relief = 'solid', anchor = tk.W)
        self.last_name_label = tk.Label(self.new_portfolio_frame, text = 'Last Name : ',
            bg = self.general_label_bg, fg = 'black', font = self.general_label_font, borderwidth = 1, relief = 'solid', anchor = tk.W)
        self.email_address_label = tk.Label(self.new_portfolio_frame, text = 'Email Address : ',
            bg = self.general_label_bg, fg = 'black', font = self.general_label_font, borderwidth = 1, relief = 'solid', anchor = tk.W)
        self.phone_number_label = tk.Label(self.new_portfolio_frame, text = 'Phone Number : ',
            bg = self.general_label_bg, fg = 'black', font = self.general_label_font, borderwidth = 1, relief = 'solid', anchor = tk.W)

        # Create Text Entry Widgets.
        self.first_name = tk.Entry(self.new_portfolio_frame, bg = self.general_entry_bg, fg = 'black',
            font = self.general_entry_font, borderwidth = 2, relief = 'sunken')
        self.last_name = tk.Entry(self.new_portfolio_frame, bg = self.general_entry_bg, fg = 'black',
            font = self.general_entry_font, borderwidth = 2, relief = 'sunken')
        self.email_address = tk.Entry(self.new_portfolio_frame, bg = self.general_entry_bg, fg = 'black',
            font = self.general_entry_font, borderwidth = 2, relief = 'sunken')
        self.phone_number = tk.Entry(self.new_portfolio_frame, bg = self.general_entry_bg, fg = 'black',
            font = self.general_entry_font, borderwidth = 2, relief = 'sunken')

        # Create Button Widget.
        self.submitButton = tk.Button(self.new_portfolio_frame, text = 'Submit', bg = self.button_bg, fg = 'white',
            font = self.button_font, borderwidth = 2, relief = 'raised', command = lambda : self.add_portfolio(STANDARD_TICKERS, CREATION_DAYS))

        # Default Text For Entry Widgets.
        self.first_name.insert(0, 'First Name')
        self.last_name.insert(0, 'Last Name')
        self.email_address.insert(0, '_______@____.com')
        self.phone_number.insert(0, '+1(XXX)-XXX-XXXX')

        # Create and Configure Label Widgets.
        self.new_portfolio_label.config(text = 'New Portfolio')
        self.creation_date_label = tk.Label(self.new_portfolio_frame, text = 'Creation Date : ',
            bg = self.general_label_bg, fg = 'black', font = self.general_label_font, borderwidth = 1, relief = 'solid',  anchor = tk.E)

        # Create Spinbox Entry Widget.
        effective_dates = [(dt.datetime.today() - dt.timedelta(effective_days)).date() for effective_days in range(CREATION_DAYS, -1, -1)]
        self.creation_date = tk.Spinbox(self.new_portfolio_frame, values = tuple(effective_dates),
            bg = self.general_entry_bg, fg = 'black', font = self.general_entry_font, borderwidth = 2, relief = 'sunken')

        # Position Widgets.
        self.new_portfolio_label.grid(row = 0, column = 0, padx = 5, pady = (0, 5), sticky = tk.W)
        self.first_name_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.W)
        self.first_name.grid(row = 1, column = 1, padx = (0, 5), pady = 5, sticky = tk.W)

        self.last_name_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tk.W)
        self.last_name.grid(row = 2, column = 1, padx = (0, 5), pady = 5, sticky = tk.W)

        self.email_address_label.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = tk.W)
        self.email_address.grid(row = 3, column = 1, padx = (0, 5), pady = 5, sticky = tk.W)

        self.phone_number_label.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = tk.W)
        self.phone_number.grid(row = 4, column = 1, padx = (0, 5), pady = 5, sticky = tk.W)

        self.creation_date_label.grid(row = 5, column = 0, padx = 5, pady = 5, sticky = tk.W)
        self.creation_date.grid(row = 5, column = 1, padx = (0, 5), pady = 5, sticky = tk.W)

        self.submitButton.grid(row = 6, column = 2, padx = 10, pady = 10, sticky = tk.E)

    def add_portfolio(self, tickers, days) :
        if not Portfolio.records_exist() :
            self.portfolio = Portfolio(tickers = tickers, days = days)
        if not hasattr(self, "confirm_destroy_portfolio") or not self.confirm_destroy_portfolio.winfo_exists() :
            self.confirm_destroy_portfolio = ConfirmPortfolioWindow(self, name = self.first_name.get(), tickers = tickers, days = days)

class ConfirmPortfolioWindow(DefaultWindow) :
    def __init__(self, home_page, name, tickers, days) :
        super(ConfirmPortfolioWindow, self).__init__(home_page)

        self.title('New Portfolio')

        ###########################
        ### New Portfolio Frame ###
        ###########################

        # Create Frames.
        self.confirmation_frame = tk.Frame(self)
        self.confirmation_frame.configure(bg = 'white')

        # Position Frames.
        self.confirmation_frame.pack(padx = 5, pady = (5,10))

        # Create Label Widgets.
        self.confirmation_label = tk.Label(self.confirmation_frame,
            text = f'Hi {name},\nYou will destroy the existing portfolio.',
            bg = 'white', fg = 'black', font = self.general_label_font, relief = 'flat', justify = tk.LEFT
        )

        # Create Button Widget.
        self.confirmButton = tk.Button(self.confirmation_frame, text = 'Confirm', bg = self.button_bg, fg = 'white',
            font = self.button_font, borderwidth = 2, relief = 'raised', command = lambda : self.add_portfolio(tickers = tickers, days = days))
        self.abortButton = tk.Button(self.confirmation_frame, text = 'Abort', bg = '#232023', fg = 'white',
            font = self.button_font, borderwidth = 2, relief = 'raised', command = self.destroy)

        # Position Widgets.
        self.confirmation_label.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = (0, 5), sticky = tk.N + tk.E + tk.S + tk.W)

        self.confirmButton.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.W)
        self.abortButton.grid(row = 1, column = 1, padx = (0, 5), pady = 5, sticky = tk.E)

    def add_portfolio(self, tickers, days) :
        self.market.reset(tickers = tickers, days = days)
        self.portfolio.reset(tickers = tickers, days = days)

        self.destroy()