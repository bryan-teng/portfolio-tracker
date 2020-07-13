# portfolio-tracker
Track an equity portfolio's performance against a major index.

Refer to Sample Code at the bottom for a template on how to use this package.

## 0. Initialising

The following packages are required: `yahoofinancials`, `pandas`, `matplotlib`, `datetime`, `numpy`

Enter the following imports at the top of the file:
```
import pyportfoliotracker
from pyportfoliotracker import Fund
```

## 1. Setting up your fund

Set up your fund using the following parameters:

`fund = Fund(cash, index_ticker, date_of_creation, strategy, risk_free_rate_percentage):`

where
- cash = cash value of the fund
- index_ticker = the ticker (based on Yahoo Finance) of the benchmark index
- date_of_creation = date of creation of the fund
- strategy (optional) = strategy used for the index benchmark. The default strategy is lump_sum. The other option is dca10, which represents Dollar Cost Averaging using 10% of cash value per day.
- risk_free_rate_percentage (optional) = the risk free rates, in percentage (e.g. enter 2.5 for 2.5%), that will be used to calculate alpha, beta and Sharpe ratio. The default is set to 2.5%.

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

There are many types of output that can be useful to you:

**1a. DataFrame of the fund's historical paper value vs Index** : obtained by calling `print(fund.all_assets_normalised)`

Note that simply calling the attribute `fund.all_assets_normalised` returns you the DataFrame that can be integrated into other packages and use cases.

**1b. Exporting the DataFrame mentioned in 1a into a CSV** : obtained by calling `fund.export_to_csv(output_path)`

<img src="/src/csv_output.png" alt="CSV Output of Fund Performance"/>

Note that the variable `output_path` in `.export_to_csv` is set to 'data/historical-paper-values.csv' by default.

**2a. Graphical comparison of fund vs index performance** : obtained by calling `fund.plot_fund_performance()`

<img src="/src/graphical_output.png" alt="Graphical Output of Fund Performance"/>

**2b. Exporting the Graph mentioned in 2a into a PNG** : obtained by calling `fund.export_graph(output_path)`

Note that the variable `output_path` in `.export_graph` is set to 'data/fund-graph-plot.png' by default.

**3a. DataFrame of the fund's key financial metrics e.g. alpha, beta, Sharpe's Ratio** : obtained by calling `print(fund.fund_metrics_table())`

<img src="/src/fund-metrics.png" alt="Fund Metrics Table">

Note that simply calling the attribute `fund.fund_metrics_table` returns you the DataFrame that can be integrated into other packages and use cases.

**3b. Exporting the DataFrame mentioned in 3a into a CSV** : obtained by calling `fund.export_fund_metrics(output_path)`

Note that the variable `output_path` in `.export_graph` is set to 'data/fund-metrics.csv' by default.

## Sample Code:

```
"""
Imports
"""
import pyportfoliotracker
from pyportfoliotracker import Fund

"""
Set up your fund
"""
date = '2020-05-18'
fund = Fund(2375706,'^FTSE',date,strategy='dca10', risk_free_rate_percentage=0.65)

"""
Buy the relevant equities
"""
fund.buy_equity('GSK.L',date,397,1670.20)
fund.buy_equity('SGE.L',date,802,653)
fund.buy_equity('NG.L',date,394,922.2)
fund.buy_equity('WHR.L',date,3345,100.5)
fund.buy_equity('SSE.L',date,161,1242.50)
fund.buy_equity('RHIM.L',date,69,2306.00)
fund.buy_equity('ICP.L',date,64,1109.00)
fund.buy_equity('ASC.L',date,21,2768.8)

"""
Sell the relevant equities
"""
fund.sell_equity('GSK.L','2020-05-22',397,1670.20)

"""
Call methods based on output desired
"""
print(fund.all_assets_normalised.head()) #Returns a DataFrame of the historical performance of the fund
fund.plot_fund_performance() #Returns a graphical plot of the fund vs index
print(fund.fund_metrics_table()) #Returns a DataFrame of key fund metrics (alpha, beta, Sharpe's ratio)
fund.export_to_csv() #Exports the DataFrame of historical performance into a CSV
fund.export_graph() #Exports the graphical plot of the fund vs index into a PNG
fund.export_fund_metrics() #Exports the DataFrame of key fund metrics into a CSV
```