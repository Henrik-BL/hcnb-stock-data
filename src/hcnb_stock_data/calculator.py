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
        result = (second / first) - 1
        result = result * 100
        return round(result, 2)

    @staticmethod
    def calculate_rsi(prices, period=14):
        prices = np.array(prices)
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])

        rsi_values = []
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi_values.append(100 - (100 / (1 + rs)))

        # Calculate RSI for the rest
        for i in range(period, len(prices) - 1):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            rs = avg_gain / avg_loss if avg_loss != 0 else 0
            rsi = 100 - (100 / (1 + rs))
            rsi_values.append(rsi)

        return float(rsi_values[-1])

# -17375000.0 -> 6539000.0

# print(Calculator.calculate_cagr(-17375000.0, 6539000.0, 5))