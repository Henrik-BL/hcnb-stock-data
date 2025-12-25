from src.mongo_db_connector import MongoDBConnector


class CreateStockBaseData:

    def __init__(self, stock_info: dict, mongodb_connector: MongoDBConnector):
        self.ticker = stock_info.get("symbol", None)
        self.pe = stock_info.get("trailingPE", None)
        self.forward_pe = stock_info.get("forwardPE", None)
        self.ps = stock_info.get("priceToSalesTrailing12Months", None)
        self.pb = stock_info.get("priceToBook", None)
        self.peg = stock_info.get("trailingPegRatio", None)

        self.currency = stock_info.get("currency", None)
        self.price = stock_info.get("currentPrice", None)
        self.market_cap = stock_info.get("marketCap", None)

        self.revenue_growth = stock_info.get("revenueGrowth", None)
        self.earnings_growth = stock_info.get("earningsQuarterlyGrowth", None)

        self.current_ratio = stock_info.get("currentRatio", None)
        self.debt_to_equity = stock_info.get("debtToEquity", None)
        self.dividend_yield = stock_info.get("trailingAnnualDividendYield", None)

        # Save to db
        query = {"ticker": self.ticker}
        mongodb_connector.insert_or_replace("stock_base_data", query, self.__dict__)
