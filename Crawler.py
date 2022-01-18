from GetInput import GetInput

# initialize class


class Crawler:
    # Constructor
    def __init__(self, company_id, date, open_price, close_price, highest_price, lowest_price, trade_count):
        self.company_id = company_id
        self.date = date
        self.open_price = open_price
        self.close_price = close_price
        self.highest_price = highest_price
        self.lowest_price = lowest_price
        self.trade_count = trade_count


    def run(self):
        from termcolor import colored
        import os
        os.system('color')
        print(colored(">> Date format example: 2021/2/9", 'green', attrs=['bold', 'reverse']))
        print(colored(">> Stock no. example: 2330", 'magenta', attrs=['bold', 'reverse']))
        print(colored(">> Data of the date will be colored", 'blue', attrs=['bold', 'reverse']))
        end = False
        while end != 1:
            userinput = GetInput("00000000", "0000")
            # only allowed get single stock number at a time
            userinput.get_valid_date()
            date = str(userinput.date)
            userinput.get_stock_no()
            stock_no = str(userinput.stock_no)
            self.date = "00000000"
            self.open_price = 0.0
            self.close_price = 0.0
            self.highest_price = 0.0
            self.lowest_price = 10000.0
            self.trade_count = 0
            self.company_id = stock_no
            self.get_stock_data(date)

    # Final result: id_result->id / highest_price,lowest_price->compare with last few days highest_price,lowest_price
    def get_stock_data(self, date):
        # First get request data url of TWSE (Just single stock)
        # Company id
        import urllib.request as req1
        import time
        timestamp = int(time.time() * 1000)
        id_url = "https://www.twse.com.tw/zh/api/codeQuery?query=" + str(self.company_id) + "&_=" + str(timestamp)
        request1 = req1.Request(id_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
        })
        # Data
        import urllib.request as req
        # Since timestamp change
        timestamp += 1
        data_url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=" + str(date) + "&stockNo=" + str(self.company_id) + "&_=" + str(
            timestamp)
        request = req.Request(data_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
        })
        # Decode data
        # Real data stored in json format
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        with req1.urlopen(request1) as response1:
            id = response1.read().decode("utf-8")
        # Parsing data (NOT using bs4 ,since bs4 is built for html format)
        # But first check if it's VALID
        import json
        id = json.loads(id)
        data = json.loads(data)
        from termcolor import colored
        import os
        os.system('color')
        if data == {"stat": "很抱歉，沒有符合條件的資料!"}:
            print(">> " + colored(id["query"], 'yellow') + colored(" failed-> ", 'red') + colored(str(data),'red') + '\n')
        else:  # Make sure data is readable
            print(">> " + colored(id["suggestions"][0], 'yellow') + colored(" success",'cyan'))
            data_results = data["data"]
            title = data["title"]
            # Transform date to chinese date
            from datetime import datetime
            temp_converted_date = datetime.strptime(str(date), '%Y%m%d').strftime('%Y/%m/%d')
            temp_converted_date = temp_converted_date.split('/')
            temp_converted_date = str(int(temp_converted_date[0]) - 1911) + "/" + str(temp_converted_date[1]) + "/" + str(temp_converted_date[2])
            # Date correspond collect data
            date = []
            open_price = []
            high_price = []
            low_price = []
            close_price = []
            trade_count = []
            from termcolor import colored
            import os
            os.system('color')
            for singleDayResult in data_results:
                if singleDayResult[0] == temp_converted_date:
                    date.append(colored(singleDayResult[0] + "    ", 'yellow'))
                    high_price.append(colored(singleDayResult[4] + "    ", 'yellow'))
                    open_price.append(colored(singleDayResult[3] + "    ", 'yellow'))
                    low_price.append(colored(singleDayResult[5] + "    ", 'yellow'))
                    close_price.append(colored(singleDayResult[6] + "    ", 'yellow'))
                    trade_count.append(colored(singleDayResult[8] + "    ", 'yellow'))
                else:
                    date.append(colored(singleDayResult[0] + "    ", 'white'))
                    high_price.append(colored(singleDayResult[4] + "    ", 'white'))
                    open_price.append(colored(singleDayResult[3] + "    ", 'white'))
                    low_price.append(colored(singleDayResult[5] + "    ", 'white'))
                    close_price.append(colored(singleDayResult[6] + "    ", 'white'))
                    trade_count.append(colored(singleDayResult[8] + "    ", 'white'))
            import pandas as pd
            import os
            os.system('color')
            df = pd.DataFrame(
                {colored('Date' + "    ", 'white'): date, colored('Open' + "    ", 'white'): open_price, colored('High' + "    ", 'white'): high_price, colored('Low' + "    ", 'white'): low_price,
                 colored('Close' + "    ", 'white'): close_price, colored('Volume' + "    ", 'white'): trade_count})
            col = len("     Date         Open         High          Low        Close     Volume")
            line = ""
            for i in range(col):
                line = line + "="
            print(line)
            print(df.to_string(index=False))
            print(line + '\n')
