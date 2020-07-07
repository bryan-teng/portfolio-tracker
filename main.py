from src.objects import Fund

#Test Code

def main():
    date1 = '2020-05-18'

    fund1 = Fund(2375706,'^FTSE',date1,strategy='dca10')

    fund1.buy_equity('GSK.L',date1,397,1670.20)
    fund1.buy_equity('SGE.L',date1,802,653)
    fund1.buy_equity('NG.L',date1,394,922.2)
    fund1.buy_equity('WHR.L',date1,3345,100.5)
    fund1.buy_equity('SSE.L',date1,161,1242.50)
    fund1.buy_equity('RHIM.L',date1,69,2306.00)
    fund1.buy_equity('ICP.L',date1,64,1109.00)
    fund1.buy_equity('ASC.L',date1,21,2768.8)

    print(fund1.all_assets_normalised)
    fund1.plot_fund_performance()
    #fund1.export_to_csv()

if __name__ == "__main__":
    main()