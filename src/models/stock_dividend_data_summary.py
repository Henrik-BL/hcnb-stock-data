import json

from src.calculator import Calculator
from src.config.db_collections import DIVIDENDS_COLLECTION
from src.mongo_db_connector import MongoDBConnector
from datetime import datetime


class StockDividendDataSummary:

    def __init__(self, ticker: str, mongodb_connector: MongoDBConnector):
        self.ticker = ticker
        query = {"ticker": ticker}
        document = mongodb_connector.fetch_one(DIVIDENDS_COLLECTION, query)
        self.consecutive_dividend_increases = self._get_consecutive_dividend_increases(document)
        self.payouts = self._get_payouts(document)
        self.five_year_dividend_cagr = self._calculate_dividend_cagr(5, document)
        self.ten_year_dividend_cagr = self._calculate_dividend_cagr(10, document)

    @staticmethod
    def _get_consecutive_dividend_increases(document: dict) -> int:
        current_year = datetime.now().year

        temp_list = document.get("dividends", [])

        if temp_list == '[]':
            temp_list = []

        if len(temp_list) < 2:
            return 0

        temp_list = list(temp_list)
        temp_list = [x for x in temp_list if x.get("year") != str(current_year)]
        consecutive = 0
        previous_total_dividend = temp_list[-1].get("total_dividend", 0)
        for i in range(len(temp_list) - 2, -1, -1):
            current_total_dividend = temp_list[i].get("total_dividend", 0)
            if previous_total_dividend > current_total_dividend:
                consecutive += 1
            else:
                break
            previous_total_dividend = temp_list[i].get("total_dividend", 0)
        return consecutive

    @staticmethod
    def _get_payouts(document: dict) -> int:
        temp_list = document.get("dividends", [])
        if temp_list == '[]':
            temp_list = []

        temp_list = [x for x in temp_list if x.get("year") != str(datetime.now().year)]

        if not temp_list:
            return 0

        return len(temp_list[-1].get("individual_payouts", []))

    @staticmethod
    def _calculate_dividend_cagr(years: int, document: dict) -> float:
        current_year = datetime.now().year
        temp_list = document.get("dividends", [])
        if temp_list == '[]':
            temp_list = []
        temp_list = [x for x in temp_list if x.get("year") != str(current_year)]
        if len(temp_list) < (years - 1):
            return 0
        last_items = temp_list[-years:]
        start_value = last_items[0].get("total_dividend", 0)
        end_value = last_items[-1].get("total_dividend", 0)
        return Calculator.calculate_cagr(start_value, end_value, years)

    def __str__(self):
        return f"<StockDividendDataSummary> {self.ticker}"