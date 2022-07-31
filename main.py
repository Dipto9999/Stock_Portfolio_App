########################################
############## Modules #################
########################################

import tkinter as tk

from landing_page import LandingPage
from portfolio_page import PortfolioPage
from market_page import MarketPage

########################################
############## Constants ###############
########################################

LANDING_PAGE = 'LandingPage'

######################################
############## Classes ###############
######################################

class GUI(tk.Tk) :
    def __init__(self) :
        # Can Initialize GUI Implicitly.
        super().__init__()

        self.config(bg = 'black')

        # Add Menu Bar to Application.
        self.toplevel_menu = tk.Menu(self)
        self.config(menu = self.toplevel_menu)

        # Add Pages Cascade.
        self.pages_menu = tk.Menu(self.toplevel_menu)
        self.toplevel_menu.add_cascade(label = 'Pages', menu = self.pages_menu)

        # Call Functions to Change Pages.
        self.pages_menu.add_command(label = 'View Portfolio', command = lambda: self.openPage('PortfolioPage'))
        self.pages_menu.add_command(label = 'View Market', command = lambda: self.openPage('MarketPage'))

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
        for Page in (LandingPage, PortfolioPage, MarketPage) :
            self.current_page = Page(frame = self.toplevel_frame, master = self)

            self.pages[Page.__name__] = self.current_page

            # Must Use Grid System for Positioning Pages on Window.
            self.current_page.grid(row = 0, column = 0, sticky = 'nsew')

        self.openPage(LANDING_PAGE)

    def openPage(self, page_name) :
        # Show a Frame for the Given Page.
        self.current_page = self.pages[page_name]
        self.current_page.tkraise()

###################################
############## Main ###############
###################################

if __name__ == '__main__' :
    gui = GUI()

    gui.mainloop()