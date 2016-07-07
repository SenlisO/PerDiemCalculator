import os
from datetime import date, timedelta


class InvalidOperationError(Exception):  # exception class
    def __init__(self, message):
        self.message = message


class Bank:
    # Class contains transaction and perdiem data and performs operations on them
    def __init__(self):
        self.begin_date = date(2000, 1, 1)  # begin date of travel, new years 2000 indicates no data
        self.end_date = date(2000, 1, 1)  # end date of travel, new years 2000 indicates no data
        self.travel_per_diem = 0  # per diem for travel days
        self.daily_per_diem = 0  # per diem for normal days

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


class Transaction:
    # Class contains data for individual transactions
    # Data: date, name, amount, remarks
    def __init__(self):
        print("Placeholder")
        # todo: create initialization function


class GUI:
    def __init__(self):
        self.bank = Bank()  # variable is used for all interaction with Bank class

    def create_test_data(self):
        # usage: create test data for debugging
        begin_date = date(2016, 8, 15)
        end_date = date(2016, 8, 31)
        travel_per_diem = 140.0
        daily_per_diem = 140.0

        # set bank objects financial data
        try:
            self.bank.set_per_diem_data(begin_date, end_date, travel_per_diem, daily_per_diem)
        except InvalidOperationError as e:
            print (e.message)

        # todo: create full test data

        # output data
        self.display_main_menu()

    @staticmethod
    def clear_screen():
        # usage: function clears the screen, built cross platform
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def display_main_menu(self):
        self.clear_screen()

        print("Main Menu")
        print("Today's date: %s" % date.today())
        print("TDY start date: %s" % self.bank.begin_date)
        print("TDY end date: %s" % self.bank.end_date)
        # todo: TDY duration display
        print("Travel Per Diem amount: %s" % '${:,.2f}'.format(self.bank.travel_per_diem))
        print("Daily Per Diem amount: %s" % '${:,.2f}'.format(self.bank.daily_per_diem))
        # todo: display total per diem amount

        # todo: display all transactions
        # todo: display total spent
        # todo: display total remaining
        # todo: display total spent vs earned for current date


ui = GUI()
ui.create_test_data()
