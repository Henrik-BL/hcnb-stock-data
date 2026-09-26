import yfinance as yf


class YahooStockData:

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.stock_ticker = yf.Ticker(ticker)

    def get_base_info(self) -> dict:
        info_dict = dict(self.stock_ticker.info or {})
        info_dict.pop('companyOfficers', None)
        info_dict.pop('longBusinessSummary', None)
        return info_dict

    def get_report_quarterly_data(self):
        income_stmt_q = self.stock_ticker.quarterly_financials
        balance_sheet_q = self.stock_ticker.quarterly_balance_sheet
        cashflow_q = self.stock_ticker.quarterly_cashflow
        return income_stmt_q, balance_sheet_q, cashflow_q

    def get_report_yearly_data(self):
        income_stmt_q = self.stock_ticker.financials
        balance_sheet_q = self.stock_ticker.balance_sheet
        cashflow_q = self.stock_ticker.cashflow
        return income_stmt_q, balance_sheet_q, cashflow_q

    def get_dividend_data(self):
        dividends = self.stock_ticker.dividends
        return dividends

    def get_price_data(self):
        # Adjusted prices so splits and dividends don't distort SMA/RSI
        data = self.stock_ticker.history(period="2y", auto_adjust=True)
        return data

    def get_calendar_data(self) -> dict:
        # Yahoo has no calendar for e.g. funds and ETFs and raises instead of returning empty
        try:
            return dict(self.stock_ticker.calendar or {})
        except Exception:
            return {}
