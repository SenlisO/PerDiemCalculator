from bank import Accountant, InvalidOperationError, UserQuitException
from tkinter import Tk, Frame, Label, Button, RIGHT, BOTTOM, TOP, END, Listbox, Entry
from decimal import Decimal, getcontext
import datetime


# todo: go through all files and only import what is necessary

class GUI:
    def __init__(self, load_data):
        self.bill = Accountant() # bill is our accountant.  He is the person we make all financial requests to

        # loads all data
        if load_data:  # flag controls whether program automatically loads data
            try:
                self.bill.load_data()
            except InvalidOperationError:  # exception is raised when file is not found
                self.last_error = "Note: Ledger file not found.  Starting fresh database"
            except IndexError: #exception is raised when file is corrupted
                self.last_error = "Error: Ledger file corrupted."

        getcontext().prec = 2 # function of decimal class to control decimal precision

        # create the root window
        root = Tk()
        root.title("Per Diem Tracker")

        w = 380 # width for the Tk root
        h = 200 # height for the Tk root

        # get screen width and height
        ws = root.winfo_screenwidth() # width of the screen
        hs = root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen
        # and where it is placed
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # define all objects
        top_frame = Frame(root)  # for buttons
        middle_frame = Frame(root) # for list of Transactions
        bottom_frame = Frame(root) # for error window

        self.transactions = Listbox(middle_frame)
        self.errors = Label(bottom_frame, text="no errors")

        add_button = Button(top_frame, text = "Add Transaction", command=self.add_transaction)
        save_button = Button(top_frame, text = "Save")
        clear_button = Button(top_frame, text = "Clear Data")
        load_button = Button(top_frame, text = "Load Data")

        # pack everything
        load_button.pack(side=RIGHT)
        save_button.pack(side=RIGHT)
        clear_button.pack(side=RIGHT)
        add_button.pack(side=RIGHT)

        self.transactions.pack()

        self.transactions.insert(END, "Test") # this is test data
        self.populate_transactions_list()

        self.errors.pack()

        # finall, pack the two frames using grid layout
        top_frame.grid(row = 0)
        middle_frame.grid(row = 1)
        bottom_frame.grid(row = 2)

        root.mainloop() # this keeps our UI running

    def populate_transactions_list(self):
        # check if we have any transactions
        if self.bill.num_transactions() < 1:
            return

        for transaction in range(1, self.bill.num_transactions()):
            pass

        # finish method here
        return

    def add_transaction(self):
        # create a new window
        root = Tk()
        root.title("Add a Transaction")

        main_frame = Frame(root)

        w = 280 # width for the Tk root
        h = 120 # height for the Tk root

        # get screen width and height
        ws = root.winfo_screenwidth() # width of the screen
        hs = root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen
        # and where it is placed
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # create all objects
        date_label = Label(main_frame, text = "Date:")
        name_label = Label(main_frame, text = "Name:")
        amount_label = Label(main_frame, text = "Amount:")
        remarks_label = Label(main_frame, text = "Remarks:")

        self.date_entry = Entry(main_frame)
        self.name_entry = Entry(main_frame)
        self.amount_entry = Entry(main_frame)
        self.remarks_entry = Entry(main_frame)

        submit_button = Button(main_frame, text = "Submit", command = self.submit_transaction(root))
        cancel_button = Button(main_frame, text = "Cancel", command = root.destroy)

        date_label.grid(row = 0, column = 0)
        self.date_entry.grid(row= 0, column = 1)
        name_label.grid(row = 1, column = 0)
        self.name_entry.grid(row = 1, column = 1)
        amount_label.grid(row = 2, column = 0)
        self.amount_entry.grid(row = 2, column = 1)
        remarks_label.grid(row = 3, column = 0)
        self.remarks_entry.grid(row = 3, column = 1)
        submit_button.grid(row = 4, column = 0)
        cancel_button.grid(row = 4, column = 1)

        main_frame.pack()

        root.mainloop()

    def submit_transaction(self, root):
        date = self.date_entry.get()

        try:
            formatted_date = datetime.date(int(date[:4]), int(date[4:6]), int(date[6:]))
        except (ValueError): # in case we got bad data
            self.errors.text = "Invalid date format" # todo: this is not executing correctly
            root.destroy
