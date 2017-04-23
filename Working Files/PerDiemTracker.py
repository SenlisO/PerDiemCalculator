import os
import pdb
from bank import Accountant, InvalidOperationError
from datetime import date, timedelta

TESTDATA = False  # default:False -- if true, test data is loaded

# todo: test page up and down
# todo: Save successful message
# todo: Changelog page
# todo: Incorporate clear data functionality

'''
Per Diem Calculator Tracker
By Richard Romick
'''




class GUI:
    def __init__(self):
        self.bill = Accountant()  # bill is our accountant.  He is the person we make all financial requests to
        self.display_index = 0
        self.max_num_transactions_display = 20
        self.load_data = True  # controlls whether the program loads from file automatically

    # this method checks a display index and corrects for out of bounds issues
    def correct_display_index(self, display_index):
        if display_index < 0:
            return 0

        # this is the case where display_index is too high
        elif display_index > (len(self.bill.transactions) - self.max_num_transactions_display - 1):
            temp = len(self.bill.transactions) - self.max_num_transactions_display - 1
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

        # set bill objects financial data
        try:
            self.bill.set_per_diem_data(begin_date, end_date, travel_per_diem, daily_per_diem)
            self.bill.add_transaction("7-11", date(2016, 8, 15), 3.23, "coffee and donuts")
            self.bill.add_transaction("Marriott Sunshine", date(2016, 8, 15), 98.0, "Hotel stay")
            self.bill.add_transaction("Burgers and more", date(2016, 8, 15), 5.5, "Dinner")
            self.bill.add_transaction("Some more burgarz", date(2016, 8, 16), 11.5, "Lunch")
            self.bill.add_transaction("Forgot these burgerz", date(2016, 8, 15), 6.75, "More Lunches")
            self.bill.add_transaction("More stuff to eat", date(2016, 8, 16), 10.75, "Lunchenator")
            self.bill.add_transaction("Marriott little dipper", date(2016, 8, 17), 95.12, "Hotel super")
            self.bill.add_transaction("Marriott bigger lipper", date(2016, 8, 18), 97.00, "Hotel duper")

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

            print("Today's date: %s" % date.today())
            print("TDY start date: %s" % self.bill.begin_date)
            print("TDY end date: %s" % self.bill.end_date)

            try:
                print("TDY duration: %s days" % self.bill.calculate_tdy_duration().days)
            except InvalidOperationError:
                print("")

            print("-------------------------------")
            print("Travel Per Diem amount: %s" % '${:,.2f}'.format(self.bill.get_value("travel per diem")))
            print("Daily Per Diem amount: %s" % '${:,.2f}'.format(self.bill.get_value("daily per diem")))
            print("Total Per Diem amount: %s" % '${:,.2f}'.format(self.bill.calculate_per_diem_total()))

            # display transactions
            print("-----------------------------------------------------------------")
            print("# Date,        Name,                             Amount,     Remarks")

            # last constant in for loop controls how many records are displayed at once
            for i in range(self.display_index, self.display_index + self.max_num_transactions_display):
                # this statement only true with databases w/ less than self.max_num_transactions_display transactions
                if i >= len(self.bill.transactions):
                    break
                print("%s:%s   %s    %s     %s" % ('{:<2}'.format(i+1), self.bill.transactions[i].transaction_date,
                                                '{:<30}'.format(self.bill.transactions[i].name),
                                                '${:6,.2f}'.format(self.bill.transactions[i].amount),
                                                self.bill.transactions[i].remarks))

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
                self.display_index = self.correct_display_index(self.display_index + self.max_num_transactions_display)

            # user chooses to page down
            elif choice == 'd':
                self.display_index = self.correct_display_index(self.display_index - self.max_num_transactions_display)

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
                print("")

        self.load_data = True  # If we didn't load data this time, set flag back to default

        # first, see if any files were loaded
        if not self.bill.is_initialized():
            self.enter_per_diem_data()

        # then, hand off program to main menu
        # if bill is still not initialized, it is because the user chose to quit during enter_per_diem_data()
        if self.bill.is_initialized():
            self.display_main_menu()
        
        
    def enter_per_diem_data(self):

        # function admin
        self.clear_screen()
        bad_data = True
        if self.bill.is_initialized(): # if bill already has previous data, user can cancel per diem entry
            print ("Enter 'c' for any answer to cancel changes")
        else: # if bill does not have previous data, user can quit program instead
            print ("Enter 'q' for any answer to quit program")

        # Beggining date: asks user for start date and converts it to date object
        while bad_data:
            bad_data = False
            try:
                temp = input("Enter beggining date ")
                if temp == "q" or temp == "c": #This is the early exit option
                    return
                begin_date = self.bill.convert_to_date(temp)
            except ValueError:
                self.clear_screen()
                print("Enter standard military date: ")
                bad_data = True

        # End date: asks user for ending date and converts it to date object
        bad_data = True
        while bad_data:
            bad_data = False
            try:
                temp = input("Enter end date: ")
                if temp == "q" or temp == "c": #This is the early exit option
                    return
                end_date = self.bill.convert_to_date(temp)
            except ValueError:
                self.clear_screen()
                print("Enter standard military date")
                bad_data = True

        # Travel per diem: asks user for per diem for travel date and checks that it is a float
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

        # Daily per diem: asks user for per diem for normal days and checks that it is a float
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
                temp = input("Enter transaction date")
                transaction_date = self.bill.convert_to_date(temp)
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
            self.bill.modify_transaction(transaction_number, transaction_name, transaction_date,
                                         transaction_amount, transaction_remarks)
        except InvalidOperationError as e:
            print(e.message)


# program starts from here
ui = GUI()

if TESTDATA:  # controlled by global variable
    ui.create_test_data()

ui.start_ui()
