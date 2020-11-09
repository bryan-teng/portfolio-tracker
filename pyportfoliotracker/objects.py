from yahoofinancials import YahooFinancials
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
import numpy as np
#Random comment

class Equity:
    def __init__(self, ticker, date_of_purchase, qty, risk_free_rate):
        """
        An Equity object.
        date_of_purchase = Date when Equity is purchased.
        qty = Quantity of equity purchased.
        historical_prices = Collects the historical prices of the equity from Yahoo Finance.
        """
        self.ticker = ticker
        self.date_of_purchase = date_of_purchase
        self.qty = qty
        self.risk_free_rate = risk_free_rate

        self.historical_prices = self.get_historical_prices(date_of_purchase,datetime.now().isoformat()[:10],'daily')
        self.historical_prices_with_qty = self.get_historical_prices_with_qty()
        self.historical_paper_value = self.get_historical_paper_value()

        self.equity_returns = self.get_equity_returns()
        self.equity_returns_log = self.get_equity_returns_log()

        self.beta = None
        self.sharpe_ratio = self.get_sharpe_ratio()
        self.alpha = None

    def get_historical_prices(self,start,end,frequency):
        """
        Collects historical prices of the equity from Yahoo Finance.
        Collects all data from the date of purchase until today
        """
        equity_financials = YahooFinancials(self.ticker)
        equity_data = equity_financials.get_historical_price_data(start, end, frequency)[self.ticker]['prices']

        df = pd.DataFrame(columns=['date','high','low','open','close','adjclose'])
    
        for data in equity_data:
            df = df.append({
                'date': data['formatted_date'],
                'high': data['high'],
                'low': data['low'],
                'open': data['open'],
                'close': data['close'],
                'adjclose': data['adjclose']
                }, ignore_index = True
                )
        df = df.set_index('date')
        return df
    
    def get_historical_prices_with_qty(self):
        df = self.historical_prices.copy()
        df['qty'] = self.qty
        return df

    def get_historical_paper_value(self, new=True):
        """
        Calculates paper value based on closing prices. Returns a DataFrame with an update column 'paper_value'.
        new=True represents that the equity is purchased for the first time.
        new=False represents a buy/sell transaction that increases/decreases the quantity of the equity.
        """
        if new == True:
            df = self.historical_prices_with_qty.copy()
            df['paper_value'] = df['adjclose'] * df['qty']
            return df
        elif new == False:
            df = self.historical_paper_value.iloc[:,:6].copy()
            df['paper_value'] = df['adjclose'] * df['qty']
            return df

    def update_historical_paper_value(self):
        """
        Updates historical paper value of an equity. This is done when an existing equity is bought or sold.
        """
        self.historical_paper_value = self.get_historical_paper_value(new=False)

    def get_equity_returns(self):
        """
        Using the closing prices from the historical_prices attribute, get a DataFrame showing the log returns
        """

        df = self.historical_prices['adjclose'].copy()
        returns = (df/df.shift(1))

        return returns

    def get_equity_returns_log(self):
        """
        Return a DataFrame of the log returns
        """
        df = self.equity_returns.copy()
        log_returns = np.log(df)

        return log_returns

    def get_sharpe_ratio(self):
        std_dev = self.get_std_dev_log_returns()
        annualised_returns = self.get_average_returns_year()

        sharpe_ratio =(annualised_returns-self.risk_free_rate)/std_dev
        return sharpe_ratio

    def get_years_since_dateofpurchase(self):
        d0 = self.date_of_purchase
        d0_date = date(int(d0[:4]),int(d0[5:7]),int(d0[8:]))

        d1 = datetime.now().isoformat()[:10]
        d1_date = date(int(d1[:4]),int(d1[5:7]),int(d1[8:]))

        time_difference = d1_date - d0_date
        years = time_difference.days/365
        return years
    
    def get_total_returns_since_dateofpurchase(self):
        df = self.historical_prices['adjclose'].copy()

        returns = (df.iloc[-1]-df.iloc[0])/df.iloc[0]
        
        return returns

    def get_average_returns_year(self):
        years = self.get_years_since_dateofpurchase()
        total_returns = self.get_total_returns_since_dateofpurchase()
        annualised_returns = total_returns/years
        return annualised_returns

    def get_std_dev_log_returns(self):
        log_returns = self.equity_returns_log.copy()
        std_dev = log_returns.std()*((250*self.get_years_since_dateofpurchase())**0.5) 
        return std_dev

class Index:
    def __init__(self, ticker, cash_value, date_of_purchase, strategy='lump_sum', risk_free_rate=0.025):
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
        self.risk_free_rate = risk_free_rate
        
        self.historical_prices = self.get_historical_prices(date_of_purchase,datetime.now().isoformat()[:10],'daily')
        self.qty = self.qty_selector()
        self.historical_paper_value = self.historical_paper_value_selector()
        self.complete_table = self.create_complete_table()

        self.index_returns = self.get_index_returns()
        self.index_returns_log = self.get_index_returns_log()

        self.sharpe_ratio = self.get_sharpe_ratio()

    def get_historical_prices(self,start,end,frequency):
        """
        Collects historical prices of the index from Yahoo Finance.
        Collects all data from the date of purchase until today
        """
        equity_financials = YahooFinancials(self.ticker)
        equity_data = equity_financials.get_historical_price_data(start, end, frequency)[self.ticker]['prices']

        df = pd.DataFrame(columns=['date','high','low','open','close','adjclose'])
    
        for data in equity_data:
            df = df.append({
                'date': data['formatted_date'],
                'high': data['high'],
                'low': data['low'],
                'open': data['open'],
                'close': data['close'],
                'adjclose': data['adjclose']
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

        if self.strategy == 'dca10':
            return self.get_historical_paper_value_dca10()

    def get_historical_paper_value_lumpsum(self):
        """
        Calculates paper value based on closing prices using the lump sum strategy. Returns a DataFrame with an update column 'paper_value'
        """
        df = self.historical_prices.copy()
        df['paper_value'] = df['adjclose'] * self.qty
        return df

    def get_historical_paper_value_dca10(self):
        """
        Calculates paper value based on closing prices using the DCA 10 strategy. Returns a DataFrame with an update column 'paper_value'
        """
        df = self.historical_prices.copy()
        df['qty_owned'] = self.qty['qty_owned']
        df['cash_not_yet_invested'] = self.qty['cash_not_yet_invested']

        df['paper_value'] = df['cash_not_yet_invested'] + (df['qty_owned']*df['adjclose'])
        df.drop(columns=['qty_owned','cash_not_yet_invested'],axis=1,inplace=True)
        return df

    def qty_selector(self):
        """
        Selects the appropriate method to calculate the quantity of index owned based on the strategy specified
        """
        if self.strategy == 'lump_sum':
            return self.get_qty_lumpsum()
        if self.strategy == 'dca10':
            return self.get_qty_dca10()
    
    def get_qty_lumpsum(self):
        """
        Calculates quantity of index owned based on the lump sum strategy. Returns a float value.
        """
        return self.cash_value/(self.historical_prices.loc[self.date_of_purchase]['adjclose'])

    def get_qty_dca10(self):
        """
        Calculates quantity of index owned based on the DCA 10 strategy. Returns a DataFrame.
        """
        df = pd.DataFrame()
        df['adjclose'] = self.historical_prices['adjclose']

        num_of_rows = len(df.index)
        total_owned = 0
        qty_owned = []
        cash_not_yet_invested = []

        for i in range(10):
            qty_bought_on_day = (self.cash_value/10)/df['adjclose'].iloc[i]
            total_owned += qty_bought_on_day
            qty_owned.append(total_owned)

            cash_not_yet_invested.append(((9-i)*0.1)*self.cash_value)
        
        for j in range(num_of_rows-10):
            qty_owned.append(total_owned)
            cash_not_yet_invested.append(0)

        df['qty_owned'] = qty_owned
        df['cash_not_yet_invested'] = cash_not_yet_invested

        return df

    def create_complete_table(self):
        """
        Normalises the paper_value column into a normalised_value column, with the initial paper_value set = 100
        """
        df = self.historical_paper_value.copy()
        df['normalised_value'] = (df['paper_value']/df['paper_value'].iloc[0])*100
        return df

    def get_index_returns(self):
        """
        Using the closing prices from the historical_prices attribute, get a DataFrame showing the log returns
        """

        df = self.historical_prices['adjclose'].copy()
        returns = (df/df.shift(1))

        return returns

    def get_index_returns_log(self):
        """
        Return a DataFrame of the log returns
        """
        df = self.index_returns.copy()
        log_returns = np.log(df)

        return log_returns

    def get_sharpe_ratio(self):
        std_dev = self.get_std_dev_log_returns()
        annualised_returns = self.get_average_returns_year()

        sharpe_ratio =(annualised_returns-self.risk_free_rate)/std_dev
        return sharpe_ratio

    def get_years_since_dateofpurchase(self):
        d0 = self.date_of_purchase
        d0_date = date(int(d0[:4]),int(d0[5:7]),int(d0[8:]))

        d1 = datetime.now().isoformat()[:10]
        d1_date = date(int(d1[:4]),int(d1[5:7]),int(d1[8:]))

        time_difference = d1_date - d0_date
        years = time_difference.days/365
        return years

    def get_total_returns_since_dateofpurchase(self):
        df = self.historical_prices['adjclose'].copy()

        returns = (df.iloc[-1]-df.iloc[0])/df.iloc[0]
        
        return returns

    def get_average_returns_year(self):
        years = self.get_years_since_dateofpurchase()
        total_returns = self.get_total_returns_since_dateofpurchase()
        annualised_returns = total_returns/years
        return annualised_returns

    def get_std_dev_log_returns(self):
        log_returns = self.index_returns_log.copy()
        std_dev = log_returns.std()*((250*self.get_years_since_dateofpurchase())**0.5) 
        return std_dev

class Fund:
    def __init__(self, cash, index_ticker, date_of_creation, strategy='lump_sum', risk_free_rate_percentage=2.5):
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
        self.risk_free_rate_percentage = risk_free_rate_percentage
        self.risk_free_rate = self.risk_free_rate_percentage/100

        self.index = self.initialise_index()
        self.cash_df = self.get_cash_df()
        self.cash_deductions = []

        self.all_assets = self.compile_all_assets()
        self.all_assets_normalised = self.normalise_all_assets()

        self.fund_returns = self.get_fund_returns()
        self.fund_returns_log = self.get_fund_returns_log()

        self.beta = self.get_fund_beta()
        self.sharpe_ratio = self.get_sharpe_ratio()
        self.alpha = self.get_fund_alpha()

    def initialise_index(self):
        """
        Creates an Index object based on the ticker specified in index_ticker
        """
        return Index(self.index_ticker, self.cash, self.date_of_creation, self.strategy, self.risk_free_rate)

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
            df[equity.ticker+' qty']= equity.historical_paper_value['qty']
            df[equity.ticker].fillna(0, inplace=True)
            df[equity.ticker+' qty'].fillna(0, inplace=True)
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

    def sell_equity(self, ticker, date_of_sale, qty, price):
        """
        This method is called when an equity is sold for cash.
        Updates the attributes equities and cash_deductions accordingly.
        Then updates the all_assets and all_assets_normalised.
        """
        for equity in self.equities:
            if equity.ticker == ticker:
                equity.historical_paper_value.loc[date_of_sale:,'qty'] -= qty
                equity.update_historical_paper_value()

        self.cash_deductions.append([-(price*qty), date_of_sale])

        self.all_assets = self.compile_all_assets()
        self.all_assets_normalised = self.normalise_all_assets()

        self.fund_returns = self.get_fund_returns()
        self.fund_returns_log = self.get_fund_returns_log()
        self.beta = self.get_fund_beta()
        self.sharpe_ratio = self.get_sharpe_ratio()
        self.alpha = self.get_fund_alpha()    

    def buy_equity(self, ticker, date_of_purchase, qty, price):
        """
        This method is called when cash is used to buy an equity.
        Updates the attributes equities and cash_deductions accordingly.
        An Equity is created based on the input values, and the beta value is calculated.
        Then updates the all_assets and all_assets_normalised.
        """
        if len(self.equities) == 0:
            equity_to_add = Equity(ticker, date_of_purchase, qty, self.risk_free_rate)

            cov_with_market = self.get_cov_with_market(equity_to_add.equity_returns_log,self.index.index_returns_log)
            market_var = self.get_market_var(self.index.index_returns_log)
            beta = self.get_beta(cov_with_market,market_var)

            equity_to_add.beta = beta

            alpha = self.get_alpha(beta, equity_to_add.get_average_returns_year())

            equity_to_add.alpha = alpha

            self.equities.append(equity_to_add)


        elif len(self.equities) != 0:
            counter = 0
            for equity in self.equities:
                if equity.ticker == ticker:
                    equity.historical_paper_value.loc[date_of_purchase:,'qty'] += qty
                    equity.update_historical_paper_value()
                else:
                    counter += 1
            if counter == len(self.equities):
                equity_to_add = Equity(ticker, date_of_purchase, qty, self.risk_free_rate)

                cov_with_market = self.get_cov_with_market(equity_to_add.equity_returns_log,self.index.index_returns_log)
                market_var = self.get_market_var(self.index.index_returns_log)
                beta = self.get_beta(cov_with_market,market_var)

                equity_to_add.beta = beta

                alpha = self.get_alpha(beta, equity_to_add.get_average_returns_year())

                equity_to_add.alpha = alpha

                self.equities.append(equity_to_add)

        self.cash_deductions.append([price*qty, date_of_purchase])

        self.all_assets = self.compile_all_assets()
        self.all_assets_normalised = self.normalise_all_assets()

        self.fund_returns = self.get_fund_returns()
        self.fund_returns_log = self.get_fund_returns_log()
        self.beta = self.get_fund_beta()
        self.sharpe_ratio = self.get_sharpe_ratio()
        self.alpha = self.get_fund_alpha()

    def normalise_all_assets(self):
        """
        Normalises all assets owned, with the initial asset value (=initial cash owned by the fund) set at 100.
        """
        df = self.all_assets.copy()
        
        tickers_equity = ['cash']
        for equity in self.equities:
            tickers_equity.append(equity.ticker)

        cash_and_equities_df = df.loc[:,tickers_equity].copy()
        df['total_asset_value'] = (cash_and_equities_df.sum(axis=1))
        df['normalised_asset_value'] = ((cash_and_equities_df.sum(axis=1))/self.cash)*100

        columns_to_round = tickers_equity
        columns_to_round.append(self.index_ticker+' paper_value')
        columns_to_round.append(self.index_ticker+' normalised_value')
        columns_to_round.append('total_asset_value')

        df[columns_to_round] = df[columns_to_round].round(2)

        return df

    def get_cov_with_market(self, equity_log_returns, index_log_returns):
        df = pd.concat([equity_log_returns, index_log_returns], axis=1)
        cov=df.cov()*250
        cov_with_market=cov.iloc[0,1]

        return cov_with_market
    
    def get_market_var(self, index_log_returns):
        market_var = index_log_returns.var()*250
        return market_var

    def get_beta(self, cov_with_market, market_var):
        beta=cov_with_market/market_var
        return beta
    
    def get_alpha(self, beta, average_returns):
        expected_rate_of_return = self.risk_free_rate + (beta*(self.index.get_average_returns_year()-self.risk_free_rate))
        alpha = average_returns - expected_rate_of_return
        return alpha

    def get_fund_alpha(self):
        alpha = self.get_alpha(self.beta, self.get_average_returns_year())
        return alpha

    def get_fund_returns(self):
        """
        Using the closing prices from the historical_prices attribute, get a DataFrame showing the log returns
        """

        df = self.all_assets_normalised['normalised_asset_value'].copy()
        returns = (df/df.shift(1))

        return returns

    def get_fund_returns_log(self):
        """
        Return a DataFrame of the log returns
        """
        df = self.fund_returns.copy()
        log_returns = np.log(df)

        return log_returns

    def get_fund_beta(self):
        cov_with_market = self.get_cov_with_market(self.fund_returns_log,self.index.index_returns_log)
        market_var = self.get_market_var(self.index.index_returns_log)
        beta = self.get_beta(cov_with_market,market_var)
        return beta

    def get_sharpe_ratio(self):
        std_dev = self.get_std_dev_log_returns()
        annualised_returns = self.get_average_returns_year()
        if std_dev == 0:
            std_dev = 1000000000

        sharpe_ratio =(annualised_returns-self.risk_free_rate)/std_dev
        return sharpe_ratio

    def get_years_since_dateofpurchase(self):
        d0 = self.date_of_creation
        d0_date = date(int(d0[:4]),int(d0[5:7]),int(d0[8:]))

        d1 = datetime.now().isoformat()[:10]
        d1_date = date(int(d1[:4]),int(d1[5:7]),int(d1[8:]))

        time_difference = d1_date - d0_date
        years = time_difference.days/365
        return years
    
    def get_total_returns_since_dateofpurchase(self):
        df = self.all_assets_normalised['normalised_asset_value'].copy()

        returns = (df.iloc[-1]-df.iloc[0])/df.iloc[0]
        
        return returns

    def get_average_returns_year(self):
        years = self.get_years_since_dateofpurchase()
        total_returns = self.get_total_returns_since_dateofpurchase()
        annualised_returns = total_returns/years
        return annualised_returns

    def get_std_dev_log_returns(self):
        log_returns = self.fund_returns_log.copy()
        std_dev = log_returns.std()*((250*self.get_years_since_dateofpurchase())**0.5) 
        return std_dev

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

    def fund_metrics_table(self):
        df = pd.DataFrame(columns=['alpha','beta','sharpe_ratio','percentage_share'])
        df = df.append(pd.Series(data={
            'alpha': self.alpha,
            'beta': self.beta,
            'sharpe_ratio': self.sharpe_ratio,
            'percentage_share': '100%',
            }, name='Fund'))
        df = df.append(pd.Series(data={
            'alpha': 'N/A',
            'beta': 1,
            'sharpe_ratio': self.index.sharpe_ratio,
            'percentage_share': 'N/A',
            }, name=self.index.ticker))

        for equity in self.equities:
            df = df.append(pd.Series(data={
            'alpha': equity.alpha,
            'beta': equity.beta,
            'sharpe_ratio': equity.sharpe_ratio,
            'percentage_share': format(((self.all_assets_normalised[equity.ticker].iloc[-1])/(self.all_assets_normalised['total_asset_value'].iloc[-1]))*100, ".2f") + "%"
            }, name=equity.ticker))

        df = df.append(pd.Series(data={
            'alpha': 'N/A',
            'beta': 'N/A',
            'sharpe_ratio': 'N/A',
            'percentage_share': format(((self.all_assets_normalised['cash'].iloc[-1])/(self.all_assets_normalised['total_asset_value'].iloc[-1]))*100, ".2f") + "%"
            }, name='cash'))       

        df = df.round(3)

        return df
    
    def export_graph(self, export_name='data/fund-graph-plot.png'):
        df = pd.DataFrame()
        df2 = self.all_assets_normalised

        df[self.index_ticker] = df2[self.index_ticker + ' normalised_value']
        df['Fund'] = df2['normalised_asset_value']

        df.plot(figsize=(12,4))
        plt.savefig(export_name)
    
    def export_to_csv(self, export_name='data/historical-paper-values.csv'):
        """
        Exports the DataFrame containing the historical paper values of all the assets
        """
        df = self.all_assets_normalised
        df = df.round(2)

        df.to_csv(
            export_name, index=True, columns=list(df.columns)
        )
    
    def export_fund_metrics(self, export_name='data/fund-metrics.csv'):
        self.fund_metrics_table().to_csv(
            export_name, index=True, columns=list(self.fund_metrics_table().columns)
        )

