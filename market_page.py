########################################
############## Modules #################
########################################

from default_page import *
from portfolio import Portfolio
from market import Market

######################################
############## Classes ###############
######################################

class MarketPage(DefaultPage) :
    def __init__(self, frame, master, market, portfolio) :
        super(MarketPage, self).__init__(frame, master)
