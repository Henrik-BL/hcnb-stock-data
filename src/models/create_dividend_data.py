from typing import Any
import json
from pandas import DataFrame

from src.config.db_collections import DIVIDENDS_COLLECTION
from src.mongo_db_connector import MongoDBConnector


class CreateDividendData:

    def __init__(self, ticker: str, dividends: DataFrame, mongodb_connector: MongoDBConnector):
        self.dividend_list = self._get_formatted_dividends(dividends)
        dividend_json_doc = {
            "ticker": ticker,
            "dividends": self.dividend_list
        }
        query = {
            "ticker": ticker,
        }
        mongodb_connector.insert_or_replace(DIVIDENDS_COLLECTION, query, dividend_json_doc)

    @staticmethod
    def _get_formatted_dividends(dividends: DataFrame) -> str | list[Any]:
        if dividends.empty:
            return json.dumps([])
        df = dividends.reset_index()
        df['Year'] = df['Date'].dt.year
        json_list = []
        for year, group in df.groupby('Year'):
            year_data = {
                "year": str(year),
                "total_dividend": round(float(group['Dividends'].sum()), 4),
                "payout_count": int(group['Dividends'].count()),
                "individual_payouts": [
                    {
                        "date": date.strftime('%Y-%m-%d'),
                        "amount": float(amount)
                    }
                    for date, amount in zip(group['Date'], group['Dividends'])
                ]
            }
            json_list.append(year_data)
        json_list.sort(key=lambda x: x['year'])
        return json_list
