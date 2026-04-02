from hcnb_stock_data.mongo_db_connector import MongoDBConnector


class StockBaseData:

    def __init__(self, ticker: str, mongodb_connector: MongoDBConnector):
        query = {"ticker": ticker}
        document = mongodb_connector.fetch_one("stock_base_data", query)

        self.ticker = document.get("ticker", None)
        self.name = document.get("name", None)
        self.pe = document.get("pe", None)
        self.forward_pe = document.get("forward_pe", None)
        self.ps = document.get("ps", None)
        self.pb = document.get("pb", None)
        self.peg = document.get("peg", None)
        self.gross_margins = document.get("gross_margins", None)
        self.currency = document.get("currency", None)
        self.price = document.get("price", None)
        self.market_cap = document.get("market_cap", None)
        self.revenue_growth = document.get("revenue_growth", None)
        self.earnings_growth = document.get("earnings_growth", None)
        self.current_ratio = document.get("current_ratio", None)
        self.debt_to_equity = document.get("debt_to_equity", None)
        self.dividend_yield = document.get("dividend_yield", None)
        self.sector = document.get("sector", None)
        self.industry = document.get("industry", None)
        self.full_time_employees = document.get("full_time_employees", None)

        self.beta = document.get("beta", None)
        self.all_time_high = document.get("all_time_high", None)
        self.fifty_two_week_high = document.get("fifty_two_week_high", None)
        self.fifty_two_week_low = document.get("fifty_two_week_low", None)

        self.short_percent_of_float = document.get("short_percent_of_float", None)
        self.short_ratio = document.get("short_ratio", None)
        self.held_percent_institutions = document.get("held_percent_institutions", None)
        self.held_percent_insiders = document.get("held_percent_insiders", None)

        # Keep legacy alias used by StockData while also exposing full name.
        self.recommendation_mean = document.get("recommendation_mean", None)
        self.target_high_price = document.get("target_high_price", None)
        self.target_low_price = document.get("target_low_price", None)
        self.target_mean_price = document.get("target_mean_price", None)
        self.target_median_price = document.get("target_median_price", None)

    def __str__(self):
        return f"Base data: {self.ticker}"
