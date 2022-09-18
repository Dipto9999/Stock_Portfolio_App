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
    def __init__(self, frame, master, market, portfolio) :
        # Initialize Frame.
        super(DefaultPage, self).__init__(frame)

        self.master = master

        self.market = market
        self.portfolio = portfolio

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
        self.confirmation_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = tk.E + tk.W+ tk.N + tk.S)

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

        self.confirmButton.grid(row = 1, column = 0, padx = 1, pady = 1)
        self.abortButton.grid(row = 1, column = 1, padx = 1, pady = 1)

    def confirm(self) :
        pass

class DefaultRecordsFrame(DefaultFrame) :
    def __init__(self, master) :
        super(DefaultRecordsFrame, self).__init__(master)

        # TTK Colors and Fonts.
        self.heading_treeview_bg = '#05445E'
        self.heading_treeview_font = Font(family = 'Ubuntu Mono', size = 10, weight = 'bold')

        self.general_treeview_bg = '#a9a9a9'
        self.general_treeview_font = Font(family = 'Ubuntu Mono', size = 10, weight = 'normal')

        # Create, Position, and Configure Frame.
        self.table_data_frame = tk.Frame(self)
        self.table_data_frame.grid(row = 0, column = 0, rowspan = 2, padx = 5, pady = (5,10))
        self.table_data_frame.configure(bg = self.general_treeview_bg)

        # Create and Position Text Label.
        self.table_data_label = tk.Label(self.table_data_frame, text = 'Table Data',
            bg = self.heading_label_bg, fg = 'black',
            font = self.heading_label_font, borderwidth = 2, relief = 'solid', anchor = tk.E
        )
        self.table_data_label.pack(padx = 5, pady = 10)

        ### Treeview Style ###

        # Create a Treeview Style.
        self.treeview_style = ttk.Style()
        self.treeview_style.theme_use('winnative')

        # Treeview Body Style.
        self.treeview_style.configure('display_style.Treeview',
            highlightthickness = 2, bd = 2, font = self.general_treeview_font,
            background = self.general_treeview_bg, foreground = 'black', fieldbackground = 'silver', rowheight = 25
        )
        # Treeview Heading Style.
        self.treeview_style.configure(
            'display_style.Treeview.Heading',
            highlightthickness = 5, bd = 2, font = self.heading_treeview_font,
            background = self.heading_treeview_bg, foreground = 'white', fieldbackground = 'silver', rowheight = 25
        )

        # Change Color of Selected Row.
        self.treeview_style.map(
            'display_style.Treeview',
            background = [('selected', 'lightblue')],
            foreground = [('selected', 'black')]
        )
