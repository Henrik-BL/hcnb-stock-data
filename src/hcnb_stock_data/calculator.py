import numpy as np

class Calculator:

    @staticmethod
    def calculate_cagr(start_value: float, end_value: float, num_units: int) -> float | None:
        if num_units <= 0:
            raise ValueError("Number of units must be greater than zero.")

        # CAGR is undefined for non-positive starting values
        if start_value <= 0:
            return None

        ratio = end_value / start_value

        # Optional: also block negative ending values
        if ratio <= 0:
            return None

        cagr = (ratio ** (1 / num_units)) - 1
        return round(cagr * 100, 2)

    @staticmethod
    def calculate_change_percentage(first, second):
        if not first:
            return None
        result = (second / first) - 1
        result = result * 100
        return round(result, 2)

    @staticmethod
    def calculate_rsi(prices, period=14):
        prices = np.array(prices, dtype=float)
        if len(prices) <= period:
            return None
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])

        # Wilder smoothing over the remaining deltas
        for i in range(period, len(deltas)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period

        if avg_loss == 0:
            # No losses: RSI is 100, or neutral if the price did not move at all
            return 100.0 if avg_gain > 0 else 50.0

        rs = avg_gain / avg_loss
        return round(float(100 - (100 / (1 + rs))), 2)

    @staticmethod
    def calculate_average(values):
        return round(sum(values) / len(values), 2) if values else None
