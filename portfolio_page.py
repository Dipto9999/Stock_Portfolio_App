########################################
############## Modules #################
########################################

from default_page import *
from portfolio import Portfolio
from market import Market

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

######################################
############## Classes ###############
######################################

class PortfolioPage(DefaultPage) :
    def __init__(self, frame, master, market, portfolio, name) :
        super(PortfolioPage, self).__init__(frame, master)

        ###########################
        ### New Portfolio Frame ###
        ###########################

        # Create Frames.
        self.display_portfolio_frame = tk.Frame(self)
        self.buy_stocks_frame = tk.Frame(self)
        self.sell_stocks_frame = tk.Frame(self)

        # Position Frames.
        self.display_portfolio_frame.grid(row = 0, column = 0, rowspan = 2, padx = 5, pady = (5,10))
        self.buy_stocks_frame.grid(row = 0, column = 1, padx = 5, pady = (5,10))
        self.sell_stocks_frame.grid(row = 1, column = 1, padx = 5, pady = (5,10))

        self.display_portfolio_frame.configure(bg = 'white')
        self.buy_stocks_frame.configure(bg = 'white')
        self.sell_stocks_frame.configure(bg = 'white')

        fig_portfolio = portfolio.display_portfolio(adj_closes = market.get_adjcloses(), name = name)

        current_portfolio = FigureCanvasTkAgg(fig_portfolio, self.display_portfolio_frame)
        current_portfolio.get_tk_widget().pack(side = tk.LEFT, fill = tk.BOTH)
