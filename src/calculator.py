class Calculator:

    @staticmethod
    def calculate_cagr(start_value: float, end_value: float, num_units: int) -> float:
        if start_value <= 0:
            raise ValueError("Start value must be greater than zero to calculate CAGR.")
        if num_units <= 0:
            raise ValueError("Number of units must be greater than zero.")
        cagr = ((end_value / start_value) ** (1 / num_units)) - 1
        return round(cagr * 100, 2)
