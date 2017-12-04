import datetime
import os
from random import randint
from decimal import *

from bank import Accountant, InvalidOperationError, UserQuitException

# todo: Save successful message
# todo: center on new/modified transaction functionality
'''
Per Diem Calculator Tracker
By Richard Romick
'''


class TextUI:
    def __init__(self, load):
        """
        GUI init method
        Params:
            load -- controls whether function loads from ledger.txt
        Returns: none
        Raises: none
        updated: 20171129
        """

        self.bill = Accountant()  # bill is our accountant.  He is the person we make all financial requests to
        self.display_index = 0
        self.max_num_transactions_display = 20
        self.load_data = load  # controls whether the program loads from file automatically
        self.last_error = ""
        getcontext().prec = 2 # function of decimal class to control decimal precision


    def page_up_down(self, is_up):
        """
        method moves display up and down
        args: is_up -- boolean value, true if page up, false if page down.
        returns: none
        raises: ValueError if is_up is not boolean
        """
        # shorten some variable names for readability
        disp_indx = self.display_index
        max_num_trans_disp = self.max_num_transactions_display
        fix_index = self.correct_display_index
        
        # test if is_up is boolean
        if not isinstance(is_up, bool):
            raise ValueError("Debug Error: UI.page_up_down arg is_up not valid type")
        # make modifications to values (local)
        if is_up: # we want to page up
            disp_indx = fix_index(disp_indx - max_num_trans_disp)
        else: # we want to page down
            disp_indx = fix_index(disp_indx + max_num_trans_disp)

        # store result in class attribute
        self.display_index = disp_indx

    def correct_display_index(self, display_index):
        """
        this method checks a display index and corrects for out of bounds issues
        args: 
            display_index: the current display index after adding or subtracting the display_index
        returns: 
            corrected display_index where display_index is within correct bounds (won't display more transaction than exists)
        raises: none
        """

        # if display_index is negative, correct it to 0 (show the first transaction first)
        if display_index < 0:
            return 0

        # this is the case where display_index is too high, show the last transactions
        elif display_index > (self.bill.num_transactions() - self.max_num_transactions_display - 1):
            temp = self.bill.num_transactions() - self.max_num_transactions_display #example: 21 - 20 = 1
            # in the case that correction causes a negative display index, return 0
            if temp < 0:
                return 0
            else:
                return temp

        # if display_index is good to go
        return display_index

    def show_latest_transaction(self):
        '''
        This method is used after a transaction is added to show the new transaction
        '''
        # todo: finish method
        pass

    def create_test_data(self, num_test_transactions):
        """
        Legacy testing method.  Replaced with testing.py
        args: 
            num_test_transactions - indicates how many test transactions to make
        returns: 
            none
        raises: 
            InvalidOperationError - debug function in case create_test_data is malfunctioning
        """

        begin_date = datetime.date(2016, 8, 15)
        end_date = datetime.date(2016, 8, 26)
        travel_per_diem = 200.0
        daily_per_diem = 140.0

        self.bill.set_per_diem_data(begin_date, end_date, travel_per_diem,
                                    daily_per_diem)
        
        # set bill objects financial data
        try:
            for i in range(1, num_test_transactions + 2):
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

    def finish_program(self):
        """
        Performs final program actions
        params: none
        returns: none
        throws: none
        """
        self.clear_screen()
        
        self.continue_program = False
        # check if Accountant has been modified since last save/load

        if self.bank_has_been_modified:
            continue_asking = True
            
            # ask the user what he wants to do

            while continue_asking: # keep looping until we have a valid answer
                print ("Data has been modified since last save")
                choice = input("Do you want to save? [y]es, [n]o, or [c]ancel: ")
                choice = str.lower(choice) # convert user input to all lowercase

                # analyze user response
                if choice == "y":
                    continue_asking = False
                    self.bill.save_data()
                elif choice == "n":
                    continue_asking = False
                elif choice == "c":
                    continue_asking = False
                    self.continue_program = True
                else:
                    continue_asking = True
                    print ("Please enter y, n or c")

    def display_main_menu(self):
        self.message = ""  # variable displays a message if not empty

        # variable continue_program and subsequent loop to continue program
        self.continue_program = True

        # create flag for when bank is modified
        self.bank_has_been_modified = False

        while self.continue_program:

            self.clear_screen()

            print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_")
            print("|                       Per Diem Tracker                        |")
            print("|                          Version 2.1                          |")
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
            choice = input("Menu: [c]hange dates & Per Diem, [n]ew transaction, [#] modify transaction, page [u]p, "
                           "page [d]own, c[l]ear data, [s]ave, [q]uit: ")

            choice = str.lower(choice) # convert user input to all lowercase

            # user chooses to quit program
            if choice == 'q':                    
                self.finish_program()

            # user chooses to change per diem data
            elif choice == 'c':
                self.enter_per_diem_data()

            # user chooses to create a new transaction
            elif choice == 'n':
                self.enter_new_transaction()

            # user chooses to page up
            elif choice == 'u':
                self.page_up_down(is_up=True)
                                
            # user chooses to page down
            elif choice == 'd':
                self.page_up_down(is_up=False)

            # user chooses to save
            elif choice == 's':
                self.bank_has_been_modified = False # resetting modified after save flag
                try:
                    self.bill.save_data()
                except InvalidOperationError as e:
                    print (e)
                    self.bank_has_been_modified = True # save unsuccessful, changing flag back


            # user chooses to clear data
            elif choice == 'l':
                self.bill = Accountant() # create new Accountant object, clearing all data
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
        """
        Singular function for entering or changing per diem amounts
        Params: none
        Returns: none
        Raises: none
        Updated: 20171129
        """
        # step 1: function admin
        self.clear_screen()

        # step 2: if there is any errors stored from elsewhere in the program, print it here
        if self.last_error != "":
            print (self.last_error)
            self.last_error = ""

        # step 3: display notice that the user can cancel input
        if self.bill.trip_parameters_set(): # case that we are modifying per diem
            print ("Enter 'c' for any answer to cancel changes")
        else: # case that this is the first time we are inputting per diem
            print ("Enter 'q' for any answer to quit program")

        # step 4-7: retrieve user input
        try:
            begin_date = self.receive_user_input("Enter TDY start date [YYYYMMDD]: ", "Enter standard military date", datetime.date)
            end_date = self.receive_user_input("Enter TDY end date [YYYYMMDD]: ", "Enter standard military date", datetime.date)
            travel_per_diem = self.receive_user_input("Enter travel per diem amount: ", "Enter a Decimal Value", Decimal)
            daily_per_diem = self.receive_user_input("Enter daily per diem amount: ", "Enter a Decimal Value", Decimal)
        except UserQuitException as e:
            print (e.message)
            return

        # step 8: call Accountant object to set per diem values
        try: # todo: bank class accepts Decimal data types
            self.bill.set_per_diem_data(begin_date, end_date, float(travel_per_diem), float(daily_per_diem))
        except InvalidOperationError as e:
            self.clear_screen()
            print(e.message)
            return

        self.bank_has_been_modified = True
        return

    def receive_user_input(self, prompt, error_prompt, data_type):
        """
        receives any type of data from user
        Params:
            prompt = prompt user sees to enter data
            error_prompt = prompt user sees if bad data entered (needed int, but user entered String)
            data_type = the type of data we want to receive
        Returns: user entered data
        Raises:
            UserQuitException if user wishes to cancel/quit
        """

        # parameter integrity checks
        valid_prompts = isinstance(prompt, str) and isinstance(error_prompt, str)
        if not valid_prompts or not isinstance(data_type, type):
            raise ValueError

        good_data = False # this value is False until we get good input from user
        data = 0 # this data type will change

        while not good_data:
            good_data = True  # assume we have good data unless we get an error
            try:
                user_input = input(prompt) # receive input from user

                if user_input == "q" or user_input == "c":  # This is the early exit option
                    raise UserQuitException("User cancel/quit detected")

                if data_type == datetime.date: # special case if requested data type is date
                    data = datetime.date(int(user_input[:4]), int(user_input[4:6]), int(user_input[6:]))
                else:
                    data = data_type(user_input)
            except (ValueError, InvalidOperation): # both cases where we got bad data (ex. string instead of date)
                self.clear_screen()
                print(error_prompt)
                good_data = False

            return data

    def enter_new_transaction(self):
        """
        Allows user to input new transaction data and add transaction to bank
        Params: none
        Returns: none
        Raises: none
        Updated: 20171201
        """

        self.clear_screen()
        bad_data = True
        transaction_amount = 0
        transaction_date = (0, 0, 0)

        # todo: finish function after receive_user_input works
        # step 1: retrieve date
        try:
            transaction_date = self.receive_user_input("Enter transaction date ", "Enter standard military date", datetime.date) # prompt for transaction date
        except UserQuitException as e:
            print (e.message)
            return

        # step 2: retrieve name
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
            return

        self.bank_has_been_modified = True
        return

    def modify_transaction_menu(self, transaction_number):
        self.clear_screen()
        bad_data = True
        transaction_amount = 0
        transaction_date = datetime.date(1950, 1, 1)

        # receive date data
        while bad_data:
            bad_data = False
            try:
                temp = input("Enter transaction date [YYYYMMDD]: ")
                transaction_date = Accountant.convert_to_date(temp)
            except ValueError:
                self.clear_screen()
                bad_data = True
                print("Enter a standard military date [YYYYMMDD]:")
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
            return

        self.bank_has_been_modified = True
        return

