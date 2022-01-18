#initialize get user input class


class GetInput:

    def __init__(self, date, stock_no):
        self.date = date
        self.stock_no = stock_no

    # Get date input from user
    def get_valid_date(self):
        import datetime
        input_check = True
        while input_check:
            date = input(">> Enter the date: ")
            # Check if input format is correct(date)
            date = date.replace("/", "-")
            try:
                datetime.datetime.strptime(date, "%Y-%m-%d")
            except Exception:
                print(">> Error: invalid date input format\n")
                continue
            # Convert date
            date = datetime.datetime.strptime(date, "%Y-%m-%d")
            date_year = date.year
            date_month = date.month
            date_day = date.day
            # Check if date is valid
            # Future date
            if datetime.datetime(date_year, date_month, date_day) > datetime.datetime.today():
                print(">> Error: invalid future date\n")
            else:
                input_check = False
                from datetime import datetime
                self.date = str(datetime.strftime(date, '%Y%m%d'))

    # get valid stock no you want to check
    def get_stock_no(self):
        input_check = True
        while input_check == 1:
            stock_no = input(">> Enter the stock no: ")
            try:
                int(stock_no)
            except ValueError:
                print(">> Error: invalid input format\n")
                continue
            if len(stock_no) != 4:
                print(">> Error: invalid input format\n")
            elif int(stock_no)<0 or int(stock_no)>10000:
                print(">> Error: invalid input format\n")
            else:
                input_check = False
                self.stock_no = stock_no
