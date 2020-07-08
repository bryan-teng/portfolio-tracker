# portfolio-tracker
Track an equity portfolio's performance against a major index.

Refer to Sample Code at the bottom for a template on how to use this package.

## 0. Initialising

The following packages are required: `yahoofinancials`, `pandas`, `matplotlib`, `datetime`

Enter the following imports at the top of the file:
```
import pyportfoliotracker
from pyportfoliotracker.objects import Fund
```

## 1. Setting up your fund

Set up your fund using the following parameters:

`fund = Fund(cash, index_ticker, date_of_creation, strategy):`

where
- cash = cash value of the fund
- index_ticker = the ticker (based on Yahoo Finance) of the benchmark index
- date_of_creation = date of creation of the fund
- strategy (optional) = strategy used for the index benchmark. The default strategy is lump_sum.

## 2. Purchasing/Selling the relevant equities

**Buying**

Using the .buy_equity() method, purchase the relevant equities that are present in your fund.

`fund.buy_equity(ticker, date_of_purchase, qty, price)`

where
- ticker = the ticker (based on Yahoo Finance) of the equity
- date_of_purchase = date of purchase of the equity
- qty = quantity of equity purchased
- price = price at which equity was purchased

**Selling**

Using the .sell_equity() method, purchase the relevant equities that are present in your fund.

`fund.sell_equity(ticker, date_of_sale, qty, price)`

where
- ticker = the ticker (based on Yahoo Finance) of the equity
- date_of_sale = date of sale of the equity
- qty = quantity of equity purchased
- price = price at which equity was purchased

## 3. Selecting your desired output

There are 2 types of output that can be obtained:

**1. Graphical comparison of fund vs index performance** : obtained by calling `fund.plot_fund_performance()`

**2. CSV file containing the value of the fund vs index over time** : obtained by calling `fund.export_to_csv(output_path)`

Note that the variable `output_path` in `.export_to_csv` is set to 'data/historical-paper-values.csv' by default.

## Sample Code:

```
#Imports
import pyportfoliotracker
from pyportfoliotracker.objects import Fund

#Set up your fund
date = '2020-05-18'
fund = Fund(2375706,'^FTSE',date,strategy='dca10')

#Buy the relevant equities
fund.buy_equity('GSK.L',date,397,1670.20)
fund.buy_equity('SGE.L',date,802,653)
fund.buy_equity('NG.L',date,394,922.2)
fund.buy_equity('WHR.L',date,3345,100.5)
fund.buy_equity('SSE.L',date,161,1242.50)
fund.buy_equity('RHIM.L',date,69,2306.00)
fund.buy_equity('ICP.L',date,64,1109.00)
fund.buy_equity('ASC.L',date,21,2768.8)

#Sell any equities
fund.sell_equity('GSK.L','2020-05-21',300,1670.20)

#Call methods based on output desired
fund.plot_fund_performance()
fund.export_to_csv()

#To view data in Python command line rather than in a csv:
print(fund.all_assets_normalised)
```