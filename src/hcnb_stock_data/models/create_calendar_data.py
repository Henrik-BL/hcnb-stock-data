from typing import Any

import pandas as pd

from hcnb_stock_data.config.db_collections import CALENDAR_COLLECTION
from hcnb_stock_data.mongo_db_connector import MongoDBConnector

EARNINGS = "earnings"
EX_DIVIDEND = "ex_dividend"
DIVIDEND_PAYMENT = "dividend_payment"

_ESTIMATE_FIELDS = {
    "Earnings Average": "eps_average",
    "Earnings Low": "eps_low",
    "Earnings High": "eps_high",
    "Revenue Average": "revenue_average",
    "Revenue Low": "revenue_low",
    "Revenue High": "revenue_high",
}


class CreateCalendarData:

    def __init__(self, ticker: str, calendar: dict, mongodb_connector: MongoDBConnector,
                 dividends: pd.Series | None = None, base_info: dict | None = None):
        self.events = self._get_events(calendar or {}, dividends, base_info or {})
        calendar_json_doc = {
            "ticker": ticker,
            "events": self.events
        }
        query = {
            "ticker": ticker,
        }
        mongodb_connector.insert_or_replace(CALENDAR_COLLECTION, query, calendar_json_doc)

    def _get_events(self, calendar: dict, dividends: pd.Series | None, base_info: dict) -> list[dict[str, Any]]:
        events = []

        earnings_dates = [self._format_date(d) for d in self._as_list(calendar.get("Earnings Date"))]
        earnings_dates = sorted(d for d in earnings_dates if d)
        if earnings_dates:
            earnings_event = {"type": EARNINGS, "date": earnings_dates[0]}
            # Yahoo gives a date range when the report day isn't confirmed yet
            if len(earnings_dates) > 1:
                earnings_event["date_end"] = earnings_dates[-1]
            for yahoo_key, key in _ESTIMATE_FIELDS.items():
                earnings_event[key] = self._to_float(calendar.get(yahoo_key))
            events.append(earnings_event)

        dividend_details = self._get_dividend_details(
            self._format_date(calendar.get("Ex-Dividend Date")), dividends, base_info)
        for yahoo_key, event_type in (("Ex-Dividend Date", EX_DIVIDEND), ("Dividend Date", DIVIDEND_PAYMENT)):
            event_date = self._format_date(calendar.get(yahoo_key))
            if event_date:
                events.append({"type": event_type, "date": event_date, **dividend_details})

        events.sort(key=lambda e: e["date"])
        return events

    def _get_dividend_details(self, ex_dividend_date: str | None, dividends: pd.Series | None,
                              base_info: dict) -> dict[str, Any]:
        """Amount per share of the upcoming payout. Exact once the ex-dividend date is in the
        dividend history, otherwise estimated from the last paid dividend."""
        amount = None
        if ex_dividend_date and dividends is not None and not dividends.empty:
            amounts = {self._format_date(d): value for d, value in dividends.items()}
            amount = self._to_float(amounts.get(ex_dividend_date))

        amount_estimated = amount is None
        if amount_estimated:
            amount = self._to_float(base_info.get("lastDividendValue"))

        return {
            "amount": amount,
            "amount_estimated": amount_estimated if amount is not None else None,
            "currency": base_info.get("currency"),
        }

    @staticmethod
    def _as_list(value) -> list:
        if value is None:
            return []
        if isinstance(value, (list, tuple)):
            return list(value)
        return [value]

    @staticmethod
    def _format_date(value) -> str | None:
        if value is None:
            return None
        try:
            # Keep the local exchange date for tz-aware timestamps from the dividend history
            timestamp = pd.Timestamp(value)
        except (TypeError, ValueError):
            return None
        if pd.isna(timestamp):
            return None
        return timestamp.strftime('%Y-%m-%d')

    @staticmethod
    def _to_float(value) -> float | None:
        if value is None:
            return None
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None
        return None if pd.isna(number) else number
