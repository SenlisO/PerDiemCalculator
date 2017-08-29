import unittest
from bank import *
import datetime
from random import randint

class BankTest(unittest.TestCase):

    def test_duplicate_transaction(self):
        """
        test evaluated Accountant's ability to detect attempted duplicate transactions
        params: none
        returns: none
        throws: none
        """
        # create test data
        test_accountant = Accountant()
        begin_date = datetime.date(2016, 8, 15)
        end_date = datetime.date(2016, 8, 26)
        travel_per_diem = 200.0
        daily_per_diem = 140.0
        number_test_transactions = 15
        positive_result = False  # this will be used as a flag in our tests

        test_accountant.set_per_diem_data(begin_date, end_date, travel_per_diem,
                                 daily_per_diem)

        # first transaction
        test_accountant.add_transaction("Test", datetime.date(2018, 8, 15), 20.0, "We will attempt to duplicate this test")

        # purposefully create a duplicate transaction
        try:
            test_accountant.add_transaction("Test", datetime.date(2018, 8, 15), 20.0, "We will attempt to duplicate this test")
        except InvalidOperationError as e:
            positive_result = True  # this is what we want to happen
        else:
            positive_result = False # this is not what we want to happen
            
        self.assertEqual(positive_result, True)
            
        # second transaction
        index = test_accountant.add_transaction("Test2", datetime.date(2018, 8, 16), 25.0, "This transaction will be modified")

        # purposefully modify second transaction to be a duplicate
        try:
            test_accountant.modify_transaction(index, "Test", datetime.date(2018, 8, 15), 20.0, "We will attempt to duplicate this test")
        except InvalidOperationError as e:
            positive_result = True # this is what we want to happen
        else:
            positive_result = False # this is not what we want to happen

        self.assertEqual(positive_result, True)
            
            
    def test_find_transaction(self):
        """
        test evaluates Accountant's ability to find a provided transaction
        params: none
        returns: none
        throws: none
        """

        # create test data
        test_accountant = Accountant()
        begin_date = datetime.date(2016, 8, 15)
        end_date = datetime.date(2016, 8, 26)
        travel_per_diem = 200.0
        daily_per_diem = 140.0
        number_test_transactions = 15

        test_accountant.set_per_diem_data(begin_date, end_date, travel_per_diem,
                                 daily_per_diem)

        # create test transactions
        try:
            for i in range(1, number_test_transactions): # loop for however many test transaction we want to make
                name = "Test" + str(i) #  ex: Test1
                random_date_delta = randint(0, test_accountant.calculate_trip_duration().days) # random number adding to the begin_date
                date = begin_date + datetime.timedelta(0, 0, random_date_delta) # add the random number
                amount = 20.0 + i # ex: 21, 22, 23
                remarks = "This is the " + str(i) + " test" # create some remarks
                test_accountant.add_transaction(name, date, amount, remarks) # and add it to the transaction
        except InvalidOperationError as e:
            print(e.message)

        # run the tests
        answer = test_accountant.find_transaction(test_accountant._transactions[3])
        self.assertEqual(answer, 3)
        answer = test_accountant.find_transaction(test_accountant._transactions[12])
        self.assertEqual(answer, 12)

        not_in_list_transaction = Transaction("Not in list check", datetime.date(2018, 8, 20), 250.0, "This transaction is not in the list")
        answer = test_accountant.find_transaction(not_in_list_transaction)
        self.assertEqual(answer, -1)
    
    def test_calculate_earned_per_diem(self):
        """
        test evaluates bank's and trip's calculations of earned per diem at different dates
        params: none
        returns: none
        throws: none
        """
        # create variables
        future_accountant = Accountant() # test for TDY before today's date
        current_accountant = Accountant() # test for TDY currently happening
        past_accountant = Accountant() # test for TDY after today's date
        daily_per_diem = 1.0
        travel_per_diem = 20.0

        # set up tests
        # test for a TDY after today's date
        begin_date = datetime.date.today() + datetime.timedelta(days=5) # ex: today is the 1st, begin_date is the 6th
        end_date = datetime.date.today() + datetime.timedelta(days=10) # ex: today is the 1st, end_date is the 11th
        # total is 6 days (6th to the 11th)
        future_accountant.set_per_diem_data(begin_date, end_date, travel_per_diem, daily_per_diem) #set per diem data

        # test for TDY current happening
        begin_date = datetime.date.today() - datetime.timedelta(days=3) # ex: today is the 5th, begin_date is the 2nd
        end_date = datetime.date.today() + datetime.timedelta(days=2) # ex: today is the 5th, end_date is the 7th
        # total is 6 days (2nd to the 7th)
        current_accountant.set_per_diem_data(begin_date, end_date, travel_per_diem, daily_per_diem) #set per diem data

        # test for TDY before today's date
        begin_date = datetime.date.today() - datetime.timedelta(days=10) # ex: today is the 15th, begin_date is the 5th
        end_date = datetime.date.today() - datetime.timedelta(days=5) # ex: today is the 15th, end_date is the 10th
        # total is 6 days (5th to the 10th)
        past_accountant.set_per_diem_data(begin_date, end_date, travel_per_diem, daily_per_diem) #set per diem data

        # conduct the tests
        # TDY in the future
        total = future_accountant.calculate_earned_per_diem()
        self.assertEqual(total, 0) # TDY hasn't started yet, so no per diem is earned

        # TDY currently happening
        total = current_accountant.calculate_earned_per_diem()
        # 1 travel day and 3 normal days have occurred
        # (1 * 20) + (3 * 1) = 23
        self.assertEqual(total, 23)

        # TDY in the past
        total = past_accountant.calculate_earned_per_diem()
        # 2 travel days and 4 normal days have occurred
        # (2 * 20) + (4 * 1 ) = 44
        self.assertEqual(total, 44)
        # since all per diem money has been earned
        # we can also compare total to the accountants calculate total method
        self.assertEqual(total, past_accountant.calculate_per_diem_total())


unittest.main()
