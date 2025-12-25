from src.mongo_db_connector import MongoDBConnector


class CreateStockBaseData:

    def __init__(self, stock_info: dict, mongodb_connector: MongoDBConnector):
        self.ticker = stock_info.get("symbol", None)
        self.pe = stock_info.get("trailingPE", None)

        # Save to db
        query = {"ticker": self.ticker}
        mongodb_connector.insert_or_replace("stock_base_data", query, self.__dict__)
