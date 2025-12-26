from src.calculator import Calculator
from src.config.db_collections import YEARLY_REPORT_DATA_COLLECTION
from src.models.stock_yearly_report_data import StockYearlyReportData
from src.mongo_db_connector import MongoDBConnector


class StockYearlyReportSummary:

    def __init__(self, ticker: str, mongodb_connector: MongoDBConnector):
        query = {"ticker": ticker}
        documents = mongodb_connector.fetch_many(YEARLY_REPORT_DATA_COLLECTION, query)
        self.report_list = self._get_report_list(documents)
        self.revenue_cagr = self.calculate_metric_cagr("revenue")
        self.net_income_cagr = self.calculate_metric_cagr("net_income")
        self.outstanding_shares_cagr = self.calculate_metric_cagr("outstanding_shares")
        self.diluted_outstanding_shares_cagr = self.calculate_metric_cagr("diluted_outstanding_shares")
        self.total_debt_cagr = self.calculate_metric_cagr("total_debt")
        self.free_cashflow_cagr = self.calculate_metric_cagr("free_cashflow")

    @staticmethod
    def _get_report_list(documents):
        result = []
        for item in documents:
            result.append(StockYearlyReportData(item))
        sorted_reports = sorted(result, key=lambda x: x.year)
        return sorted_reports

    def calculate_metric_cagr(self, attr_name: str) -> float:
        if not self.report_list or len(self.report_list) < 2:
            return 0.0
        first_val = getattr(self.report_list[0], attr_name, 0)
        last_val = getattr(self.report_list[-1], attr_name, 0)
        periods = len(self.report_list) - 1
        return Calculator.calculate_cagr(first_val, last_val, periods)
