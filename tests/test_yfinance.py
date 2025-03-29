from pybottrader.datastreamers.yfinance import YFHistory

ss = YFHistory("NFLX", start="2024-01-01", end="2024-12-31")
while True:
    data = ss.next()
    if not data:
        break
    print(data)
    
