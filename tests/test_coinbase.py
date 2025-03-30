from pybottrader.datastreamers.coinbase import CBHistory


def test_history():
    counter = 0
    ss = CBHistory("BTC-USD", start="2023-01-01", end="2023-12-31")
    while True:
        value = ss.next()
        if not value:
            break
        counter += 1
    assert counter > 0
