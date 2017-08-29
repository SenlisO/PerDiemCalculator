import unittest
from UI import TextUI
import datetime
from bank import InvalidOperationError
from random import randint

class UITests(unittest.TestCase):

    def test_page_up_down_correction(self):
        """
        Test ensures page up and down works and does not go out of bounds
        args: none
        returns: none
        raises: 
            InvalidOperationError - transaction data is malformed
        """

        testUI = TextUI(False)  # Create test UI, False flag prevents loading from file
        number_test_transactions = 45

        # This data must be created for test to proceed
        begin_date = datetime.date(2016, 8, 15)
        end_date = datetime.date(2016, 8, 26)
        travel_per_diem = 200.0
        daily_per_diem = 140.0

        testUI.bill.set_per_diem_data(begin_date, end_date, travel_per_diem,
                                 daily_per_diem)

        # create test transactions
        try:
            for i in range(1, number_test_transactions):
                name = "Test" + str(i)
                random_date_delta = randint(0, testUI.bill.calculate_trip_duration().days)
                date = begin_date + datetime.timedelta(0, 0, random_date_delta)
                amount = 20.0 + i
                remarks = "This is the " + str(i) + " test"
                testUI.bill.add_transaction(name, date, amount, remarks)
        except InvalidOperationError as e:
            print(e.message)

        # run tests
        # transactions index runs from 0 to 44 for a total of 45 transactions
        self.assertEqual(testUI.display_index, 0) # test display index starting point
        testUI.page_up_down(is_up=False) # display index changes from 0 to 20
        self.assertEqual(testUI.display_index, 20)
        testUI.page_up_down(is_up=False) # display index changes from 20 to 40, corrected to 24
        self.assertEqual(testUI.display_index, 24)
        testUI.page_up_down(is_up=True) # display index changes from 24 to 4
        self.assertEqual(testUI.display_index, 4)
        testUI.page_up_down(is_up=True) # display index changes from 4 to -16, corrected to 0
        self.assertEqual(testUI.display_index, 0)

unittest.main()

        
