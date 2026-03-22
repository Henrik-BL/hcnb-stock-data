from hcnb_stock_data.models.stock_data_constructor import StockDataConstructor


class StockData:

    def __init__(self, stock_data_constructor: StockDataConstructor):
        self.ticker = stock_data_constructor.base_data.ticker
        self.pe = stock_data_constructor.base_data.pe
        self.forward_pe = stock_data_constructor.base_data.forward_pe
        self.ps = stock_data_constructor.base_data.ps
        self.pb = stock_data_constructor.base_data.pb
        self.peg = stock_data_constructor.base_data.peg
        self.currency = stock_data_constructor.base_data.currency
        self.price = stock_data_constructor.base_data.price
        self.market_cap = stock_data_constructor.base_data.market_cap
        self.revenue_growth = stock_data_constructor.calculated_data.revenue_growth
        self.earnings_growth = stock_data_constructor.calculated_data.earnings_growth
        self.current_ratio = stock_data_constructor.base_data.current_ratio
        self.debt_to_equity = stock_data_constructor.base_data.debt_to_equity
        self.dividend_yield = stock_data_constructor.base_data.dividend_yield
        self.sector = stock_data_constructor.base_data.sector
        self.industry = stock_data_constructor.base_data.industry
        self.beta = stock_data_constructor.base_data.beta

        # Quarterly reports
        self.quarterly_revenue_cagr = stock_data_constructor.quarterly_data.revenue_cagr
        self.quarterly_net_income_cagr = stock_data_constructor.quarterly_data.net_income_cagr
        self.quarterly_outstanding_shares_cagr = stock_data_constructor.quarterly_data.outstanding_shares_cagr
        self.quarterly_diluted_outstanding_shares_cagr = stock_data_constructor.quarterly_data.diluted_outstanding_shares_cagr
        self.quarterly_total_debt_cagr = stock_data_constructor.quarterly_data.total_debt_cagr
        self.quarterly_free_cashflow_cagr = stock_data_constructor.quarterly_data.free_cashflow_cagr

        # Last quarter
        self.last_quarter_pe = stock_data_constructor.calculated_data.last_quarter_pe
        self.last_quarter_free_cashflow_yield = stock_data_constructor.calculated_data.last_quarter_free_cashflow_yield
        self.last_quarter_date = stock_data_constructor.calculated_data.last_quarter_date
        self.last_quarter_revenue = stock_data_constructor.calculated_data.last_quarter_revenue
        self.last_quarter_net_income = stock_data_constructor.calculated_data.last_quarter_net_income
        self.last_quarter_free_cashflow = stock_data_constructor.calculated_data.last_quarter_free_cashflow
        self.last_quarter_margin = stock_data_constructor.calculated_data.last_quarter_margin

        # Yearly reports
        self.yearly_revenue_cagr = stock_data_constructor.yearly_data.revenue_cagr
        self.yearly_net_income_cagr = stock_data_constructor.yearly_data.net_income_cagr
        self.yearly_outstanding_shares_cagr = stock_data_constructor.yearly_data.outstanding_shares_cagr
        self.yearly_diluted_outstanding_shares_cagr = stock_data_constructor.yearly_data.diluted_outstanding_shares_cagr
        self.yearly_total_debt_cagr = stock_data_constructor.yearly_data.total_debt_cagr
        self.yearly_free_cashflow_cagr = stock_data_constructor.yearly_data.free_cashflow_cagr

        # Dividend
        self.five_year_dividend_cagr = stock_data_constructor.dividend_data.five_year_dividend_cagr
        self.ten_year_dividend_cagr = stock_data_constructor.dividend_data.ten_year_dividend_cagr
        self.payouts = stock_data_constructor.dividend_data.payouts
        self.consecutive_dividend_increases = stock_data_constructor.dividend_data.consecutive_dividend_increases

        # Price
        self.rsi_14 = stock_data_constructor.price_data.rsi_14
        self.sma_225 = stock_data_constructor.price_data.sma_225
        self.sma_255_diff = stock_data_constructor.price_data.sma_255_diff

    def __str__(self):
        return f"StockData: {self.ticker}"
