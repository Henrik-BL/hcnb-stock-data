from datetime import datetime

import pytest

from hcnb_stock_data.config.db_collections import (
    DIVIDENDS_COLLECTION,
    PRICE_COLLECTION,
    QUARTERLY_REPORT_DATA_COLLECTION,
)
from hcnb_stock_data.models.calculated_data import CalculatedData
from hcnb_stock_data.models.stock_base_data import StockBaseData
from hcnb_stock_data.models.stock_dividend_data_summary import StockDividendDataSummary
from hcnb_stock_data.models.stock_price_data_summary import StockPriceDataSummary
from hcnb_stock_data.models.stock_quarterly_report_summary import StockQuarterlyReportSummary


def _dividend_years(totals, last_year=None):
    """Full years of dividend totals ending in last_year (default: last calendar year)."""
    last_year = last_year or datetime.now().year - 1
    first_year = last_year - len(totals) + 1
    return [
        {"year": str(first_year + i), "total_dividend": total, "payout_count": 4,
         "individual_payouts": [{"date": f"{first_year + i}-03-01", "amount": total / 4}] * 4}
        for i, total in enumerate(totals)
    ]


def test_dividend_cagr_uses_n_growth_periods(mongo):
    # 1.00 -> 1.10^5 over 6 full years is exactly 10% per year for 5 years
    totals = [round(1.1 ** i, 6) for i in range(6)]
    mongo.insert_one(DIVIDENDS_COLLECTION, {"ticker": "ABC", "dividends": _dividend_years(totals)})

    summary = StockDividendDataSummary("ABC", mongo)

    assert summary.five_year_dividend_cagr == 10.0
    assert summary.ten_year_dividend_cagr is None
    assert summary.consecutive_dividend_increases == 5
    assert summary.payouts == 4


def test_dividend_cagr_ignores_current_partial_year(mongo):
    totals = [round(1.1 ** i, 6) for i in range(6)]
    dividends = _dividend_years(totals)
    dividends.append({"year": str(datetime.now().year), "total_dividend": 0.1,
                      "payout_count": 1, "individual_payouts": []})
    mongo.insert_one(DIVIDENDS_COLLECTION, {"ticker": "ABC", "dividends": dividends})

    assert StockDividendDataSummary("ABC", mongo).five_year_dividend_cagr == 10.0


def test_dividend_cagr_none_with_too_few_years(mongo):
    mongo.insert_one(DIVIDENDS_COLLECTION, {"ticker": "ABC", "dividends": _dividend_years([1, 1.1, 1.2, 1.3, 1.4])})

    assert StockDividendDataSummary("ABC", mongo).five_year_dividend_cagr is None


@pytest.mark.parametrize("stored", ["[]", None])
def test_dividend_summary_without_dividends(mongo, stored):
    if stored is not None:
        mongo.insert_one(DIVIDENDS_COLLECTION, {"ticker": "ABC", "dividends": stored})

    summary = StockDividendDataSummary("ABC", mongo)

    assert summary.consecutive_dividend_increases == 0
    assert summary.payouts == 0
    assert summary.five_year_dividend_cagr is None


def test_price_summary(mongo):
    prices = [float(p) for p in range(1, 301)]
    mongo.insert_one(PRICE_COLLECTION, {"ticker": "ABC", "close_prices": prices})

    summary = StockPriceDataSummary("ABC", mongo)

    assert summary.latest_price == 300.0
    assert summary.sma_50 == 275.5
    assert summary.sma_225 == 188.0
    assert summary.sma_50_diff == round((300 / 275.5 - 1) * 100, 2)
    assert summary.rsi_14 == 100.0


def test_price_summary_without_price_document(mongo):
    summary = StockPriceDataSummary("ABC", mongo)

    assert summary.latest_price is None
    assert summary.sma_50 is None
    assert summary.sma_50_diff is None
    assert summary.rsi_14 is None


def test_base_data_missing_ticker_raises_lookup_error(mongo):
    with pytest.raises(LookupError, match="ABC"):
        StockBaseData("ABC", mongo)


def test_calculated_data_handles_missing_quarter_values(mongo):
    mongo.insert_one("stock_base_data", {"ticker": "ABC", "market_cap": 1_000_000})
    mongo.insert_one(QUARTERLY_REPORT_DATA_COLLECTION, {
        "ticker": "ABC", "quarter": "2026-06-30", "revenue": 1000.0,
        "net_income": None, "free_cashflow": None,
    })

    base = StockBaseData("ABC", mongo)
    quarterly = StockQuarterlyReportSummary("ABC", mongo)
    calculated = CalculatedData("ABC", base, quarterly)

    assert calculated.last_quarter_pe is None
    assert calculated.last_quarter_free_cashflow_yield is None
    assert calculated.last_quarter_margin is None
    assert quarterly.report_list[0].net_margin == 0.0


def test_calculated_data_last_quarter_values(mongo):
    mongo.insert_one("stock_base_data", {"ticker": "ABC", "market_cap": 1_000_000})
    mongo.insert_one(QUARTERLY_REPORT_DATA_COLLECTION, {
        "ticker": "ABC", "quarter": "2026-06-30", "revenue": 50_000.0,
        "net_income": 10_000.0, "free_cashflow": 5_000.0,
    })

    base = StockBaseData("ABC", mongo)
    calculated = CalculatedData("ABC", base, StockQuarterlyReportSummary("ABC", mongo))

    assert calculated.last_quarter_pe == 25.0
    assert calculated.last_quarter_free_cashflow_yield == 2.0
    assert calculated.last_quarter_margin == 20.0
