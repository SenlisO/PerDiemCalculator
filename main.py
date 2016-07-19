import os
from datetime import date, timedelta


class InvalidOperationError(Exception):  # exception class
    def __init__(self, message):
        self.message = message


class Bank:
    # Class contains transaction and perdiem data and performs operations on them
    def __init__(self):
        self.begin_date = date(1950, 1, 1)  # begin date of travel, new years 2000 indicates no data
        self.end_date = date(1950, 1, 1)  # end date of travel, new years 2000 indicates no data
        self.travel_per_diem = 0  # per diem for travel days
        self.daily_per_diem = 0  # per diem for normal days
        self.transactions = []

    def set_per_diem_data(self, begin_date, end_date, travel_per_diem, daily_per_diem):
        # sanitize date values
        if not isinstance(begin_date, date) or not isinstance(end_date, date):
            raise InvalidOperationError("Debug error: dates provided to Bank.setperdiemdata are not correct type")
        if end_date <= begin_date:
            raise InvalidOperationError("Debug error: Bank.setperdiemdata: end date is <= to begin date")

        # sanitize per diem values
        if not isinstance(travel_per_diem, float) or not isinstance(daily_per_diem, float):
            raise InvalidOperationError("Debug error: Bank.setperdiemdata: per_diem data provided are not floats")
        if travel_per_diem < 0 or daily_per_diem < 0:
            raise InvalidOperationError("Debug error: Bank.setperdiemdata: per_diem data not valid")

        # set class attributes
        self.begin_date = begin_date
        self.end_date = end_date
        self.travel_per_diem = travel_per_diem
        self.daily_per_diem = daily_per_diem

    def calculate_tdy_duration(self):
        # usage: returns the difference between TDY begin and end dates
        # first, check to ensure Bank's values have been set
        if not self.is_initialized():
            raise InvalidOperationError("Debug error: Operations on Bank executed before values initialized")

        # then, make calculation and return result
        return self.end_date - self.begin_date

    def is_initialized(self):
        # usage: determine if Bank has been given any updates to its original values
        if self.begin_date == date(1950, 1, 1):
            return False
        else:
            return True

    def calculate_per_diem_total(self):
        # usage: calculate total per diem dollar amount
        total = self.travel_per_diem * 2
        duration = self.calculate_tdy_duration()
        total += (duration.days - 2) * self.daily_per_diem
        return total

    def add_transaction(self, name, transaction_date, amount, remarks):
        try:
            self.transactions.append(Transaction(name, transaction_date, amount, remarks))
        except InvalidOperationError as e:
            print(e)

        self.transactions = sorted(self.transactions, key=lambda Transaction: Transaction.transaction_date)


class Transaction:
    # Class contains data for individual transactions
    # Data: date, name, amount, remarks
    def __init__(self, name, transaction_date, amount, remarks):
        # first step: sanitize input
        if not isinstance(name, str) or not isinstance(amount, float) or not isinstance(remarks, str):
            raise InvalidOperationError("Debug error: Transaction init; values passed not valid type")
        if not isinstance(transaction_date, date):
            raise InvalidOperationError("Debug error: Transaction init; values passed not valid type")

        if not amount > 0:
            raise InvalidOperationError("Debug error: Transaction init; amount not greater than 0")

        # set object values
        self.name = name
        self.transaction_date = transaction_date
        self.amount = amount
        self.remarks = remarks


class GUI:
    def __init__(self):
        self.bank = Bank()  # variable is used for all interaction with Bank class
        self.display_index = 0

    def create_test_data(self):
        # usage: create test data for debugging
        begin_date = date(2016, 8, 15)
        end_date = date(2016, 8, 26)
        travel_per_diem = 200.0
        daily_per_diem = 140.0

        # set bank objects financial data
        try:
            self.bank.set_per_diem_data(begin_date, end_date, travel_per_diem, daily_per_diem)
            self.bank.add_transaction("7-11", date(2016, 8, 15), 3.23, "coffee and donuts")
            self.bank.add_transaction("Marriott Sunshine", date(2016, 8, 15), 98.0, "Hotel stay")
            self.bank.add_transaction("Burgers and more", date(2016, 8, 15), 5.5, "Dinner")
            self.bank.add_transaction("Some more burgarz", date(2016, 8, 16), 11.5, "Lunch")
            self.bank.add_transaction("Forgot these burgerz", date(2016, 8, 15), 6.75, "More Lunches")
            self.bank.add_transaction("More stuff to eat", date(2016, 8, 16), 10.75, "Lunchenator")
            self.bank.add_transaction("Marriott Sunset", date(2016, 8, 16), 112.68, "Hotel stay")
            self.bank.add_transaction("Marriott little dipper", date(2016, 8, 17), 95.12, "Hotel super")
            self.bank.add_transaction("Marriott bigger lipper", date(2016, 8, 18), 97.00, "Hotel duper")

        except InvalidOperationError as e:
            print(e.message)

        # todo: create full test data

    @staticmethod
    def clear_screen():
        # usage: function clears the screen, built cross platform
        # todo: fix clear screen function
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def display_main_menu(self):
        self.clear_screen()

        print("Main Menu")
        print("------------------------")
        print("Today's date: %s" % date.today())
        print("TDY start date: %s" % self.bank.begin_date)
        print("TDY end date: %s" % self.bank.end_date)

        try:
            print("TDY duration: %s" % self.bank.calculate_tdy_duration())
        except InvalidOperationError:
            print("")

        print ("-------------------------------")
        print("Travel Per Diem amount: %s" % '${:,.2f}'.format(self.bank.travel_per_diem))
        print("Daily Per Diem amount: %s" % '${:,.2f}'.format(self.bank.daily_per_diem))
        print("Total Per Diem amount: %s" % '${:,.2f}'.format(self.bank.calculate_per_diem_total()))

        # display transactions
        print("-----------------------------------------------------------------")
        print("# Date,        Name,                             Amount,    Remarks")

        # todo: function to check display_index is valid
        # last constant in for loop controls how many records are displayed at once
        for i in range(self.display_index, self.display_index+5):
            print("%s:%s   %s    %s     %s" % (i, self.bank.transactions[i].transaction_date,
                                             '{:<30}'.format(self.bank.transactions[i].name),
                                             '${:6,.2f}'.format(self.bank.transactions[i].amount),
                                             self.bank.transactions[i].remarks))

        # todo: display total spent
        # todo: display total remaining
        # todo: display total spent vs earned for current date

        # todo: a menu

    def start_ui(self):
        # usage: begin main program loop
        # todo: load files

        # first, see if any files were loaded
        if not self.bank.is_initialized():
            self.enter_per_diem_data()

        # then, hand off program to main menu
        self.display_main_menu()

    def enter_per_diem_data(self):
        self.clear_screen()
        bad_data = True
        while (bad_data):
            bad_data = False
            print("Beginning date data")
            try:
                begin_date_year = int(input("Enter date year:"))
                begin_date_month = int(input("Enter date month:"))
                begin_date_day = int(input("Enter date day:"))
            except ValueError:
                self.clear_screen()
                print("Enter integers for date values")
                bad_data=True
                continue

            try:
                begin_date = date(begin_date_year, begin_date_month, begin_date_day)
            except ValueError:
                self.clear_screen()
                print("Enter a valid date")
                bad_data = True
                continue

            print("End date data")
            try:
                end_date_year = int(input("Enter date year:"))
                end_date_month = int(input("Enter date month:"))
                end_date_day = int(input("Enter date day:"))
            except ValueError:
                self.clear_screen()
                print("Enter integers for date values")
                bad_data = True
                continue

            try:
                end_date = date(end_date_year, end_date_month, end_date_day)
            except ValueError:
                self.clear_screen()
                print("Enter a valid date")
                bad_data = True
                continue

            try:
                travel_per_diem = float(input("Enter travel per diem amount:"))
            except ValueError:
                self.clear_screen()
                print("Enter an integer please")
                bad_data = True
                continue

            try:
                daily_per_diem = float(input("Enter daily per diem amount:"))
            except ValueError:
                self.clear_screen()
                print("Enter an integer please")
                bad_data = True
                continue

            try:
                self.bank.set_per_diem_data(begin_date, end_date, travel_per_diem, daily_per_diem)
            except InvalidOperationError as e:
                self.clear_screen()
                print(e.message)
                bad_data = True
                continue

    def main_menu_menu(self):
        choice = input("Enter [c]ange dates & Per Diem, [n]ew transaction, [#] modify transaction, [s]ave, [q]uit:")

ui = GUI()
ui.create_test_data()
ui.start_ui()
