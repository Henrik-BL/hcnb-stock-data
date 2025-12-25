from src.models.stock_base_data import StockBaseData
from src.mongo_db_connector import MongoDBConnector


class StockData:

    def __init__(self, ticker: str, mongodb_connector: MongoDBConnector):
        self.base_data = StockBaseData(ticker, mongodb_connector)
        self.quarterly_report_data = []

    def __str__(self):
        return f"Ticker: {self.base_data.ticker}"
