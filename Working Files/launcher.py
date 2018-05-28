from UI import TextUI

load_data = True            # default:True -- if true,ledger.txt data is loaded
test_data = False             # default:False -- if true, test data is loaded
number_test_transactions = 40 # number of test transactions to create


# program starts from here
ui = TextUI(load_data)

if test_data: # Legacy testing functionality
    ui.create_test_data(number_test_transactions)

ui.start_ui()
