import os
import pdb
from bank import Accountant, InvalidOperationError, Trip
import datetime
from random import randint

TEST_DATA = False  # default:False -- if true, test data is loaded
NUMBER_TEST_TRANSACTIONS = 40 # number of test transactions to create

# todo: test page up and down
# todo: Save successful message
# todo: Changelog page
# todo: Incorporate clear data functionality
# todo: create testing functionatlity
# todo: test page up/down
'''
Per Diem Calculator Tracker
By Richard Romick
'''


class GUI:
    def __init__(self):
        self.bill = Accountant()  # bill is our accountant.  He is the person we make all financial requests to
        self.display_index = 0
        self.max_num_transactions_display = 20
        self.load_data = True  # controls whether the program loads from file automatically
        self.last_error = ""

    # this method checks a display index and corrects for out of bounds issues
    def correct_display_index(self, display_index):
        if display_index < 0:
            return 0

        # this is the case where display_index is too high
        elif display_index > (self.bill.num_transactions() - self.max_num_transactions_display - 1):
            temp = self.bill.num_transactions() - self.max_num_transactions_display - 1
            # case that correction causes a negative display index
            if temp < 0:
                return 0
            else:
                return temp

        # if display_index is good to go
        return display_index

    def create_test_data(self):
        # usage: create test data for debugging
        begin_date = datetime.date(2016, 8, 15)
        end_date = datetime.date(2016, 8, 26)
        travel_per_diem = 200.0
        daily_per_diem = 140.0

        self.bill.set_per_diem_data(begin_date, end_date, travel_per_diem, daily_per_diem)

        # set bill objects financial data
        try:
            # todo: make sure we are creating exactly 40 records
            for i in range(1, NUMBER_TEST_TRANSACTIONS + 2):
                name = "Test" + str(i)
                random_date_delta = randint(0, self.bill.calculate_trip_duration().days)
                date = begin_date + datetime.timedelta(0, 0, random_date_delta)
                amount = 20.0 + i
                remarks = "This is the " + str(i) + " test"
                self.bill.add_transaction(name, date, amount, remarks)
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
            print("|                      Per Diem Tracker Beta                    |")
            print("|                       By Richard Romick                       |")
            print("-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-")

            # todo: print last error message here

            print("Today's date: %s" % datetime.date.today())
            print("TDY start date: %s" % self.bill.get_trip_value("begin date"))
            print("TDY end date: %s" % self.bill.get_trip_value("end date"))

            try:
                print("TDY duration: %s days" % self.bill.calculate_trip_duration().days)
            except InvalidOperationError:
                print("")

            print("-------------------------------")
            print("Travel Per Diem amount: %s" % '${:,.2f}'.format(self.bill.get_trip_value("travel per diem")))
            print("Daily Per Diem amount: %s" % '${:,.2f}'.format(self.bill.get_trip_value("daily per diem")))
            print("Total Per Diem amount: %s" % '${:,.2f}'.format(self.bill.calculate_per_diem_total()))

            # display transactions
            print("-----------------------------------------------------------------")
            print("#  Date,        Name,                             Amount,     Remarks")

            # last constant in for loop controls how many records are displayed at once
            for i in range(self.display_index, self.display_index + self.max_num_transactions_display):
                # this statement only true with databases w/ less than self.max_num_transactions_display transactions
                if i >= self.bill.num_transactions():
                    break
                print("%s:%s   %s    %s     %s" % ('{:<2}'.format(i+1), self.bill.get_transaction_value("date", i),
                                                '{:<30}'.format(self.bill.get_transaction_value("name", i)),
                                                '${:6,.2f}'.format(self.bill.get_transaction_value("amount", i)),
                                                self.bill.get_transaction_value("remarks", i)))

            # display totals
            print("----------------------------------------------------------------")
            print("Total spent: %s" % '${:,.2f}'.format(self.bill.calculate_total_spent()))
            print("Total remaining: %s" % '${:,.2f}'.format(self.bill.calculate_per_diem_total() -
                                                self.bill.calculate_total_spent()))
            print("Total per diem gained to date: %s" % '${:,.2f}'.format(self.bill.calculate_earned_per_diem()))
            print("Difference between gained and spent: %s" % '${:,.2f}'.format(self.bill.calculate_earned_per_diem() -
                                                                    self.bill.calculate_total_spent()))


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
                self.display_index = self.correct_display_index(self.display_index - self.max_num_transactions_display)

            # user chooses to page down
            elif choice == 'd':
                self.display_index = self.correct_display_index(self.display_index + self.max_num_transactions_display)

            # user chooses to save
            elif choice == 's':
                self.bill.save_data()

            # user chooses to clear data
            elif choice == 'l':
                self.bill.clear_data()     # clear all data
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
        if self.load_data:  # flag controls whether program automatically loads data
            try:
                self.bill.load_data()
            except InvalidOperationError:  # exception is raised when file is not found
                self.last_error = "Note: Ledger file not found.  Starting fresh database"
            except IndexError: #exception is raised when file is corrupted
                self.last_error = "Error: Ledger file corrupted."

        self.load_data = True  # If we didn't load data this time, set flag back to default

        # first, see if any files were loaded
        if not self.bill.trip_parameters_set():
            self.enter_per_diem_data()

        # then, hand off program to main menu
        # if bill is still not initialized, it is because the user chose to quit during enter_per_diem_data()
        if self.bill.trip_parameters_set():
            self.display_main_menu()
        
        
    def enter_per_diem_data(self):

        # step 1: function admin
        self.clear_screen()
        bad_data = True

        # step 2: if there is any errors, print them here
        if self.last_error != "":
            print (self.last_error)
            self.last_error = ""

        # step 3: display notice that the user can cancel input
        if self.bill.trip_parameters_set(): # case that we are modifying per diem
            print ("Enter 'c' for any answer to cancel changes")
        else: # case that this is the first time we are inputting per diem
            print ("Enter 'q' for any answer to quit program")

        # step 4: asks user for start date and converts it to date object
        while bad_data:
            bad_data = False
            try:
                temp = input("Enter beggining date ")
                if temp == "q" or temp == "c": #This is the early exit option
                    return
                begin_date = Accountant.convert_to_date(temp)
            except ValueError:
                self.clear_screen()
                print("Enter standard military date: ")
                bad_data = True

        # step 5: asks user for ending date and converts it to date object
        bad_data = True
        while bad_data:
            bad_data = False
            try:
                temp = input("Enter end date: ")
                if temp == "q" or temp == "c": #This is the early exit option
                    return
                end_date = Accountant.convert_to_date(temp)
            except ValueError:
                self.clear_screen()
                print("Enter standard military date")
                bad_data = True

        # step 6: asks user for per diem for travel date and checks that it is a float
        bad_data = True
        while bad_data:
            bad_data = False
            try:
                temp = input("Enter travel per diem amount: ")
                if temp == "q" or temp == "c": #This is the early exit option
                    return
                travel_per_diem = float(temp)
            except ValueError:
                self.clear_screen()
                print("Enter an monetary value please")
                bad_data = True

        # step 7: asks user for per diem for normal days and checks that it is a float
        bad_data = True
        while bad_data:
            bad_data = False
            try:
                temp = input("Enter daily per diem amount: ")
                if temp == "q" or temp == "c": #This is the early exit option
                    return
                daily_per_diem = float(temp)
            except ValueError:
                self.clear_screen()
                print("Enter an monetary value please")
                bad_data = True

        # step 8: call Accountant object to set per diem values
        try:
            self.bill.set_per_diem_data(begin_date, end_date, travel_per_diem, daily_per_diem)
        except InvalidOperationError as e:
            self.clear_screen()
            print(e.message)
            return

    def enter_new_transaction(self):
        self.clear_screen()
        bad_data = True
        transaction_amount = 0
        transaction_date = (0, 0, 0)

        # receive date data
        while bad_data:
            bad_data = False
            try:
                temp = input("Enter transaction date: ")
                transaction_date = Accountant.convert_to_date(temp)
            except ValueError:
                self.clear_screen()
                bad_data = True
                print("Enter a standard military date")
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

        # enter transaction remarks
        transaction_remarks = input("Enter transaction remarks: ")

        try:
            self.bill.add_transaction(transaction_name, transaction_date, transaction_amount, transaction_remarks)
        except InvalidOperationError as e:
            print(e.message)

    def modify_transaction_menu(self, transaction_number):
        # todo: make modifying transaction date military date
        self.clear_screen()
        bad_data = True
        transaction_amount = 0
        transaction_date = datetime.date(1950, 1, 1)

        # receive date data
        while bad_data:
            bad_data = False
            try:
                temp = input("Enter transaction date: ")
                transaction_date = Accountant.convert_to_date(temp)
            except ValueError:
                self.clear_screen()
                bad_data = True
                print("Enter a standard military date")
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
            self.bill.modify_transaction(transaction_number, transaction_name, transaction_date,
                                         transaction_amount, transaction_remarks)
        except InvalidOperationError as e:
            print(e.message)


# program starts from here
ui = GUI()

if TEST_DATA:  # controlled by global variable
    ui.create_test_data()

ui.start_ui()
