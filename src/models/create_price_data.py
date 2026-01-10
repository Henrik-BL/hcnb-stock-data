from pandas import DataFrame

from src.config.db_collections import PRICE_COLLECTION
from src.mongo_db_connector import MongoDBConnector


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
