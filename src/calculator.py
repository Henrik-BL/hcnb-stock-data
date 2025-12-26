class Calculator:

    @staticmethod
    def calculate_cagr(start_value: float, end_value: float, num_units: int) -> float:
        if num_units <= 0:
            raise ValueError("Number of units must be greater than zero.")

        if start_value == 0:
            return 0.0

        ratio = end_value / start_value

        if ratio < 0:
            sign = 1 if end_value > start_value else -1
            cagr = (abs(ratio) ** (1 / num_units) - 1) * sign
        else:
            cagr = (ratio ** (1 / num_units)) - 1

        return round(cagr * 100, 2)
