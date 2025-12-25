import yfinance as yf


class YahooStockData:

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.stock_ticker = yf.Ticker(ticker)

    def get_base_info(self) -> dict:
        return self.stock_ticker.info



