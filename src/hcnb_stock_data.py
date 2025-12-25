from src.models.create_stock_base_data import CreateStockBaseData
from src.models.stock_data import StockData
from src.mongo_db_connector import MongoDBConnector
from src.yahoo_stock_data import YahooStockData


class HcnbStockData:

    def __init__(self):
        self.mongo_db_connector = MongoDBConnector()

    def get_stock_data(self, ticker: str):
        self._fetch_stock_data(ticker)

        return StockData(ticker, self.mongo_db_connector)

    def _fetch_stock_data(self, ticker: str):
        yahoo_stock_data = YahooStockData(ticker)
        CreateStockBaseData(yahoo_stock_data.get_base_info(), self.mongo_db_connector)



