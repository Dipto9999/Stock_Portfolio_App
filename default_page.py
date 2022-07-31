########################################
############## Modules #################
########################################

import tkinter as tk
from tkinter.font import Font
from tkinter import ttk

######################################
############## Classes ###############
######################################

class DefaultPage(tk.Frame) :
    def __init__(self, frame, master) :
        # Initialize Frame.
        tk.Frame.__init__(self, frame)

        master.title('Stock Portfolio')
        master.iconbitmap('Images\Icons\Stocks.ico')

        self.config(bg = 'black')

        # TTK Colors and Fonts.
        self.button_bg = '#0D4BC5'
        self.button_font = Font(family = 'Arial', size = 12, weight = 'bold')

        self.heading_label_bg = '#0076CE'
        self.heading_label_font = Font(family = 'Ubuntu Mono', size = 12, weight = 'bold')

        self.general_label_bg = '#0076CE'
        self.general_label_font = Font(family = 'Ubuntu Mono', size = 10, weight = 'normal')

        self.general_entry_bg = '#6699CC'
        self.general_entry_font = Font(family = 'Ubuntu Mono', size = 10, weight = 'normal')

class DefaultWindow(tk.Toplevel) :
    def __init__(self, home_page) :
        # Can Initialize GUI Implicitly.
        super().__init__()

        self.iconbitmap('Images\Icons\Stocks.ico')
        self.config(bg = 'black')

        # TTK Colors and Fonts.
        self.button_bg = '#0D4BC5'
        self.button_font = Font(family = 'Arial', size = 12, weight = 'bold')

        self.heading_label_bg = '#0076CE'
        self.heading_label_font = Font(family = 'Ubuntu Mono', size = 12, weight = 'bold')

        self.general_label_bg = '#0076CE'
        self.general_label_font = Font(family = 'Ubuntu Mono', size = 10, weight = 'normal')

        self.general_entry_bg = '#6699CC'
        self.general_entry_font = Font(family = 'Ubuntu Mono', size = 10, weight = 'normal')

class DefaultRecordsWindow(DefaultWindow) :
    def __init__(self, home_page) :
        super(DefaultRecordsWindow, self).__init__(home_page)

        self.title('Records')
        self.iconbitmap('Images/Icons/Stocks.ico')
        self.config(bg = 'black')

        # Retrieve Table Data.
        self.column_to_organize = str(home_page.order_information.get())

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
        self.treeview_style.configure(
            'display_style.Treeview',
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
