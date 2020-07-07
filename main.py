from portfoliotracker.objects import Fund

#Test Code

def main():
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

    #Call methods based on output desired
    fund.plot_fund_performance()
    #fund.export_to_csv()

if __name__ == "__main__":
    main()