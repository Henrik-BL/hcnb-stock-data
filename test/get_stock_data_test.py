import unittest

from hcnb_stock_data.hcnb_stock_data import HcnbStockData


class StockDataTest(unittest.TestCase):

    def test_get_data(self):
        ticker = "ADP"
        hcnb_stock_data = HcnbStockData()
        stock_data = hcnb_stock_data.get_stock_data(ticker, True)
        self.assertEqual(stock_data.ticker, ticker)  # add assertion here

if __name__ == '__main__':
    unittest.main()
