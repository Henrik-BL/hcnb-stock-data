import os
import unittest

from hcnb_stock_data.hcnb_stock_data import HcnbStockData


@unittest.skipUnless(os.environ.get("HCNB_INTEGRATION"), "set HCNB_INTEGRATION=1 to run against Yahoo and a local MongoDB")
class StockDataTest(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.hcnb_stock_data = HcnbStockData()

    def tearDown(self):
        """Clean up after test."""
        self.hcnb_stock_data.close()

    def test_get_data(self):
        ticker = "ADP"
        stock_data = self.hcnb_stock_data.get_stock_data(ticker, True)
        self.assertEqual(stock_data.ticker, ticker)  # add assertion here

if __name__ == '__main__':
    unittest.main()
