from hcnb_stock_data.calculator import Calculator
from hcnb_stock_data.config.db_collections import YEARLY_REPORT_DATA_COLLECTION
from hcnb_stock_data.models.stock_yearly_report_data import StockYearlyReportData
from hcnb_stock_data.mongo_db_connector import MongoDBConnector


class StockYearlyReportSummary:

    def __init__(self, ticker: str, mongodb_connector: MongoDBConnector):
        self.ticker = ticker
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

    def calculate_metric_cagr(self, attr_name: str) -> float | None:
        if not self.report_list or len(self.report_list) < 2:
            return None
        first_val = getattr(self.report_list[0], attr_name, 0)
        last_val = getattr(self.report_list[-1], attr_name, 0)

        if first_val is None or last_val is None:
            return None

        periods = len(self.report_list) - 1
        return Calculator.calculate_cagr(first_val, last_val, periods)

    def __str__(self):
        return f"<StockYearlyReportSummary> {self.ticker}"