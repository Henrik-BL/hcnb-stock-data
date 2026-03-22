from pandas import DataFrame

from hcnb_stock_data.config.db_collections import PRICE_COLLECTION
from hcnb_stock_data.mongo_db_connector import MongoDBConnector


class CreatePriceData:

    def __init__(self, ticker: str, data: DataFrame, mongodb_connector: MongoDBConnector):
        dividend_json_doc = {
            "ticker": ticker,
            "close_prices": data['Close'].tolist()
        }
        query = {
            "ticker": ticker,
        }
        mongodb_connector.insert_or_replace(PRICE_COLLECTION, query, dividend_json_doc)
