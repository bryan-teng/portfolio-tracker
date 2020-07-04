from yahoofinancials import YahooFinancials
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class Index:
    def __init__(self, ticker, cash_value, date_of_purchase, strategy='lump_sum'):
        """
        An index object.
        cash_value = Cash value that is invested into the fund
        date_of_purchase = Date where cash is injected into the fund
        strategy = Strategy of investing into the index fund. Currently only supports lump_sum strategy, looking to implement DCA soon.
        historical_prices = Collects the historical prices of the index from Yahoo Finance.
        qty = Quantity of index that is owned
        historical_paper_value = An update to the historical_prices DataFrame where the paper value of the index is reflected.
        complete_table = An update to the historical_paper_value DataFrame where the values are normalised to the initial value which is set at 100.
        """
        self.ticker = ticker
        self.cash_value = cash_value
        self.date_of_purchase = date_of_purchase
        self.strategy = strategy
        
        self.historical_prices = self.get_historical_prices(date_of_purchase,datetime.now().isoformat()[:10],'daily')
        self.qty = self.qty_selector()
        self.historical_paper_value = self.historical_paper_value_selector()
        self.complete_table = self.create_complete_table()


    def get_historical_prices(self,start,end,frequency):
        """
        Collects historical prices of the index from Yahoo Finance.
        Collects all data from the date of purchase until today
        """
        equity_financials = YahooFinancials(self.ticker)
        equity_data = equity_financials.get_historical_price_data(start, end, frequency)[self.ticker]['prices']

        df = pd.DataFrame(columns=['date','high','low','open','close'])
    
        for data in equity_data:
            df = df.append({
                'date': data['formatted_date'],
                'high': data['high'],
                'low': data['low'],
                'open': data['open'],
                'close': data['close'],
                }, ignore_index = True
                )
        df = df.set_index('date')
        return df

    def historical_paper_value_selector(self):
        """
        Selects the appropriate method to calculate the paper value based on the strategy specified
        """
        if self.strategy == 'lump_sum':
            return self.lump_sum_paper_value()


    def lump_sum_paper_value(self):
        """
        Calculates paper value based on the lump sum strategy. Returns a DataFrame with an update column 'paper_value'
        """
        df = self.historical_prices
        df['paper_value'] = df['close'] * self.qty
        return df

    def qty_selector(self):
        """
        Selects the appropriate method to calculate the quantity of index owned based on the strategy specified
        """
        if self.strategy == 'lump_sum':
            return self.lump_sum_qty()
    
    def lump_sum_qty(self):
        """
        Calculates quantity of index owned based on the lump sum strategy. Returns a float value.
        """
        return self.cash_value/(self.historical_prices.loc[self.date_of_purchase]['close'])

    def create_complete_table(self):
        """
        Normalises the paper_value column into a normalised_value column, with the initial paper_value set = 100
        """
        df = self.historical_paper_value
        df['normalised_value'] = (df['paper_value']/df['paper_value'].iloc[0])*100
        return df


#Test Code
"""
index1 = Index('^NDX',1000,'2020-03-25')
print(index1.complete_table)
"""