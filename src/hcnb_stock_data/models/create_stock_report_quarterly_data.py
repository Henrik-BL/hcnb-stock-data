import pandas as pd

from hcnb_stock_data.config.db_collections import QUARTERLY_REPORT_DATA_COLLECTION
from hcnb_stock_data.mongo_db_connector import MongoDBConnector


class CreateStockReportQuarterlyData:

    def __init__(self, ticker: str, report_quarterly_data: tuple,
                 mongodb_connector: MongoDBConnector):
        self.ticker = ticker
        self.json_data_list = self._get_json_data_list(report_quarterly_data)

        for json_data in self.json_data_list:
            query = {"ticker": self.ticker, "quarter": json_data["quarter"]}

            revenue = json_data.get("revenue")

            if revenue:
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

    def _get_income_statement_json_list(self, income_stmt_q: pd.DataFrame) -> list:
        required_rows = ["Total Revenue", "Net Income", "Basic Average Shares", "Diluted Average Shares"]
        df_safe = income_stmt_q.reindex(required_rows)
        result = []

        for quarter in df_safe.columns:
            rev = df_safe.loc["Total Revenue", quarter]
            ni = df_safe.loc["Net Income", quarter]
            o_s = df_safe.loc["Basic Average Shares", quarter]
            d_o_s = df_safe.loc["Diluted Average Shares", quarter]

            def safe_cast(val, cast_type):
                if pd.isna(val):
                    return None
                try:
                    return cast_type(val)
                except (ValueError, TypeError):
                    return None

            result.append({
                "ticker": self.ticker,
                "quarter": quarter.strftime("%Y-%m-%d") if hasattr(quarter, 'strftime') else str(quarter),
                "revenue": safe_cast(rev, float),
                "net_income": safe_cast(ni, float),
                "outstanding_shares": safe_cast(o_s, int),
                "diluted_outstanding_shares": safe_cast(d_o_s, int)
            })

        return result

    def _get_balance_statement_json_list(self, balance_stmt_q: pd.DataFrame) -> list:
        df_safe = balance_stmt_q.reindex(["Total Debt"])
        result = []

        for quarter in df_safe.columns:
            t_debt = df_safe.loc["Total Debt", quarter]
            total_debt_val = float(t_debt) if pd.notna(t_debt) else None

            result.append({
                "ticker": self.ticker,
                "quarter": quarter.strftime("%Y-%m-%d") if hasattr(quarter, 'strftime') else str(quarter),
                "total_debt": total_debt_val
            })
        return result

    def _get_cashflow_statement_json_list(self, cashflow_stmt_q: pd.DataFrame) -> list:
        df_safe = cashflow_stmt_q.reindex(["Free Cash Flow"])
        result = []

        for quarter in df_safe.columns:
            fc_flow = df_safe.loc["Free Cash Flow", quarter]
            free_cf_val = float(fc_flow) if pd.notna(fc_flow) else None
            result.append({
                "ticker": self.ticker,
                "quarter": quarter.strftime("%Y-%m-%d") if hasattr(quarter, 'strftime') else str(quarter),
                "free_cashflow": free_cf_val
            })
        return result