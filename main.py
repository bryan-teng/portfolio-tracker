from pyportfoliotracker import Fund

#Test Code

def main():
    #Set up your fund
    date = '2020-05-18'
    fund = Fund(2375706,'^FTSE',date,strategy='dca10', risk_free_rate_percentage=0.65)

    #Buy the relevant equities
    fund.buy_equity('GSK.L',date,397,1670.20)
    fund.buy_equity('SGE.L',date,802,653)
    fund.buy_equity('NG.L',date,394,922.2)
    fund.buy_equity('WHR.L',date,3345,100.5)
    fund.buy_equity('SSE.L',date,161,1242.50)
    fund.buy_equity('RHIM.L',date,69,2306.00)
    fund.buy_equity('ICP.L',date,64,1109.00)
    fund.buy_equity('ASC.L',date,21,2768.8)

    #fund.sell_equity('GSK.L','2020-05-22',397,1670.20)

    #Call methods based on output desired
    #print(fund.all_assets_normalised.head()) #Returns a DataFrame of the historical performance of the fund
    #fund.plot_fund_performance() #Returns a graphical plot of the fund vs index
    #print(fund.fund_metrics_table()) #Returns a DataFrame of key fund metrics (alpha, beta, Sharpe's ratio)
    #fund.export_to_csv() #Exports the DataFrame of historical performance into a CSV
    #fund.export_graph() #Exports the graphical plot of the fund vs index into a PNG
    #fund.export_fund_metrics() #Exports the DataFrame of key fund metrics into a CSV



if __name__ == "__main__":
    main()