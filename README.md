# portfolio-tracker
Track an equity portfolio's performance against a major index.

## 0. Initialising

The following packages are required: `yahoofinancials`, `pandas`, `matplotlib`, `datetime`

Enter the following imports at the top of the file:
`import pyportfoliotracker`
`from pyportfoliotracker.objects import Fund`

## 1. Setting up your fund

Set up your fund using the following parameters:

`fund = Fund(cash, index_ticker, date_of_creation, strategy):`

where
- cash = cash value of the fund
- index_ticker = the ticker (based on Yahoo Finance) of the benchmark index
- date_of_creation = date of creation of the fund
- strategy (optional) = strategy used for the index benchmark. The default strategy is lump_sum.

## 2. Purchasing the relevant equities

Using the .buy_equity() method, purchase the relevant equities that are present in your fund.

`fund.buy_equity(ticker, date_of_purchase, qty, price)`

where
- ticker = the ticker (based on Yahoo Finance) of the equity
- date_of_purchase = date of purchase of the equity
- qty = quantity of equity purchased
- price = price at which equity was purchased

## 3. Selecting your desired output

There are 2 types of output that can be obtained:

**1. Graphical comparison of fund vs index performance** : obtained by calling `fund.plot_fund_performance()`

**2. CSV file containing the value of the fund vs index over time** : obtained by calling `fund.export_to_csv(output_path)`

Note that the variable `output_path` in `.export_to_csv` is set to 'data/historical-paper-values.csv' by default.