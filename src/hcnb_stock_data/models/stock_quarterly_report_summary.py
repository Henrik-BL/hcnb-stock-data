from hcnb_stock_data.calculator import Calculator
from hcnb_stock_data.config.db_collections import QUARTERLY_REPORT_DATA_COLLECTION
from hcnb_stock_data.models.stock_quarterly_report_data import StockQuarterlyReportData
from hcnb_stock_data.mongo_db_connector import MongoDBConnector


class StockQuarterlyReportSummary:

    def __init__(self, ticker: str, mongodb_connector: MongoDBConnector):
        self.ticker = ticker
        query = {"ticker": ticker}
        documents = mongodb_connector.fetch_many(QUARTERLY_REPORT_DATA_COLLECTION, query)
        self.report_list = self._get_report_list(documents)
        self.revenue_cagr = self.calculate_metric_cagr("revenue")
        self.net_income_cagr = self.calculate_metric_cagr("net_income")
        self.outstanding_shares_cagr = self.calculate_metric_cagr("outstanding_shares")
        self.diluted_outstanding_shares_cagr = self.calculate_metric_cagr("diluted_outstanding_shares")
        self.total_debt_cagr = self.calculate_metric_cagr("total_debt")
        self.free_cashflow_cagr = self.calculate_metric_cagr("free_cashflow")
        self.margin_difference_yoy = self.get_margin_difference_yoy()

    @staticmethod
    def _get_report_list(documents):
        result = []
        for item in documents:
            result.append(StockQuarterlyReportData(item))
        sorted_reports = sorted(result, key=lambda x: x.quarter)
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

    def get_margin_difference_yoy(self) -> float | None:
        latest_quarter_margin = self.report_list[-1].net_margin if self.report_list else None
        margin_one_year_ago = self.report_list[-5].net_margin if len(self.report_list) >= 5 else None
        if latest_quarter_margin is None or margin_one_year_ago is None:
            return None
        return round(latest_quarter_margin - margin_one_year_ago, 2)


    def __str__(self):
        return f"<StockQuarterlyReportSummary> {self.ticker}"