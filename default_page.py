########################################
############## Modules #################
########################################

from constants import *

import tkinter as tk
from tkinter.font import Font
from tkinter import ttk

######################################
############## Classes ###############
######################################

class DefaultFrame(tk.Frame) :
    def __init__(self, master) :
        # Initialize Frame.
        tk.Frame.__init__(self, master)

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

class DefaultPage(DefaultFrame) :
    def __init__(self, frame, master) :
        # Initialize Frame.
        super(DefaultPage, self).__init__(frame)

        self.master = master

        self.master.title('Stock Portfolio')
        self.master.iconbitmap('Images\Icons\Stocks.ico')

class DefaultWindow(tk.Toplevel) :
    def __init__(self) :
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

class ConfirmationWindow(DefaultWindow) :
    def __init__(self, master, message) :
        super(ConfirmationWindow, self).__init__()

        self.master = master

        self.title('Confirmation')

        ##########################
        ### Confirmation Frame ###
        ##########################

        # Create and Configure Frame.
        self.confirmation_frame = tk.Frame(self)
        self.confirmation_frame.configure(bg = 'white')

        # Position Frame.
        self.confirmation_frame.pack(padx = 5, pady = (5,10))

        # Create Label Widget.
        self.confirmation_label = tk.Label(self.confirmation_frame,
            text = message,
            bg = 'white', fg = 'black', font = self.general_label_font, relief = 'flat', justify = tk.LEFT
        )

        # Create Button Widgets.
        self.confirmButton = tk.Button(
            self.confirmation_frame, text = 'Confirm', bg = self.button_bg, fg = 'white',
            font = self.button_font, borderwidth = 2, relief = 'raised',
            command = self.confirm
        )
        self.abortButton = tk.Button(
            self.confirmation_frame, text = 'Abort', bg = '#232023', fg = 'white',
            font = self.button_font, borderwidth = 2, relief = 'raised', command = self.destroy
        )

        # Position Widgets.
        self.confirmation_label.grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = (0, 5), sticky = tk.N + tk.E + tk.S + tk.W)

        self.confirmButton.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.W)
        self.abortButton.grid(row = 1, column = 1, padx = (0, 5), pady = 5, sticky = tk.E)

    def confirm(self) :
        pass

class DefaultRecordsWindow(DefaultWindow) :
    def __init__(self, home_page) :
        super(DefaultRecordsWindow, self).__init__()

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
