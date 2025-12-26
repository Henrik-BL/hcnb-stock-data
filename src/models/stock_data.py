from src.models.stock_base_data import StockBaseData
from src.models.stock_quarterly_report_summary import StockQuarterlyReportSummary
from src.models.stock_yearly_report_summary import StockYearlyReportSummary
from src.mongo_db_connector import MongoDBConnector


class StockData:

    def __init__(self, ticker: str, mongodb_connector: MongoDBConnector):
        self.base_data = StockBaseData(ticker, mongodb_connector)
        self.quarterly_reports_data = StockQuarterlyReportSummary(ticker, mongodb_connector)
        self.yearly_reports_data = StockYearlyReportSummary(ticker, mongodb_connector)


    def __str__(self):
        return f"Ticker: {self.base_data.ticker}"
