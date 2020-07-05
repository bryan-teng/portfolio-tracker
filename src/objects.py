from yahoofinancials import YahooFinancials
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class Equity:
    def __init__(self, ticker, date_of_purchase, qty):
        """
        An Equity object.
        date_of_purchase = Date when Equity is purchased.
        qty = Quantity of equity purchased.
        historical_prices = Collects the historical prices of the equity from Yahoo Finance.
        """
        self.ticker = ticker
        self.date_of_purchase = date_of_purchase
        self.qty = qty

        self.historical_prices = self.get_historical_prices(date_of_purchase,datetime.now().isoformat()[:10],'daily')
        self.historical_paper_value = self.get_historical_paper_value()

    def get_historical_prices(self,start,end,frequency):
        """
        Collects historical prices of the equity from Yahoo Finance.
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

    def get_historical_paper_value(self):
        """
        Calculates paper value based on closing prices. Returns a DataFrame with an update column 'paper_value'
        """
        df = self.historical_prices
        df['paper_value'] = df['close'] * self.qty
        return df

class Index:
    def __init__(self, ticker, cash_value, date_of_purchase, strategy='lump_sum'):
        """
        An Index object.
        cash_value = Cash value that is invested into the fund
        date_of_purchase = Date when cash is injected into the fund
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
            return self.get_historical_paper_value_lumpsum()


    def get_historical_paper_value_lumpsum(self):
        """
        Calculates paper value based on closing prices using the lump sum strategy. Returns a DataFrame with an update column 'paper_value'
        """
        df = self.historical_prices
        df['paper_value'] = df['close'] * self.qty
        return df

    def qty_selector(self):
        """
        Selects the appropriate method to calculate the quantity of index owned based on the strategy specified
        """
        if self.strategy == 'lump_sum':
            return self.get_qty_lumpsum()
    
    def get_qty_lumpsum(self):
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

class Fund:
    def __init__(self, cash, index_ticker, date_of_creation, strategy='lump_sum'):
        """
        A Fund object.
        cash = Total amount of cash injected into the fund.
        index_ticker = The ticker of the index used as the fund's benchmark.
        date_of_creation = Date when the fund is created.
        equities = Equities owned by the fund. Add on equities using the .buy_equity method.
        strategy = The strategy used for the equivalent index comparison.

        index = Contains an Index object that is created based on the index_ticker attribute.
        cash_df = A DataFrame that contains Index performance and the amount of cash owned by the fund.
        cash_deductions = 
        Contains lists [a,b] which are individually appended after each .buy_equity() method.
        Accounts for the decreaese in cash, where a = amount of cash decrease, b = date of decreasse.

        all_assets = A DataFrame that adds on the total asset value owned by the fund in addition to the cash_df.
        all_assets_normalised = A DataFrame that adds on the normalised total asset value.
        """
        self.cash = cash
        self.index_ticker = index_ticker
        self.date_of_creation = date_of_creation
        self.equities = []
        self.strategy = strategy

        self.index = self.initialise_index()
        self.cash_df = self.get_cash_df()
        self.cash_deductions = []

        self.all_assets = self.compile_all_assets()
        self.all_assets_normalised = self.normalise_all_assets()

    def initialise_index(self):
        """
        Creates an Index object based on the ticker specified in index_ticker
        """
        return Index(self.index_ticker, self.cash, self.date_of_creation, self.strategy)

    def compile_all_assets(self):
        """
        Creates a DataFrame that contains the Index's paper_value, its normalised_value, and the cash owned by the fund.
        Then calls the check_cash_deduction methods to adjust the cash values accordingly.
        Then adds in the paper value of the equities owned by the fund.
        """
        df = pd.DataFrame()
        df[self.index.ticker+' paper_value'] = self.index.complete_table['paper_value']
        df[self.index.ticker+' normalised_value'] = self.index.complete_table['normalised_value']
        df['cash'] = self.cash_df

        df = self.check_cash_deductions(df)

        for equity in self.equities:
            df[equity.ticker] = equity.historical_paper_value['paper_value']
            df[equity.ticker].fillna(0, inplace=True)
        return df
    
    def get_cash_df(self):
        """
        Generates a DataFrame where each element is equivalent to the fund's cash.
        The index.complete_table method is called just to generate rows which are equal to the number of dates.
        """
        df = pd.DataFrame()
        df[self.index.ticker] = self.index.complete_table['paper_value']
        df['cash'] = self.cash
        df.drop(columns=[self.index.ticker],axis=1,inplace=True)
        return df

    def check_cash_deductions(self, df):
        """
        Adjusts cash values in the appropriate rows (at specific dates) based on the deductions present.
        """
        for deduction in self.cash_deductions:
            df.loc[deduction[1]:,'cash'] -= deduction[0]
        return df

    def buy_equity(self, ticker, date_of_purchase, qty, price):
        """
        This method is called when cash is used to buy an equity.
        Updates the attributes equities and cash_deductions accordingly.
        Then updates the all_assets and all_assets_normalised.
        """
        self.equities.append(Equity(ticker, date_of_purchase, qty))
        self.cash_deductions.append([price*qty, date_of_purchase])

        self.all_assets = self.compile_all_assets()
        self.all_assets_normalised = self.normalise_all_assets()

    def normalise_all_assets(self):
        """
        Normalises all assets owned, with the initial asset value (=initial cash owned by the fund) set at 100.
        """
        df = self.all_assets
        cash_and_equities_df = df.iloc[:,2:]
        df['normalised_asset_value'] = ((cash_and_equities_df.sum(axis=1))/self.cash)*100
        return df
    
    def plot_fund_performance(self):
        """
        Plots the fund's performance against the index.
        """
        df = pd.DataFrame()
        df2 = self.all_assets_normalised

        df[self.index_ticker] = df2[self.index_ticker + ' normalised_value']
        df['Fund'] = df2['normalised_asset_value']

        df.plot(figsize=(12,4))
        plt.show()

#Test Code

equity1 = Equity('EBAY','2020-06-24',1000)
equity2 = Equity('ADSK','2020-06-23',500)

fund1= Fund(200000,'^NDX','2020-06-19')

#print(fund1.all_assets.head())

fund1.buy_equity('EBAY','2020-06-24',1000,equity1.historical_prices.loc['2020-06-24','close'])
fund1.buy_equity('ADSK','2020-06-23',500,equity2.historical_prices.loc['2020-06-23','close'])

#print(fund1.all_assets.head())
print(fund1.all_assets_normalised)
fund1.plot_fund_performance()