from hcnb_stock_data.models.stock_data import StockData


class DividendStockGrader:

    def __init__(self, stock_data: StockData):
        self.stock_data = stock_data
        self.score = 0.0
        self.max_score = 0.0
        self.result = []

    def evaluate(self):
        self._consecutive_dividend_increases()
        self._five_year_dividend_cagr()
        self._ten_year_dividend_cagr()
        self._payout_ratio()
        self._current_ratio()
        self._debt_to_equity()
        self._yearly_revenue_cagr()
        self._yearly_net_income_cagr()
        self._quarterly_revenue_cagr()
        self._quarterly_net_income_cagr()
        self._yearly_outstanding_shares_cagr()
        return self

    def get_score(self):
        return round(self.score / self.max_score if self.max_score else 0, 2)

    def get_grade(self):
        ratio = self.get_score()

        if ratio >= 0.85:
            return "A"
        elif ratio >= 0.70:
            return "B"
        elif ratio >= 0.50:
            return "C"
        else:
            return "D"

    # -------- metrics --------

    def _consecutive_dividend_increases(self):
        self.max_score += 1

        passed = self.stock_data.consecutive_dividend_increases >= 10
        if passed:
            self.score += 1

        self.result.append({
            "metric": "consecutive_dividend_increases",
            "value": self.stock_data.consecutive_dividend_increases,
            "passed": passed
        })

    def _five_year_dividend_cagr(self):
        self.max_score += 1

        passed = self.stock_data.five_year_dividend_cagr >= 5
        if passed:
            self.score += 1

        self.result.append({
            "metric": "five_year_dividend_cagr",
            "value": self.stock_data.five_year_dividend_cagr,
            "passed": passed
        })

    def _ten_year_dividend_cagr(self):
        self.max_score += 1

        passed = self.stock_data.ten_year_dividend_cagr >= 5
        if passed:
            self.score += 1

        self.result.append({
            "metric": "ten_year_dividend_cagr",
            "value": self.stock_data.ten_year_dividend_cagr,
            "passed": passed
        })

    def _payout_ratio(self):
        self.max_score += 1

        value = self.stock_data.payout_ratio

        # safer dividend range (avoids overpaying dividends)
        passed = value is not None and value <= 0.8

        if passed:
            self.score += 1

        self.result.append({
            "metric": "payout_ratio",
            "value": value,
            "passed": passed
        })

    def _current_ratio(self):
        self.max_score += 1

        cr = self.stock_data.current_ratio

        # handle null / None safely
        if cr is None:
            passed = False
            value = None
        else:
            if cr >= 1.5:
                self.score += 1
                passed = True
            elif cr >= 1.0:
                self.score += 0.5
                passed = True
            else:
                passed = False

            value = cr

        self.result.append({
            "metric": "current_ratio",
            "value": value,
            "passed": passed
        })

    def _debt_to_equity(self):
        self.max_score += 1

        debt_to_equity = self.stock_data.debt_to_equity

        if debt_to_equity is None:
            passed = False
            value = None
        else:
            value = debt_to_equity
            if debt_to_equity < 100:
                self.score += 1
                passed = True
            else:
                passed = False

        self.result.append({
            "metric": "current_ratio",
            "value": value,
            "passed": passed
        })

    def _yearly_revenue_cagr(self):
        self.max_score += 1

        value = self.stock_data.yearly_revenue_cagr
        passed = value is not None and value >= 5

        if passed:
            self.score += 1

        self.result.append({
            "metric": "yearly_revenue_cagr",
            "value": value,
            "passed": passed
        })

    def _yearly_net_income_cagr(self):
        self.max_score += 1

        value = self.stock_data.yearly_net_income_cagr
        passed = value is not None and value >= 5

        if passed:
            self.score += 1

        self.result.append({
            "metric": "yearly_net_income_cagr",
            "value": value,
            "passed": passed
        })

    def _quarterly_revenue_cagr(self):
        self.max_score += 1

        value = self.stock_data.quarterly_revenue_cagr
        passed = value is not None and value >= 2

        if passed:
            self.score += 1

        self.result.append({
            "metric": "quarterly_revenue_cagr",
            "value": value,
            "passed": passed
        })

    def _quarterly_net_income_cagr(self):
        self.max_score += 1

        value = self.stock_data.quarterly_net_income_cagr
        passed = value is not None and value >= 2

        if passed:
            self.score += 1

        self.result.append({
            "metric": "quarterly_net_income_cagr",
            "value": value,
            "passed": passed
        })

    def _yearly_outstanding_shares_cagr(self):
        self.max_score += 1

        value = self.stock_data.yearly_outstanding_shares_cagr

        # lower is better (share dilution)
        passed = value is not None and value <= 0

        if passed:
            self.score += 1

        self.result.append({
            "metric": "yearly_outstanding_shares_cagr",
            "value": value,
            "passed": passed
        })