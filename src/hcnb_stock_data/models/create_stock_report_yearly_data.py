from pandas import DataFrame
import pandas as pd

from hcnb_stock_data.config.db_collections import YEARLY_REPORT_DATA_COLLECTION
from hcnb_stock_data.mongo_db_connector import MongoDBConnector


class CreateStockReportYearlyData:

    def __init__(self, ticker: str, report_yearly_data: tuple, mongodb_connector: MongoDBConnector):
        self.ticker = ticker
        self.json_data_list = self._get_json_data_list(report_yearly_data)

        for json_data in self.json_data_list:
            query = {"ticker": self.ticker, "year": json_data["year"]}
            mongodb_connector.insert_if_not_exists(YEARLY_REPORT_DATA_COLLECTION, query, json_data)

    @staticmethod
    def _safe_cast(val, cast_type):
        if pd.isna(val):
            return None
        try:
            return cast_type(val)
        except (ValueError, TypeError):
            return None

    def _get_json_data_list(self, report_yearly_data: tuple) -> list:
        result_income = self._get_income_statement_json_list(report_yearly_data[0])
        result_balance = self._get_balance_statement_json_list(report_yearly_data[1])
        result_cashflow = self._get_cashflow_statement_json_list(report_yearly_data[2])

        combined = {}
        for lst in (result_income, result_balance, result_cashflow):
            for item in lst:
                key = (item["ticker"], item["year"])

                if key not in combined:
                    combined[key] = {}

                for k, v in item.items():
                    # Populate the dictionary, keeping existing values if already set
                    if k not in combined[key]:
                        combined[key][k] = v
                    # Optional: If a value was None but we found a real value in another list, update it
                    elif combined[key][k] is None and v is not None:
                        combined[key][k] = v

        return list(combined.values())

    def _get_income_statement_json_list(self, income_stmt_q: DataFrame) -> list:
        rows = ["Total Revenue", "Net Income", "Basic Average Shares", "Diluted Average Shares"]
        # reindex ensures all rows exist without throwing KeyError
        df_safe = income_stmt_q.reindex(rows)

        result = []
        for year in df_safe.columns:
            result.append({
                "ticker": self.ticker,
                "year": year.strftime("%Y-%m-%d") if hasattr(year, 'strftime') else str(year),
                "revenue": self._safe_cast(df_safe.loc["Total Revenue", year], float),
                "net_income": self._safe_cast(df_safe.loc["Net Income", year], float),
                "outstanding_shares": self._safe_cast(df_safe.loc["Basic Average Shares", year], int),
                "diluted_outstanding_shares": self._safe_cast(df_safe.loc["Diluted Average Shares", year], int)
            })
        return result

    def _get_balance_statement_json_list(self, balance_stmt_q: DataFrame) -> list:
        df_safe = balance_stmt_q.reindex(["Total Debt"])

        result = []
        for year in df_safe.columns:
            result.append({
                "ticker": self.ticker,
                "year": year.strftime("%Y-%m-%d") if hasattr(year, 'strftime') else str(year),
                "total_debt": self._safe_cast(df_safe.loc["Total Debt", year], float)
            })
        return result

    def _get_cashflow_statement_json_list(self, cashflow_stmt_q: DataFrame) -> list:
        df_safe = cashflow_stmt_q.reindex(["Free Cash Flow"])

        result = []
        for year in df_safe.columns:
            result.append({
                "ticker": self.ticker,
                "year": year.strftime("%Y-%m-%d") if hasattr(year, 'strftime') else str(year),
                "free_cashflow": self._safe_cast(df_safe.loc["Free Cash Flow", year], float)
            })
        return result