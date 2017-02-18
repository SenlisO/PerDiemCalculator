import os
import pdb
from datetime import date, timedelta

TESTDATA = False  # default:False -- if true, test data is loaded

# todo: test page up and down
# todo: test calculations
# todo: Save successful message
# todo: Changelog page
'''
Per Diem Calculator Beta
By Richard Romick

Version history
V1.0 (TBD) -- All basic functions working.  All code properly commented and
    data is tested in all functions for integrity

Future features
Multi-platform -- runs as standalone executable/script
Future plans page -- make this data available from within program
Clean code -- optimize code to run faster and cleaner.  Fix all notifications on editors bar
Comment code -- comment all code for readability
Harden code -- implement input and parameter sanitation for all functions
Multiple trips -- user can switch between different trips in realtime.  Multiple trips per file.  Can delete trips from file
Loading functionality -- user chooses when to load at beginning of program and can load while running
Intro message -- displays program name, author and version number
Streamline console -- More creative ways to display data and receive inputs
Non-calculated transactions -- transactions that add to total, but not to remaining per diem
    Useful in calculating how much was spent overall
Complex Per Diem amounts -- add optional flight and lodging per diem amounts
Partial payments -- add tracker for partial DTS disbursements and total remaining uncompensated amount
Multiple files -- Able to interact with multiple ledgers, saving and loading to them at will
Complex settings -- able to change display and functional behavior and carry over between running
Automatic backup -- When saving to a file, automatically keeps a number of copies defined in settings file
GUI -- change terminal behavior into buttons, labels, menus, etc
Mobile functionality -- migrate desktop GUI into Android and iOS and maintain in concert with desktop
Dropbox integration -- able to sync between devices by storing files in dropbox

'''


class InvalidOperationError(Exception):  # exception class
    def __init__(self, message):
        self.message = message


class Bank:
    # Class contains transaction and perdiem data and performs operations on them
    def __init__(self):
        self.begin_date = date(1950, 1, 1)  # begin date of travel, new years 1950 indicates no data
        self.end_date = date(1950, 1, 1)  # end date of travel, new years 1950 indicates no data
        self.travel_per_diem = 0  # per diem for travel days
        self.daily_per_diem = 0  # per diem for normal days
        self.transactions = []


    def clear_data(self):
        #function erases all data from the program
        self.begin_date = date(1950, 1, 1)
        self.end_date = date(1950, 1, 1)
        self.travel_per_diem = 0
        self.daily_per_diem = 0
        self.transactions = []

           
    def load_data(self):
        # function loads data from file ledger.txt
        try:
            file = open("ledger.txt", "r")  # opens file in read only mode
        except OSError:
            raise InvalidOperationError("Ledger.txt not found")

        file_data = []  # this is the array we will read all data into

        # now, we will read all data from the file
        for line in file:
            file_data.append(line)

        file.close()  # we no longer need the file open

        # store begin_date from file_data
        temp = file_data[0]
        begin_date = date(int(temp[0:4]), int(temp[4:6]), int(temp[6:]))

        # store end_date from file_data
        temp = file_data[1]
        end_date = date(int(temp[0:4]), int(temp[4:6]), int(temp[6:]))

        # store both per diem values
        travel_per_diem = float(file_data[2])
        daily_per_diem = float(file_data[3])

        # plug all read data into instance bank object
        self.set_per_diem_data(begin_date, end_date, travel_per_diem, daily_per_diem)

        i = 4  # index number,starts after previous reads are done
        while i + 4 <= len(file_data):  # continue until file_data is out of records
            # store next transaction's name and increment index
            name = file_data[i]
            name = name[:-1]  # this cuts off the newline character
            i += 1

            # store transaction date and increment index
            temp = file_data[i]
            transaction_date = date(int(temp[0:4]), int(temp[4:6]), int(temp[6:]))
            i += 1

            # store transaction amount and increment index
            amount = float(file_data[i])
            i += 1

            # store transaction remarks and increment index
            remarks = file_data[i]
            remarks = remarks[:-1]  # this cuts off the newline character
            i += 1

            # add full transaction to the bank's transaction stack
            self.add_transaction(name, transaction_date, amount, remarks)

    def save_data(self):
        # function saves data to file ledger.txt
        file = open("ledger.txt", "w")

        file.write(self.begin_date.strftime("%Y%m%d") + "\n")
        file.write(self.end_date.strftime("%Y%m%d") + "\n")
        file.write(str(self.travel_per_diem) + "\n")
        file.write(str(self.daily_per_diem) + "\n")

        i = 0
        while True:
            if i >= len(self.transactions):
                break

            file.write(self.transactions[i].name + "\n")
            file.write(str(self.transactions[i].transaction_date.strftime("%Y%m%d")) + "\n")
            file.write(str(self.transactions[i].amount) + "\n")
            file.write(str(self.transactions[i].remarks) + "\n")

            i += 1

        file.close()

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

        # then, make calculation and return result (added 1 to make the dates inclusive on both ends [20161228])
        return self.end_date.day - self.begin_date.day + 1

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
        total += (duration - 2) * self.daily_per_diem
        return total

    def add_transaction(self, name, transaction_date, amount, remarks):
        try:
            self.transactions.append(Transaction(name, transaction_date, amount, remarks))
        except InvalidOperationError as e:
            print(e)

        self.transactions = sorted(self.transactions, key=lambda Transaction: Transaction.transaction_date)

    def calculate_total_spent(self):
        total = 0

        for t in self.transactions:
            total = total + t.amount

        return total

    def calculate_earned_per_diem(self):
        total = 0

        # if tdy hasn't started yet, return 0
        if date.today() < self.begin_date:
            return 0

        # calculate how many days have transpired
        time_spent = date.today() - self.begin_date
        days = time_spent.days  # days will be modified, time_spent will not be

        # if the entire tdy has passed, return the total
        if date.today() >= self.end_date:
            return self.calculate_per_diem_total()

        # if there is more than one day, add travel per diem
        if days > 1:
            total += self.travel_per_diem
            days -= 1

        total += (self.daily_per_diem * days)

        return total

    def modify_transaction(self, transaction_number, name, transaction_date, amount, remarks):
        if len(self.transactions) <= transaction_number:
            raise InvalidOperationError("transaction number out of range")

        # remove transaction with indicated transaction number
        self.transactions.remove(self.transactions[transaction_number - 1])

        # use bank's own add_transaction function to add transaction
        self.add_transaction(name, transaction_date, amount, remarks)


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
        self.max_num_transactions_display = 20
        self.load_data = True  # controlls whether the program loads from file automatically

    # this method checks a display index and corrects for out of bounds issues
    def correct_display_index(self, display_index):
        if display_index < 0:
            return 0

        # this is the case where display_index is too high
        elif display_index > (len(self.bank.transactions) - self.max_num_transactions_display - 1):
            temp = len(self.bank.transactions) - self.max_num_transactions_display - 1
            # case that correction causes a negative display index
            if temp < 0:
                return 0
            else:
                return temp

        # if display_index is good to go
        return display_index

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
            self.bank.add_transaction("Marriott little dipper", date(2016, 8, 17), 95.12, "Hotel super")
            self.bank.add_transaction("Marriott bigger lipper", date(2016, 8, 18), 97.00, "Hotel duper")

        except InvalidOperationError as e:
            print(e.message)

    @staticmethod
    def clear_screen():
        # usage: function clears the screen, built cross platform
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def display_main_menu(self):
        self.message = ""  # variable displays a message if not empty

        # variable continue_program and subsequent loop to continue program
        continue_program = True

        while continue_program:

            self.clear_screen()

            print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")
            print("|                    Per Diem Calculator Beta                   |")
            print("|                       By Richard Romick                       |")
            print("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")

            print("Today's date: %s" % date.today())
            print("TDY start date: %s" % self.bank.begin_date)
            print("TDY end date: %s" % self.bank.end_date)

            try:
                print("TDY duration: %s days" % self.bank.calculate_tdy_duration())
            except InvalidOperationError:
                print("")

            print("-------------------------------")
            print("Travel Per Diem amount: %s" % '${:,.2f}'.format(self.bank.travel_per_diem))
            print("Daily Per Diem amount: %s" % '${:,.2f}'.format(self.bank.daily_per_diem))
            print("Total Per Diem amount: %s" % '${:,.2f}'.format(self.bank.calculate_per_diem_total()))

            # display transactions
            print("-----------------------------------------------------------------")
            print("# Date,        Name,                             Amount,     Remarks")

            # last constant in for loop controls how many records are displayed at once
            for i in range(self.display_index, self.display_index + self.max_num_transactions_display):
                # this statement only true with databases w/ less than self.max_num_transactions_display transactions
                if i >= len(self.bank.transactions):
                    break
                print("%s:%s   %s    %s     %s" % ('{:<2}'.format(i+1), self.bank.transactions[i].transaction_date,
                                                '{:<30}'.format(self.bank.transactions[i].name),
                                                '${:6,.2f}'.format(self.bank.transactions[i].amount),
                                                self.bank.transactions[i].remarks))

            # display totals
            print("----------------------------------------------------------------")
            print("Total spent: %s" % '${:,.2f}'.format(self.bank.calculate_total_spent()))
            print("Total remaining: %s" % '${:,.2f}'.format(self.bank.calculate_per_diem_total() -
                                                self.bank.calculate_total_spent()))
            print("Total per diem earned: %s" % '${:,.2f}'.format(self.bank.calculate_earned_per_diem()))
            print("Total earned remaining: %s" % '${:,.2f}'.format(self.bank.calculate_earned_per_diem() -
                                                                    self.bank.calculate_total_spent()))


            # display message if one is stored
            if not self.message == "":
                print ("\n" + self.message)
                self.message = ""
            else:
                print ("")

            # time for user input
            choice = input("Menu: [c]ange dates & Per Diem, [n]ew transaction, [#] modify transaction, page [u]p, "
                           "page [d]own, c[l]ear data, [s]ave, [q]uit: ")

            # user chooses to quit program
            if choice == 'q':
                continue_program = False

            # user chooses to change per diem data
            elif choice == 'c':
                self.enter_per_diem_data()

            # user chooses to create a new transaction
            elif choice == 'n':
                self.enter_new_transaction()

            # user chooses to page up
            elif choice == 'u':
                self.display_index = self.correct_display_index(self.display_index + self.max_num_transactions_display)

            # user chooses to page down
            elif choice == 'd':
                self.display_index = self.correct_display_index(self.display_index - self.max_num_transactions_display)

            # user chooses to save
            elif choice == 's':
                self.bank.save_data()

            # user chooses to clear data
            elif choice == 'l':
                self.bank.clear_data()     # clear all data
                self.load_data = False     # prevents the program from loading data
                self.enter_per_diem_data() # restart process for entering initial per diem data

            else:
                # user chooses to modify transaction
                try:
                    transaction_number = int(choice)
                    self.modify_transaction_menu(transaction_number)
                except ValueError as e:
                    # the last possibility is that the user entered an invalid choice
                    self.message = "Error: Invalid menu option"

    def start_ui(self):
        # usage: begin main program loop
        pdb.set_trace()
        if self.load_data:  # flag controls whether program automatically loads data
            try:
                self.bank.load_data()
            except InvalidOperationError:  # exception is raised when file is not found
                print("")

        self.load_data = True  # If we didn't load data this time, set flag back to default

        # first, see if any files were loaded
        if not self.bank.is_initialized():
            self.enter_per_diem_data()

        # then, hand off program to main menu
        self.display_main_menu()

    def enter_per_diem_data(self):
        # todo: fix function so an error doesn't start entire loop again

        self.clear_screen()
        bad_data = True
        while bad_data:
            bad_data = False
            print("Beginning date data")
            try:
                begin_date_year = int(input("Enter date year:"))
                begin_date_month = int(input("Enter date month:"))
                begin_date_day = int(input("Enter date day:"))
            except ValueError:
                self.clear_screen()
                print("Enter integers for date values")
                bad_data = True
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

    def enter_new_transaction(self):
        self.clear_screen()
        bad_data = True
        transaction_amount = 0
        transaction_date = (0, 0, 0)

        # receive date data
        while bad_data:
            bad_data = False
            try:
                transaction_date_year = int(input("Enter transaction date year: "))
                transaction_date_month = int(input("Enter transaction date month: "))
                transaction_date_day = int(input("Enter transaction date day:"))
            except ValueError:
                self.clear_screen()
                bad_data = True
                print("Enter integers for date values")
                continue

            try:
                transaction_date = date(transaction_date_year, transaction_date_month, transaction_date_day)
            except ValueError:
                self.clear_screen()
                bad_data = True
                print("Enter a valid date")

        # receive transaction name
        transaction_name = input("Enter transaction name: ")

        # receive transaction amount
        bad_data = True
        while bad_data:
            bad_data = False
            try:
                transaction_amount = float(input("Enter transaction amount: "))
            except ValueError:
                self.clear_screen()
                bad_data = True
                print("Enter a valid dollar amount")

        # enter transaction remarks
        transaction_remarks = input("Enter transaction remarks: ")

        try:
            self.bank.add_transaction(transaction_name, transaction_date, transaction_amount, transaction_remarks)
        except InvalidOperationError as e:
            print(e.message)

    def modify_transaction_menu(self, transaction_number):
        self.clear_screen()
        bad_data = True
        transaction_amount = 0
        transaction_date = date(1950, 1, 1)

        # receive date data
        while bad_data:
            bad_data = False
            try:
                transaction_date_year = int(input("Enter transaction date year: "))
                transaction_date_month = int(input("Enter transaction date month: "))
                transaction_date_day = int(input("Enter transaction date day:"))
            except ValueError:
                self.clear_screen()
                bad_data = True
                print("Enter integers for date values")
                continue

            try:
                transaction_date = date(transaction_date_year, transaction_date_month, transaction_date_day)
            except ValueError:
                self.clear_screen()
                bad_data = True
                print("Enter a valid date")
                continue

        # receive transaction name
        transaction_name = input("Enter transaction name: ")

        # receive transaction amount
        bad_data = True
        while bad_data:
            bad_data = False
            try:
                transaction_amount = float(input("Enter transaction amount: "))
            except ValueError:
                self.clear_screen()
                bad_data = True
                print("Enter a valid dollar amount")
                continue

        # enter transaction remarks
        transaction_remarks = input("Enter transaction remarks: ")

        try:
            self.bank.modify_transaction(transaction_number, transaction_name, transaction_date,
                                         transaction_amount, transaction_remarks)
        except InvalidOperationError as e:
            print(e.message)


# program starts from here
ui = GUI()

if TESTDATA:  # controlled by global variable
    ui.create_test_data()

ui.start_ui()
