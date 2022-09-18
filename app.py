########################################
############## Modules #################
########################################

from constants import *

from registration_page import RegistrationPage
from portfolio_page import PortfolioPage
from market_page import MarketPage

from market import Market
from portfolio import Portfolio

import datetime as dt
from functools import partial

import tkinter as tk

######################################
############## Classes ###############
######################################

class GUI(tk.Tk) :
    def __init__(self) :
        # Can Initialize GUI Implicitly.
        super().__init__()

        name = Portfolio.get_name_record()
        tickers = Market.get_ticker_records()
        days = (dt.datetime.today().date() - Market.get_creation_date()).days

        # Create Portfolio When Application is Opened.
        self.market = Market(tickers = tickers, days = days)
        self.portfolio = Portfolio(name = name, tickers = tickers, days = days)

        self.config(bg = 'black')

        self.resizable(height = True, width = True)

        # Add Menu Bar to Application.
        self.toplevel_menu = tk.Menu(self)
        self.config(menu = self.toplevel_menu)

        # Add Pages Cascade.
        self.pages_menu = tk.Menu(self.toplevel_menu)
        self.toplevel_menu.add_cascade(label = 'Pages', menu = self.pages_menu)

        # Call Functions to Change Pages.
        self.landing_page = REGISTRATION_PAGE if (Portfolio.get_name_record() == 'NA') else PORTFOLIO_PAGE
        self.menu_labels = {
            REGISTRATION_PAGE : 'New Portfolio',
            PORTFOLIO_PAGE : 'View Portfolio',
            MARKET_PAGE : 'View Market'
        }

        for key, page_label in self.menu_labels.items() :
            self.pages_menu.add_command(label = page_label, command = partial(self.openPage, key))

        if (self.portfolio.get_name() == 'NA') :
            self.pages_menu.entryconfig(index = 'View Portfolio', state = 'disabled')
            self.pages_menu.entryconfig(index = 'View Market', state = 'disabled')

        self.toplevel_frame = tk.Frame(self)

        self.toplevel_frame.pack(
            side = 'top',
            fill = 'both',
            expand = True
        )

        # Configure Rows and Columns to be Uniform in Application.
        self.toplevel_frame.grid_rowconfigure(0, weight = 1)
        self.toplevel_frame.grid_columnconfigure(0, weight = 1)

        # Initialize Dictionaries With Page Classes.
        self.pages = {}
        for Page in (RegistrationPage, PortfolioPage, MarketPage) :
            self.current_page = Page(frame = self.toplevel_frame, master = self, market = self.market, portfolio = self.portfolio)

            self.pages[Page.__name__] = self.current_page

            # Must Use Grid System for Positioning Pages on Window.
            self.current_page.grid(row = 0, column = 0, sticky = 'nsew')

        self.openPage(self.landing_page)

    def openPage(self, page_name) :
        # Show a Frame for the Given Page.
        self.current_page = self.pages[page_name]
        self.current_page.tkraise()

        # Configure Page Geometry.
        if (page_name == REGISTRATION_PAGE) :
            self.geometry("450x250")
        else :
            self.geometry("950x350")

        if (page_name == PORTFOLIO_PAGE) :
            self.current_page.display_portfolio(self.market.get_adjcloses())

        self.refreshMenu(page_name)

    def refreshMenu(self, page_name) :
        # Configure Menu Commands.
        for key, page_label in self.menu_labels.items() :
            if (key == page_name or Portfolio.get_name_record() == 'NA') :
                self.pages_menu.entryconfig(index = page_label, state = 'disabled')
            else :
                self.pages_menu.entryconfig(index = page_label, state = 'normal')

###################################
############## Main ###############
###################################

if __name__ == '__main__' :
    gui = GUI()
    gui.mainloop()