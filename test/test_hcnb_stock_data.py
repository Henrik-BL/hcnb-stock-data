from datetime import date
from unittest.mock import MagicMock

import pandas as pd
import pytest

import hcnb_stock_data.hcnb_stock_data as hcnb_module
from hcnb_stock_data.config.db_collections import QUARTERLY_REPORT_DATA_COLLECTION
from hcnb_stock_data.hcnb_stock_data import HcnbStockData
from hcnb_stock_data.models.create_stock_report_quarterly_data import CreateStockReportQuarterlyData
from hcnb_stock_data.yahoo_stock_data import YahooStockData

QUARTERS = [pd.Timestamp("2025-09-30"), pd.Timestamp("2025-12-31")]


def _statement(rows: dict, columns=QUARTERS) -> pd.DataFrame:
    return pd.DataFrame(rows, index=columns).T


def _reports(net_income=(100.0, 120.0), free_cashflow=(50.0, 60.0)):
    income = _statement({
        "Total Revenue": [1000.0, 1100.0],
        "Net Income": list(net_income),
        "Basic Average Shares": [10.0, 10.0],
        "Diluted Average Shares": [11.0, 11.0],
    })
    balance = _statement({"Total Debt": [500.0, 450.0]})
    cashflow = _statement({"Free Cash Flow": list(free_cashflow)})
    return income, balance, cashflow


class FakeYahoo:
    def __init__(self, ticker):
        self.ticker = ticker

    def get_base_info(self):
        return {"symbol": self.ticker.upper(), "longName": "ABC Corp", "marketCap": 2_000, "currency": "USD"}

    def get_report_quarterly_data(self):
        return _reports()

    def get_report_yearly_data(self):
        return _reports()

    def get_dividend_data(self):
        dates = pd.to_datetime(["2024-03-01", "2025-03-01"])
        return pd.Series([1.0, 1.1], index=pd.DatetimeIndex(dates, name="Date"), name="Dividends")

    def get_price_data(self):
        return pd.DataFrame({"Close": [float(p) for p in range(1, 61)] + [float("nan")]})

    def get_calendar_data(self):
        return {"Earnings Date": [date(2999, 1, 20)], "Earnings Average": 1.5}


@pytest.fixture
def app(mongo, monkeypatch):
    monkeypatch.setattr(hcnb_module, "YahooStockData", FakeYahoo)
    instance = HcnbStockData.__new__(HcnbStockData)
    instance.mongo_db_connector = mongo
    instance.update_limit_hours = 0
    instance.fear_greed_index = None
    return instance


def test_get_stock_data_fetches_and_builds(app):
    stock_data = app.get_stock_data("ABC")

    assert stock_data.ticker == "ABC"
    assert stock_data.name == "ABC Corp"
    assert stock_data.last_quarter_pe == round(2_000 / (120 * 4), 2)
    assert [r["date"] for r in stock_data.quarterly_reports] == ["2025-09-30", "2025-12-31"]
    assert stock_data.sma_50 == 35.5  # NaN close is dropped
    assert stock_data.rsi_14 == 100.0
    assert stock_data.next_earnings_date == "2999-01-20"


def test_lowercase_ticker_is_readable(app):
    # Base data used to be stored under Yahoo's symbol ("ABC"), making "abc" unreadable
    stock_data = app.get_stock_data("abc")

    assert stock_data.ticker == "abc"
    assert stock_data.name == "ABC Corp"


def test_get_stock_data_without_update_for_unknown_ticker(app):
    with pytest.raises(LookupError):
        app.get_stock_data("NOPE", update_data=False)


def test_quarterly_reports_update_without_losing_values(mongo):
    CreateStockReportQuarterlyData("ABC", _reports(), mongo)
    # A later fetch revises net income but is missing free cash flow
    CreateStockReportQuarterlyData("ABC", _reports(net_income=(100.0, 130.0), free_cashflow=(None, None)), mongo)

    docs = sorted(mongo.fetch_many(QUARTERLY_REPORT_DATA_COLLECTION, {"ticker": "ABC"}), key=lambda d: d["quarter"])

    assert len(docs) == 2
    assert docs[1]["net_income"] == 130.0
    assert docs[1]["free_cashflow"] == 60.0


def test_yahoo_base_info_without_optional_fields(monkeypatch):
    fake_ticker = MagicMock()
    fake_ticker.info = {"symbol": "SPY", "longName": "SPDR S&P 500"}
    monkeypatch.setattr("hcnb_stock_data.yahoo_stock_data.yf.Ticker", lambda ticker: fake_ticker)

    assert YahooStockData("SPY").get_base_info() == {"symbol": "SPY", "longName": "SPDR S&P 500"}


def test_yahoo_base_info_strips_large_fields(monkeypatch):
    fake_ticker = MagicMock()
    fake_ticker.info = {"symbol": "ABC", "companyOfficers": [], "longBusinessSummary": "..."}
    monkeypatch.setattr("hcnb_stock_data.yahoo_stock_data.yf.Ticker", lambda ticker: fake_ticker)

    assert YahooStockData("ABC").get_base_info() == {"symbol": "ABC"}
