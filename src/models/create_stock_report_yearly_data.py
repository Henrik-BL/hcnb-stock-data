from pandas import DataFrame
import pandas as pd

from src.config.db_collections import YEARLY_REPORT_DATA_COLLECTION
from src.mongo_db_connector import MongoDBConnector


class CreateStockReportYearlyData:

    def __init__(self, ticker: str, report_yearly_data: tuple, mongodb_connector: MongoDBConnector):
        self.ticker = ticker
        self.json_data_list = self._get_json_data_list(report_yearly_data)

        for json_data in self.json_data_list:
            query = {"ticker": self.ticker, "year": json_data["year"]}
            mongodb_connector.insert_if_not_exists(YEARLY_REPORT_DATA_COLLECTION, query, json_data)

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
                    if k not in combined[key]:
                        combined[key][k] = v

        return list(combined.values())

    def _get_income_statement_json_list(self, income_stmt_q: DataFrame) -> list:
        revenue = income_stmt_q.loc["Total Revenue"]
        net_income = income_stmt_q.loc["Net Income"]
        outstanding_shares = income_stmt_q.loc["Basic Average Shares"]
        diluted_outstanding_shares = income_stmt_q.loc["Diluted Average Shares"]

        result = []

        for year in income_stmt_q.columns:
            rev = revenue[year]
            ni = net_income[year]
            o_s = outstanding_shares[year]
            d_o_s = diluted_outstanding_shares[year]

            if pd.isna(rev) or pd.isna(ni) or pd.isna(o_s) or pd.isna(d_o_s):
                continue

            result.append({
                "ticker": self.ticker,
                "year": year.strftime("%Y-%m-%d"),
                "revenue": float(rev),
                "net_income": float(ni),
                "outstanding_shares": int(o_s),
                "diluted_outstanding_shares": int(d_o_s)
            })

        return result

    def _get_balance_statement_json_list(self, balance_stmt_q: DataFrame) -> list:
        total_debt = balance_stmt_q.loc["Total Debt"]
        result = []

        for year in balance_stmt_q.columns:
            t_debt = total_debt[year]
            if pd.isna(t_debt):
                continue
            result.append({
                "ticker": self.ticker,
                "year": year.strftime("%Y-%m-%d"),
                "total_debt": float(t_debt)
            })
        return result

    def _get_cashflow_statement_json_list(self, cashflow_stmt_q: DataFrame) -> list:
        free_cashflow = cashflow_stmt_q.loc["Free Cash Flow"]
        result = []
        for year in cashflow_stmt_q.columns:
            fc_flow = free_cashflow[year]
            if pd.isna(fc_flow):
                continue
            result.append({
                "ticker": self.ticker,
                "year": year.strftime("%Y-%m-%d"),
                "free_cashflow": float(fc_flow)
            })
        return result
