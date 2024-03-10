import os
import json
import requests
from datetime import datetime

class Search:
    def __init__(self, folder, ticker, key):
        self.folder = folder
        self.ticker = ticker
        self.key = key


        self.functions = ["OVERVIEW", "INCOME_STATEMENT", "BALANCE_SHEET", "CASH_FLOW"]
        self.filename = f"{self.functions[0].lower()}.json"

    def folder_exists(self, folder):
        if os.path.exists(folder): return True
        else: return False

    def folder_updated(self, folder):
        filepath = os.path.join(folder, self.filename)
        modification_time = os.path.getmtime(filepath)
        modification_date = datetime.fromtimestamp(modification_time)
        current_date = datetime.now()
        print(f'path: {filepath}')
        print(f'time: {modification_time}')
        print(f'date: {modification_date}')
        print(f'actual: {current_date}')
        print(f'year: {modification_date.year == current_date.year}')
        print(f'month: {modification_date.month == current_date.month}')
        print(f'day: {modification_date.day == current_date.day}')
        return modification_date.year == current_date.year and modification_date.month == current_date.month and modification_date.day == current_date.day

    def fetch_stock_data(self, ticker, api_key, function):
        base_url = "https://www.alphavantage.co/query"
        params = {
            "function": function,
            "symbol": ticker,
            "apikey": api_key
        }

        response = requests.get(base_url, params=params)
        data = response.json()
        return data
    
    def save_to_file(self, data, folder, filename):
        filepath = os.path.join(folder, filename)
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)

    def update_data(self, folder):
        for function in self.functions:
            stock_data = self.fetch_stock_data(self.ticker, self.key, function)
            filename = f"{function.lower()}.json"
            self.save_to_file(stock_data, folder, filename)

    def get_ticker(self):
        folder = f'{self.folder}/{self.ticker}'
        if self.folder_exists(folder):
            if self.folder_updated(folder): return 'updated'
            else: 
                self.update_data(folder)
                return 'download'

        else:
            os.makedirs(folder)
            self.update_data(folder)

            return 'ticker dont exists!'