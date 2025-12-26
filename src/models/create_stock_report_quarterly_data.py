from pandas import DataFrame
import pandas as pd

from src.config.db_collections import QUARTERLY_REPORT_DATA_COLLECTION
from src.mongo_db_connector import MongoDBConnector


class CreateStockReportQuarterlyData:

    def __init__(self, ticker: str, report_quarterly_data: tuple,
                 mongodb_connector: MongoDBConnector):
        self.ticker = ticker
        self.json_data_list = self._get_json_data_list(report_quarterly_data)

        for json_data in self.json_data_list:
            query = {"ticker": self.ticker, "quarter": json_data["quarter"]}
            mongodb_connector.insert_if_not_exists(QUARTERLY_REPORT_DATA_COLLECTION, query, json_data)

    def _get_json_data_list(self, report_quarterly_data: tuple) -> list:
        result_income = self._get_income_statement_json_list(report_quarterly_data[0])
        result_balance = self._get_balance_statement_json_list(report_quarterly_data[1])
        result_cashflow = self._get_cashflow_statement_json_list(report_quarterly_data[2])

        combined = {}
        for lst in (result_income, result_balance, result_cashflow):
            for item in lst:
                key = (item["ticker"], item["quarter"])

                if key not in combined:
                    combined[key] = {}

                for k, v in item.items():
                    if k not in combined[key]:
                        combined[key][k] = v

        return list(combined.values())

    def _get_income_statement_json_list(self, income_stmt_q: DataFrame) -> list:
        revenue = income_stmt_q.loc["Total Revenue"]
        net_income = income_stmt_q.loc["Net Income"]
        outstanding_shares = income_stmt_q.loc["Basic Average Shares"]
        diluted_outstanding_shares = income_stmt_q.loc["Diluted Average Shares"]

        result = []

        for quarter in income_stmt_q.columns:
            rev = revenue[quarter]
            ni = net_income[quarter]
            o_s = outstanding_shares[quarter]
            d_o_s = diluted_outstanding_shares[quarter]

            if pd.isna(rev) or pd.isna(ni) or pd.isna(o_s) or pd.isna(d_o_s):
                continue

            result.append({
                "ticker": self.ticker,
                "quarter": quarter.strftime("%Y-%m-%d"),
                "revenue": float(rev),
                "net_income": float(ni),
                "outstanding_shares": int(o_s),
                "diluted_outstanding_shares": int(d_o_s)
            })

        return result

    def _get_balance_statement_json_list(self, balance_stmt_q: DataFrame) -> list:
        total_debt = balance_stmt_q.loc["Total Debt"]
        result = []

        for quarter in balance_stmt_q.columns:
            t_debt = total_debt[quarter]
            if pd.isna(t_debt):
                continue
            result.append({
                "ticker": self.ticker,
                "quarter": quarter.strftime("%Y-%m-%d"),
                "total_debt": float(t_debt)
            })
        return result

    def _get_cashflow_statement_json_list(self, cashflow_stmt_q: DataFrame) -> list:
        free_cashflow = cashflow_stmt_q.loc["Free Cash Flow"]
        result = []
        for quarter in cashflow_stmt_q.columns:
            fc_flow = free_cashflow[quarter]
            if pd.isna(fc_flow):
                continue
            result.append({
                "ticker": self.ticker,
                "quarter": quarter.strftime("%Y-%m-%d"),
                "free_cashflow": float(fc_flow)
            })
        return result
