from src.mongo_db_connector import MongoDBConnector


class StockBaseData:

    def __init__(self, ticker: str, mongodb_connector: MongoDBConnector):
        query = {"ticker": ticker}
        document = mongodb_connector.fetch_one("stock_base_data", query)

        self.ticker = document.get("ticker", None)
        self.pe = document.get("pe", None)
        self.forward_pe = document.get("forward_pe", None)
        self.ps = document.get("ps", None)
        self.pb = document.get("pb", None)
        self.peg = document.get("peg", None)
        self.currency = document.get("currency", None)
        self.price = document.get("price", None)
        self.market_cap = document.get("market_cap", None)
        self.revenue_growth = document.get("revenue_growth", None)
        self.earnings_growth = document.get("earnings_growth", None)
        self.current_ratio = document.get("current_ratio", None)
        self.debt_to_equity = document.get("debt_to_equity", None)
        self.dividend_yield = document.get("dividend_yield", None)

    def __str__(self):
        return f"Base data: {self.ticker}"
