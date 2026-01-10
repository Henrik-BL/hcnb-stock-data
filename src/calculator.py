import numpy as np

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

        return rsi_values[-1]