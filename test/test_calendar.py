from datetime import date
from unittest.mock import MagicMock, PropertyMock

import pandas as pd

from hcnb_stock_data.config.db_collections import CALENDAR_COLLECTION
from hcnb_stock_data.hcnb_stock_data import HcnbStockData
from hcnb_stock_data.models.create_calendar_data import CreateCalendarData
from hcnb_stock_data.models.stock_calendar_data_summary import StockCalendarDataSummary
from hcnb_stock_data.yahoo_stock_data import YahooStockData

TODAY = date(2026, 9, 26)

YAHOO_CALENDAR = {
    "Dividend Date": date(2026, 10, 1),
    "Ex-Dividend Date": date(2026, 9, 15),
    "Earnings Date": [date(2026, 10, 20)],
    "Earnings High": 0.89,
    "Earnings Low": 0.85,
    "Earnings Average": 0.87,
    "Revenue High": 13_029_000_000,
    "Revenue Low": 12_813_800_000,
    "Revenue Average": 12_891_810_140,
}


def test_calendar_events_are_stored(mongo):
    CreateCalendarData("KO", YAHOO_CALENDAR, mongo)

    events = mongo.fetch_one(CALENDAR_COLLECTION, {"ticker": "KO"})["events"]

    assert [(e["type"], e["date"]) for e in events] == [
        ("ex_dividend", "2026-09-15"),
        ("dividend_payment", "2026-10-01"),
        ("earnings", "2026-10-20"),
    ]
    assert events[2]["eps_average"] == 0.87
    assert events[2]["revenue_high"] == 13_029_000_000.0


def test_summary_only_keeps_future_events(mongo):
    CreateCalendarData("KO", YAHOO_CALENDAR, mongo)

    summary = StockCalendarDataSummary("KO", mongo, today=TODAY)

    assert [e["type"] for e in summary.future_events] == ["dividend_payment", "earnings"]
    assert summary.next_earnings_date == "2026-10-20"
    assert summary.next_dividend_payment_date == "2026-10-01"
    assert summary.next_ex_dividend_date is None  # already passed


def test_event_today_counts_as_future(mongo):
    CreateCalendarData("KO", {"Ex-Dividend Date": TODAY}, mongo)

    assert StockCalendarDataSummary("KO", mongo, today=TODAY).next_ex_dividend_date == "2026-09-26"


def test_unconfirmed_earnings_range(mongo):
    CreateCalendarData("ABC", {"Earnings Date": [pd.Timestamp("2026-10-30"), pd.Timestamp("2026-09-25")]}, mongo)

    event = mongo.fetch_one(CALENDAR_COLLECTION, {"ticker": "ABC"})["events"][0]
    assert (event["date"], event["date_end"]) == ("2026-09-25", "2026-10-30")
    assert event["eps_average"] is None
    # Range has started but not ended, so it's still upcoming
    assert StockCalendarDataSummary("ABC", mongo, today=TODAY).next_earnings_date == "2026-09-25"


def test_empty_calendar(mongo):
    CreateCalendarData("SPY", {}, mongo)

    summary = StockCalendarDataSummary("SPY", mongo, today=TODAY)
    assert summary.future_events == []
    assert summary.next_earnings_date is None


def test_summary_without_stored_calendar(mongo):
    assert StockCalendarDataSummary("NOPE", mongo).future_events == []


def test_future_events_across_tickers(mongo):
    CreateCalendarData("KO", {"Earnings Date": [date(2999, 3, 1)]}, mongo)
    CreateCalendarData("AAPL", {"Earnings Date": [date(2999, 2, 1)], "Ex-Dividend Date": date(2000, 1, 1)}, mongo)
    CreateCalendarData("MSFT", {"Earnings Date": [date(2999, 1, 1)]}, mongo)
    app = HcnbStockData.__new__(HcnbStockData)
    app.mongo_db_connector = mongo

    assert [(e["ticker"], e["date"]) for e in app.get_future_events()] == [
        ("MSFT", "2999-01-01"), ("AAPL", "2999-02-01"), ("KO", "2999-03-01"),
    ]
    assert [e["ticker"] for e in app.get_future_events(["KO", "AAPL"])] == ["AAPL", "KO"]


def test_yahoo_calendar_missing_for_funds(monkeypatch):
    fake_ticker = MagicMock()
    type(fake_ticker).calendar = PropertyMock(side_effect=Exception("404 Not Found"))
    monkeypatch.setattr("hcnb_stock_data.yahoo_stock_data.yf.Ticker", lambda ticker: fake_ticker)

    assert YahooStockData("SPY").get_calendar_data() == {}


def _dividend_history(*payouts):
    dates = pd.DatetimeIndex([pd.Timestamp(d, tz="America/New_York") for d, _ in payouts], name="Date")
    return pd.Series([amount for _, amount in payouts], index=dates, name="Dividends")


def test_dividend_amount_from_history_once_ex_date_passed(mongo):
    dividends = _dividend_history(("2026-06-15 09:30", 0.51), ("2026-09-15 09:30", 0.53))
    CreateCalendarData("KO", YAHOO_CALENDAR, mongo, dividends=dividends,
                       base_info={"currency": "USD", "lastDividendValue": 0.51})

    payment = StockCalendarDataSummary("KO", mongo, today=TODAY).future_events[0]

    assert payment == {"type": "dividend_payment", "date": "2026-10-01",
                       "amount": 0.53, "amount_estimated": False, "currency": "USD"}


def test_dividend_amount_estimated_before_ex_date(mongo):
    dividends = _dividend_history(("2026-06-15 09:30", 0.51))
    CreateCalendarData("KO", YAHOO_CALENDAR, mongo, dividends=dividends,
                       base_info={"currency": "USD", "lastDividendValue": 0.51})

    events = mongo.fetch_one(CALENDAR_COLLECTION, {"ticker": "KO"})["events"]
    ex_dividend = next(e for e in events if e["type"] == "ex_dividend")

    assert (ex_dividend["amount"], ex_dividend["amount_estimated"]) == (0.51, True)


def test_dividend_amount_unknown(mongo):
    CreateCalendarData("KO", YAHOO_CALENDAR, mongo)

    event = mongo.fetch_one(CALENDAR_COLLECTION, {"ticker": "KO"})["events"][0]
    assert (event["amount"], event["amount_estimated"], event["currency"]) == (None, None, None)
