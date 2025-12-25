import yfinance as yf


class YahooStockData:

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.stock_ticker = yf.Ticker(ticker)

    def get_base_info(self) -> dict:
        info_dict = self.stock_ticker.info
        info_dict.pop('companyOfficers')
        info_dict.pop('longBusinessSummary')
        return info_dict

    def get_report_quarterly_data(self):
        income_stmt_q = self.stock_ticker.quarterly_financials
        balance_sheet_q = self.stock_ticker.quarterly_balance_sheet
        cashflow_q = self.stock_ticker.quarterly_cashflow
        return income_stmt_q, balance_sheet_q, cashflow_q


# y = YahooStockData('PLTR')

# y.get_report_quarterly_data()
