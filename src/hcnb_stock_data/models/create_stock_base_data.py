from hcnb_stock_data.mongo_db_connector import MongoDBConnector


class CreateStockBaseData:

    def __init__(self, stock_info: dict, mongodb_connector: MongoDBConnector):
        self.ticker = stock_info.get("symbol", None)
        self.name = stock_info.get("longName", None)
        self.pe = stock_info.get("trailingPE", None)
        self.forward_pe = stock_info.get("forwardPE", None)
        self.ps = stock_info.get("priceToSalesTrailing12Months", None)
        self.pb = stock_info.get("priceToBook", None)
        self.peg = stock_info.get("trailingPegRatio", None)

        self.gross_margins = stock_info.get("grossMargins", None)

        self.currency = stock_info.get("currency", None)
        self.price = stock_info.get("currentPrice", None)
        self.market_cap = stock_info.get("marketCap", None)

        self.revenue_growth = stock_info.get("revenueGrowth", None)
        self.earnings_growth = stock_info.get("earningsQuarterlyGrowth", None)

        self.current_ratio = stock_info.get("currentRatio", None)
        self.debt_to_equity = stock_info.get("debtToEquity", None)
        self.dividend_yield = stock_info.get("dividendYield", None)

        self.sector = stock_info.get("sector", None)
        self.industry = stock_info.get("industry", None)
        self.full_time_employees = stock_info.get("fullTimeEmployees", None)

        self.beta = stock_info.get("beta", None)
        self.all_time_high = stock_info.get("allTimeHigh", None)
        self.fifty_two_week_high  = stock_info.get("fiftyTwoWeekHigh", None)
        self.fifty_two_week_low = stock_info.get("fiftyTwoWeekLow", None)

        self.short_percent_of_float = stock_info.get("shortPercentOfFloat", None)
        self.short_ratio = stock_info.get("shortRatio", None)
        self.held_percent_institutions = stock_info.get("heldPercentInstitutions", None)
        self.held_percent_insiders = stock_info.get("heldPercentInsiders", None)

        self.recommendation_mean = stock_info.get("recommendationMean", None)
        self.target_high_price = stock_info.get("targetHighPrice", None)
        self.target_low_price = stock_info.get("targetLowPrice", None)
        self.target_mean_price = stock_info.get("targetMeanPrice", None)
        self.target_median_price = stock_info.get("targetMedianPrice", None)

        # Save to db
        query = {"ticker": self.ticker}
        mongodb_connector.insert_or_replace("stock_base_data", query, self.__dict__)
