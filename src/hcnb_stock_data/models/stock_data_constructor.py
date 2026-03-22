from hcnb_stock_data.models.calculated_data import CalculatedData
from hcnb_stock_data.models.stock_base_data import StockBaseData
from hcnb_stock_data.models.stock_dividend_data_summary import StockDividendDataSummary
from hcnb_stock_data.models.stock_price_data_summary import StockPriceDataSummary
from hcnb_stock_data.models.stock_quarterly_report_summary import StockQuarterlyReportSummary
from hcnb_stock_data.models.stock_yearly_report_summary import StockYearlyReportSummary
from hcnb_stock_data.mongo_db_connector import MongoDBConnector


class StockDataConstructor:

    def __init__(self, ticker: str, mongodb_connector: MongoDBConnector):
        self.base_data = StockBaseData(ticker, mongodb_connector)
        self.quarterly_data = StockQuarterlyReportSummary(ticker, mongodb_connector)
        self.yearly_data = StockYearlyReportSummary(ticker, mongodb_connector)
        self.dividend_data = StockDividendDataSummary(ticker, mongodb_connector)
        self.price_data = StockPriceDataSummary(ticker, mongodb_connector)
        self.calculated_data = CalculatedData(ticker, self.base_data, self.quarterly_data)

    def __str__(self):
        return f"StockData: {self.base_data.ticker}"
