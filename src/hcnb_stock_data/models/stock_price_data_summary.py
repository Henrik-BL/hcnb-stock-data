from hcnb_stock_data.calculator import Calculator
from hcnb_stock_data.config.db_collections import PRICE_COLLECTION
from hcnb_stock_data.mongo_db_connector import MongoDBConnector



class StockPriceDataSummary:
    def __init__(self, ticker: str, mongodb_connector: MongoDBConnector):
        self.ticker = ticker
        query = {"ticker": ticker}
        document = mongodb_connector.fetch_one(PRICE_COLLECTION, query) or {}
        self.latest_price = self._get_latest_price(document)

        self.sma_50 = self._get_50_sma(document)
        self.sma_50_diff = self._get_sma_diff(self.sma_50)

        self.sma_225 = self._get_225_sma(document)
        self.sma_255_diff = self._get_sma_diff(self.sma_225)

        self.rsi_14 = self._get_rsi_14(document)

    @staticmethod
    def _get_latest_price(document):
        close_prices = document.get("close_prices", [])
        if not close_prices:
            return None
        return close_prices[-1]

    @staticmethod
    def _get_50_sma(document ):
        close_prices = document.get("close_prices", [])
        if not close_prices:
            return None
        sma_50 = round(sum(close_prices[-50:]) / len(close_prices[-50:]), 2)
        return sma_50

    @staticmethod
    def _get_225_sma(document):
        close_prices = document.get("close_prices", [])
        if not close_prices:
            return None
        sma_225 = round(sum(close_prices[-225:]) / len(close_prices[-225:]), 2)
        return sma_225

    def _get_sma_diff(self, sma_value: float|None):
        if sma_value is None or self.latest_price is None:
            return None
        return Calculator.calculate_change_percentage(sma_value, self.latest_price)

    @staticmethod
    def _get_rsi_14(document):
        close_prices = document.get("close_prices", [])
        if not close_prices:
            return None
        return Calculator.calculate_rsi(close_prices)


    def __str__(self):
        return f"<StockPriceDataSummary> {self.ticker}"