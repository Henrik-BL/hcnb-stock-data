from src.calculator import Calculator
from src.config.db_collections import PRICE_COLLECTION
from src.mongo_db_connector import MongoDBConnector



class StockPriceDataSummary(Calculator):
    def __init__(self, ticker: str, mongodb_connector: MongoDBConnector):
        self.ticker = ticker
        query = {"ticker": ticker}
        document = mongodb_connector.fetch_one(PRICE_COLLECTION, query)
        self.latest_price = self._get_latest_price(document)
        self.sma_225 = self._get_225_sma(document)
        self.sma_255_diff = self._get_sma_255_diff(document)
        self.rsi_14 = self._get_rsi_14(document)

        print("")

    @staticmethod
    def _get_latest_price(document: dict):
        close_prices = document.get("close_prices", [])
        if not close_prices:
            return None
        return close_prices[-1]

    @staticmethod
    def _get_225_sma(document: dict):
        close_prices = document.get("close_prices", [])

        if not close_prices:
            return None
        sma_225 = round(sum(close_prices[-225:]) / len(close_prices[-225:]), 2)
        # sma_255_diff = Calculator.calculate_change_percentage(sma_225, close_prices[-1])
        return sma_225

    def _get_sma_255_diff(self, document: dict):
        return Calculator.calculate_change_percentage(self.sma_225, self.latest_price)

    @staticmethod
    def _get_rsi_14(document: dict):
        close_prices = document.get("close_prices", [])
        if not close_prices:
            return None
        return Calculator.calculate_rsi(close_prices)


    def __str__(self):
        return f"<StockPriceDataSummary> {self.ticker}"