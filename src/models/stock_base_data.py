from src.mongo_db_connector import MongoDBConnector


class StockBaseData:

    def __init__(self, ticker: str, mongodb_connector: MongoDBConnector):
        query = {"ticker": ticker}
        document = mongodb_connector.fetch_one("stock_base_data", query)

        self.ticker = document.get("ticker", None)
        self.pe = document.get("pe", None)

    def __str__(self):
        return f"Base data: {self.ticker}"
