from datetime import date, timedelta


class InvalidOperationError(Exception):  # exception class
    def __init__(self, message):
        self.message = message


class Accountant:
    # Class contains transaction and perdiem data and performs operations on them

    def get_trip_values(self, variable_name, trip_index=0):
        """
        This function is a one stop shop for necessary variable data
        Input
            name - name of the variable caller wants a value for
            possibilities include: "begin date", "end date" "daily per diem" "travel per diem"
        Return
            value of variable requested
        Throws
            value error if name is incorrect
        """

        # step 1: pull dictionary variable containing trip's values from Trip method
        pulled_values = self._tdy[trip_index].retrieve_values()

        # step 2: determine what caller is asking for and return that value
        try:
            if variable_name == "begin date":
                return pulled_values['begin_date']
            elif variable_name == "end date":
                return pulled_values['end_date']
            elif variable_name == "daily_per_diem":
                return pulled_values['daily_per_diem']
            elif variable_name == "travel_per_diem":
                return pulled_values['travel_per_diem']
            else: # step 3: handle error scenarios
                raise InvalidOperationError("Debug error: Accountant.get_trip_values: trip variable does not exist")
        except InvalidOperationError as e:
            raise e

    @staticmethod  # This means we can call the method without initializing an object
    def convert_to_date(d):
        """
        This function accepts a date and attempts to convert it to date object
        Input
            d - the date string to convert to a date object.  Must be military time
        Returns
            date object
        Throws
            value error if date can't be converted
        """

        # step 1: ensure method parameter is an integer
        try:
            begging_value = int(d)
        except ValueError as e:
            raise e

        # step 2: convert the method parameter to a string
        working_value = str(begging_value)

        # step 3: cut up string into year, month and day segments
        try:
            result = date(int(working_value[:4]), int(working_value[4:6]), int(working_value[6:]))
        except ValueError as e:  # step 4: raise value error if number can't be parsed into a date
            raise e

        # step 5: return resulting date object
        return result

    def __init__(self):
        self._tdy = []  # class Accountant built to contain multiple trips, if necessary
        self._tdy[0] = Trip()  # this will be the default trip the object will refer to if no trip is specified
        
        self._transactions = []

    def clear_data(self):
        # function erases all data from the program by assigning blank arrays
        self._tdy = []
        self._tdy[0] = Trip()

        self._transactions = []

    def load_data(self):
        # todo: continue incorporating Trip object after this point
        """
        This function loads data from the file ledger.txt 
        Input
            none
        Returns
            none
        Throws
            Invalid operation error if ledger.txt is not found
        """
        # function loads data from file ledger.txt
        try:
            file = open("ledger.txt", "r")  # opens file in read only mode
        except IOError:
            raise InvalidOperationError("Ledger.txt not found")

        file_data = []  # this is the array we will read all data into

        # now, we will read all data from the file
        for line in file:
            file_data.append(line)

        file.close()  # we no longer need the file open

        # todo: check file inputs for bad data and raise ValueError exception if necessary
        # store _begin_date from file_data
        temp = file_data[0]
        begin_date = date(int(temp[0:4]), int(temp[4:6]), int(temp[6:]))

        # store _end_date from file_data
        temp = file_data[1]
        end_date = date(int(temp[0:4]), int(temp[4:6]), int(temp[6:]))

        # store both per diem values
        travel_per_diem = float(file_data[2])
        daily_per_diem = float(file_data[3])

        # plug all read data into instance bank object
        self._tdy[0].set_per_diem(daily_per_diem, travel_per_diem)
        self._tdy[0].set_dates(begin_date, end_date)

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

        file.write(self._begin_date.strftime("%Y%m%d") + "\n")
        file.write(self._end_date.strftime("%Y%m%d") + "\n")
        file.write(str(self._travel_per_diem) + "\n")
        file.write(str(self._daily_per_diem) + "\n")

        i = 0
        while True:
            if i >= len(self._transactions):
                break

            file.write(self._transactions[i].name + "\n")
            file.write(str(self._transactions[i].transaction_date.strftime("%Y%m%d")) + "\n")
            file.write(str(self._transactions[i].amount) + "\n")
            file.write(str(self._transactions[i].remarks) + "\n")

            i += 1

        file.close()

    def set_per_diem_data(self, _begin_date, _end_date, _travel_per_diem, _daily_per_diem):
        # sanitize date values
        if not isinstance(_begin_date, date) or not isinstance(_end_date, date):
            raise InvalidOperationError("Debug error: dates provided to Bank.setperdiemdata are not correct type")
        if _end_date <= _begin_date:
            raise InvalidOperationError("Debug error: Bank.setperdiemdata: end date is <= to begin date")

        # sanitize per diem values
        if not isinstance(_travel_per_diem, float) or not isinstance(_daily_per_diem, float):
            raise InvalidOperationError("Debug error: Bank.setperdiemdata: per_diem data provided are not floats")
        if _travel_per_diem < 0 or _daily_per_diem < 0:
            raise InvalidOperationError("Debug error: Bank.setperdiemdata: per_diem data not valid")

        # set class attributes
        self._begin_date = _begin_date
        self._end_date = _end_date
        self._travel_per_diem = _travel_per_diem
        self._daily_per_diem = _daily_per_diem

    def calculate_tdy_duration(self):
        # usage: returns the difference between TDY begin and end dates
        # first, check to ensure Bank's values have been set
        if not self.is_initialized():
            raise InvalidOperationError("Debug error: Operations on Bank executed before values initialized")

        #Create timedelta object that is the difference between two dates
        result = self._end_date - self._begin_date

        #Result will be short one day, so we create a timedelta object of one day
        modification = timedelta(days=1)

        #Finally, we add modification to result
        result = result + modification

        #and return the result
        return result

    def is_initialized(self):
        # usage: determine if Bank has been given any updates to its original values
        if self._begin_date == date(1950, 1, 1):
            return False
        else:
            return True

    def calculate_per_diem_total(self):
        # usage: calculate total per diem dollar amount
        total = self._travel_per_diem * 2
        duration = self.calculate_tdy_duration().days
        total += (duration - 2) * self._daily_per_diem
        return total

    def add_transaction(self, name, transaction_date, amount, remarks):
        try:
            self._transactions.append(Transaction(name, transaction_date, amount, remarks))
        except InvalidOperationError as e:
            print(e)

        self._transactions = sorted(self._transactions, key=lambda Transaction: Transaction.transaction_date)

    def calculate_total_spent(self):
        total = 0

        for t in self._transactions:
            total = total + t.amount

        return total

    def calculate_earned_per_diem(self):
        total = 0

        # if tdy hasn't started yet, return 0
        if date.today() < self._begin_date:
            return 0

        # if the entire tdy has passed, return the total
        if date.today() >= self._end_date:
            return self.calculate_per_diem_total()

        # based on our previous checks, today must be on, or after, the first travel day
        total += self._travel_per_diem
        
        # calculate how many days have transpired (not including the first travel day)
        time_spent = date.today() - self._begin_date
        # note: because of the way dates are subtracted, it will be short 1 day. In this function, that
        # missing day is treated as the first travel day, making the calculations work.
        days = time_spent.days
        
        # multiple days by _daily_per_diem and add to total
        total += (self._daily_per_diem * days)

        return total

    def modify_transaction(self, transaction_number, name, transaction_date, amount, remarks):
        if len(self._transactions) <= transaction_number:
            raise InvalidOperationError("transaction number out of range")

        # remove transaction with indicated transaction number
        self._transactions.remove(self._transactions[transaction_number - 1])

        # use bank's own add_transaction function to add transaction
        self.add_transaction(name, transaction_date, amount, remarks)


class Transaction:
    # Class contains data for individual _transactions
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


class Trip:
    # Class contains beginning and end dates of a trip, per diem info and calculations
    def __init__(self, begin_date = Date(1950, 1, 1) , end_date = Date(1950, 1, 1), daily_per_diem = -1, travel_per_diem = -1):
        self.begin_date = begin_date
        self.end_date = end_date
        self.daily_per_diem = daily_per_diem
        self.travel_per_diem = travel_per_diem

    def set_per_diem(self, daily_per_diem, travel_per_diem):
        """
        Function used to set optional per diem values
        parameters: float daily_per_diem and travel_per_diem
        throws Value error if parameters are not floats
        returns: none
        """
        # step 1: make sure per diem values provided to function are integers or float
        if (not isinstance(daily_per_diem, float) and not isinstance(daily_per_diem, int)) or (not isinstance(travel_per_diem, float) and not isinstance(travel_per_diem, int)):
            raise ValueError('Debug error: Trip.set_per_diem; values passed not float or int')
             
        # step 2: make sure the per diem values provided to function make sense (not negative)
        if daily_per_diem < 0 or travel_per_diem < 0:
            raise ValueError('Debug error: Trip.set_per_diem; values passed must be positive')

        # step 3: store per diem values as floats
        self.daily_per_diem = float(daily_per_diem)
        self.travel_per_diem = float(ravel_per_diem)

    def set_dates(self, begin_date, end_date):
        """
        Function used to set begin and end dates
        parameters: Date objects for the beggining and end dates of trip
        throwns: ValueError if parameters are not date objects
        returns: none
        """
        # step 1: ensure that parameters provided are Date objects
        if not isinstance(begin_date, date) or not isinstance(end_date, date):
            raise ValueError('Debug error: Trip.set_dates; error: parameters provided not date objects')

        # step 2: ensure that begin_date and end_dates make sense
        if end_date <= begin_date:
            raise ValueError('Debug error: Trip.set_dates; error: trip end date should be after begin date')

        # step 3: set begin and end dates to provided values
        self.begin_date = begin_date
        self.end_date = end_date

    def retrieve_values(self):
        """
        Function used to retrieve all values from the Trip. 
        parameters: none
        returns: dictionary containing all values.  These values can be modified without affecting object's variables
        throws: none
        """
        # todo: ensure that if the optional per diem values are not set, we don't put those in the dictionary
        # step 1: make sure Trip object has been initialized (provided legit values for)
        if not self.is_initialized():
            raise InvalidOperationError('Debug error: Trip.retrieve_values; error:attempted to retrieve vales before '
                                        'object is initialized')

        # step 2: create a dictionary with date objects belonging to Trip object
        values = {'begin_date' : self.begin_date, 'end_date': self.end_date}

        # step 2: if per diem values are set, include those as well
        if self.per_diem_values_set():
             values['daily_per_diem'] = self.daily_per_diem
             values['travel_per_diem'] = self.travel_per_diem
             
        # step 3: return dictionary to caller
        return values

    def is_initialized(self):
        """
        Function used to determine whether Trip object has been provided proper values
        parameters: none
        returns: boolean indicating if object is initialized
        throws: none
        """
        # step 1: check all mandatory variables against the default values to make sure some value has been provided to it
        # the only mandatory variables are the begin_date and the end_date, as of right now
        if self.begin_date == date(1950, 1, 1) or self.end_date == date(1950, 1, 1):
            return False

        #step 2: if you make it past that first check, values are good and we return true
        return True
        
    def per_diem_values_set(self):
        """
        Function check per diem values to see if they have been set
        parameters: none
        returns: boolean indicating if per diem values have been set
        throws: none
        """
        # step 1: check per diem values against defaults
        if self.daily_per_diem == -1 or self.travel_per_diem == -1:
             return False

        # step 2: if we got past the first check, we must be good
        return True
