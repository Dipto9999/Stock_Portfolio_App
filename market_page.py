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

        #########################
        ### Market Data Frame ###
        #########################

        # Create Frames.
        self.market_data_frame = tk.Frame(self)

class DefaultRecordsFrame(DefaultFrame) :
    def __init__(self, home_page) :
        super(DefaultRecordsFrame, self).__init__(home_page)

        # Retrieve Table Data.
        self.column_to_organize  = str(home_page.order_information.get())

        # Create, Position, and Configure Frame.
        self.db_records_frame = tk.Frame(self)
        self.db_records_frame.pack(pady = 20)
        self.db_records_frame.config(bg = 'black')

        # Create and Position Text Label.
        self.records_data_label = tk.Label(self.db_records_frame, text = 'Records Data',
            bg = self.general_label_bg, fg = 'black', font = self.general_label_font, borderwidth = 5, anchor = tk.E)
        self.records_data_label.pack(padx = 5, pady = 10)

        ### Treeview Style ###

        # Create a Treeview Style.
        self.treeview_style = ttk.Style()
        # Treeview Body Style.
        self.treeview_style.configure('display_style.Treeview',
            highlightthickness = 2, bd = 2, font = self.general_entry_font,
            background = 'lightblue', foreground = 'black', rowheight = 25, fieldbackground = 'silver'
        )
        # Treeview Heading Style.
        self.treeview_style.configure(
            'display_style.Treeview.Heading',
            highlightthickness = 5, bd = 5, font = self.general_label_font,
            background = 'lightgreen', foreground = 'black', rowheight = 25, fieldbackground = 'silver'
        )
        # Change Color of Selected Row.
        self.treeview_style.map('display_style.Treeview', background = [('selected', 'white')])

        ### Treeview ###

        # Create and Position Scrollbar for Treeview.
        self.tree_scroll = tk.Scrollbar(self.db_records_frame)
        self.tree_scroll.pack(side = tk.RIGHT, fill = tk.Y)
        # Create Treeview.
        self.records_tree = ttk.Treeview(
            self.db_records_frame,
            yscrollcommand = self.tree_scroll.set,
            style = 'display_style.Treeview'
        )
        # Configure Scrollbar for Treeview.
        self.tree_scroll.config(command = self.records_tree.yview)

class EmployeesRecordsWindow(DefaultRecordsWindow) :
    def __init__(self, home_page) :
        super(EmployeesRecordsWindow, self).__init__(home_page)

        self.title('Employee Information')
        self.records_df = db.show_all_records(self.column_to_organize)

        # Configure Text Label.
        self.records_data_label.config(text = 'Employee Data')

        # Assign Treeview Column Headings.
        self.records_tree['column'] = list(self.records_df.columns)
        self.records_tree['show'] = 'headings'
        for column in self.records_tree['column'] :
            self.records_tree.heading(column, text = column)
        # Assign Treeview Rows.
        records_df_rows = self.records_df.to_numpy().tolist()
        for current_row in records_df_rows :
            self.records_tree.insert('', tk.END, values = current_row)

        self.records_tree.pack()