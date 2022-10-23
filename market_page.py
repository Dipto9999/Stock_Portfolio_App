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
        super(MarketPage, self).__init__(frame, master, market, portfolio)

        # Create Frames.
        self.market_records_frame = MarketRecordsFrame(master = self, market = market)
        self.historical_data_frame = tk.Frame(self)
        self.add_ticker_frame = tk.Frame(self)

        # Position Frames.
        self.market_records_frame.grid(row = 0, column = 0, rowspan = 1, padx = 5, pady = (5,10))
        self.historical_data_frame.grid(row = 0, column = 1, padx = 5, pady = (5,10), sticky = tk.E + tk.W + tk.N + tk.S)
        self.add_ticker_frame.grid(row = 1, column = 1, padx = 5)

        # Configure Frames.
        self.market_records_frame.configure(bg = self.market_records_frame.general_treeview_bg)
        self.historical_data_frame.configure(bg = 'white')
        self.add_ticker_frame.configure(bg = 'white')

        ###############################
        ### Historical Trends Frame ###
        ###############################

        # Create Label Widgets.
        self.historical_data_label = tk.Label(self.historical_data_frame, text = 'Historical Data',
            bg = self.heading_label_bg, fg = 'black', font = self.heading_label_font, borderwidth = 2, relief = 'solid', anchor = tk.W)

        self.ticker_label = tk.Label(self.historical_data_frame, text = 'Ticker : ',
            bg = self.general_label_bg, fg = 'black', font = self.general_label_font, borderwidth = 1, relief = 'solid', anchor = tk.W)
        self.days_label = tk.Label(self.historical_data_frame, text = 'Days : ',
            bg = self.general_label_bg, fg = 'black', font = self.general_label_font, borderwidth = 1, relief = 'solid', anchor = tk.W)

        self.duplicate_rsi_label = tk.Label(self.add_ticker_frame, text = 'Historical Data',
            bg = self.heading_label_bg, fg = 'black', font = self.heading_label_font, borderwidth = 2, relief = 'solid', anchor = tk.W)

        self.duplicate_ticker_label = tk.Label(self.add_ticker_frame, text = 'Ticker : ',
            bg = self.general_label_bg, fg = 'black', font = self.general_label_font, borderwidth = 1, relief = 'solid', anchor = tk.W)
        self.duplicate_days_label = tk.Label(self.add_ticker_frame, text = 'Days : ',
            bg = self.general_label_bg, fg = 'black', font = self.general_label_font, borderwidth = 1, relief = 'solid', anchor = tk.W)

        # Create Spinbox Entry Widgets.
        # self.rsi_ticker =

        self.historical_data_label.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.W)

        self.ticker_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.W)
        self.days_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tk.W)

        self.duplicate_rsi_label.grid(row = 0, column = 0, padx = 5, pady = (0, 5), sticky = tk.W)

        self.duplicate_ticker_label.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.W)
        self.duplicate_days_label.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tk.W)

class MarketRecordsFrame(DefaultRecordsFrame) :
    def __init__(self, master, market) :
        super(MarketRecordsFrame, self).__init__(master)

        ### Treeview ###

        # Create and Position Horizontal Scrollbar for Treeview.
        self.tree_scroll_x = tk.Scrollbar(self.table_data_frame, orient = tk.HORIZONTAL)
        self.tree_scroll_x.pack(side = tk.BOTTOM, fill = tk.X)

        # Create and Position Vertical Scrollbar for Treeview.
        self.tree_scroll_y = tk.Scrollbar(self.table_data_frame, orient = tk.VERTICAL)
        self.tree_scroll_y.pack(side = tk.RIGHT, fill = tk.Y)

        # Create Treeview.
        self.records_tree = ttk.Treeview(
            self.table_data_frame,
            xscrollcommand = self.tree_scroll_x.set,
            yscrollcommand = self.tree_scroll_y.set,
            style = 'display_style.Treeview',
        )

        # Configure Scrollbars for Treeview.
        self.tree_scroll_x.config(command = self.records_tree.xview)
        self.tree_scroll_y.config(command = self.records_tree.yview)

        # Configure DataFrame for Treeview.
        self.market = market
        self.market_df = self.market.adj_closes
        self.market_df['Date'] = self.market_df.index

        market_df_cols = self.market_df.columns.tolist()
        market_df_cols = market_df_cols[-1:] + market_df_cols[:-1]

        self.market_df = self.market_df[market_df_cols]

        # Configure Text Label.
        self.table_data_label.config(text = 'Market Data')

        # Assign Treeview Column Headings.
        self.records_tree['column'] = list(self.market_df.columns)
        self.records_tree['show'] = 'headings'

        for column in self.records_tree['column'] :
            self.records_tree.heading(column, text = column)

            if column == 'Date' :
                self.records_tree.column(column, minwidth = 0, width = 100, stretch = tk.NO)
            else :
                self.records_tree.column(column, minwidth = 0, width = 50, stretch = tk.NO)

        # Assign Treeview Rows.
        market_df_rows = self.market_df.to_numpy().tolist()
        for current_row in market_df_rows :
            self.records_tree.insert('', tk.END, values = current_row)

        self.records_tree.pack()
