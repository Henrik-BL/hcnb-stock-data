from typing import Any

from hcnb_stock_data.models.stock_base_data import StockBaseData
from hcnb_stock_data.models.stock_quarterly_report_summary import StockQuarterlyReportSummary


class CalculatedData:
    def __init__(self, ticker: str, base_data: StockBaseData, quarterly_reports: StockQuarterlyReportSummary):
        self.ticker = ticker
        self.revenue_growth = self._get_revenue_growth(base_data)
        self.earnings_growth = self._get_earnings_growth(base_data)
        self.last_quarter_pe = self._get_last_quarter_pe(base_data, quarterly_reports)
        self.last_quarter_free_cashflow_yield = self._get_last_quarter_free_cashflow_yield(base_data, quarterly_reports)
        self.last_quarter_date = self._get_last_quarter_date(quarterly_reports)
        self.last_quarter_revenue = self._get_last_quarter_revenue(quarterly_reports)
        self.last_quarter_net_income = self._get_last_quarter_net_income(quarterly_reports)
        self.last_quarter_free_cashflow = self._get_last_quarter_free_cashflow(quarterly_reports)
        self.last_quarter_margin = self._get_last_quarter_margin()

    def __str__(self):
        return f"<StockPriceDataSummary> {self.ticker}"

    @staticmethod
    def _get_revenue_growth(base_data: StockBaseData) -> float:
        revenue_growth = base_data.revenue_growth * 100
        return round(revenue_growth, 3)

    @staticmethod
    def _get_earnings_growth(base_data: StockBaseData) -> Any | None:
        if base_data.earnings_growth is None:
            return None
        earnings_growth = base_data.earnings_growth * 100
        return round(earnings_growth, 3)

    @staticmethod
    def _get_last_quarter_pe(base_data: StockBaseData, quarterly_reports: StockQuarterlyReportSummary):
        if not quarterly_reports.report_list or not base_data.market_cap:
            return None
        last_quarter_earnings = quarterly_reports.report_list[-1].net_income
        yearly_earnings = last_quarter_earnings * 4

        if yearly_earnings == 0 or last_quarter_earnings == 0:
            return None

        return round(base_data.market_cap / yearly_earnings, 2)

    @staticmethod
    def _get_last_quarter_free_cashflow_yield(base_data: StockBaseData, quarterly_reports: StockQuarterlyReportSummary):
        if not quarterly_reports.report_list or not base_data.market_cap:
            return None

        last_quarter_free_cash_flow = quarterly_reports.report_list[-1].free_cashflow
        yearly_free_cash_flow = last_quarter_free_cash_flow * 4

        if last_quarter_free_cash_flow == 0 or yearly_free_cash_flow == 0:
            return None

        free_cash_flow_yield = round(yearly_free_cash_flow / base_data.market_cap, 5)

        return round(free_cash_flow_yield * 100, 2)

    @staticmethod
    def _get_last_quarter_date(quarterly_reports: StockQuarterlyReportSummary):
        if not quarterly_reports.report_list:
            return None
        latest_quarter = quarterly_reports.report_list[-1]
        return latest_quarter.quarter

    @staticmethod
    def _get_last_quarter_revenue(quarterly_reports: StockQuarterlyReportSummary):
        if not quarterly_reports.report_list:
            return None
        latest_quarter = quarterly_reports.report_list[-1]
        return latest_quarter.revenue

    @staticmethod
    def _get_last_quarter_net_income(quarterly_reports: StockQuarterlyReportSummary):
        if not quarterly_reports.report_list:
            return None
        latest_quarter = quarterly_reports.report_list[-1]
        return latest_quarter.net_income

    @staticmethod
    def _get_last_quarter_free_cashflow(quarterly_reports: StockQuarterlyReportSummary):
        if not quarterly_reports.report_list:
            return None
        latest_quarter = quarterly_reports.report_list[-1]
        return latest_quarter.free_cashflow

    def _get_last_quarter_margin(self):
        if not self.last_quarter_revenue or not self.last_quarter_net_income:
            return None
        calculated_margin = round(self.last_quarter_net_income / self.last_quarter_revenue, 5)
        calculated_margin = round(calculated_margin * 100, 2)
        return calculated_margin
