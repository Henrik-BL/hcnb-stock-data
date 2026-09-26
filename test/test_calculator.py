import pytest

from hcnb_stock_data.calculator import Calculator


def test_cagr_over_periods():
    # 100 -> 121 over two periods is 10% per period
    assert Calculator.calculate_cagr(100, 121, 2) == 10.0


def test_cagr_undefined_for_non_positive_values():
    assert Calculator.calculate_cagr(0, 100, 2) is None
    assert Calculator.calculate_cagr(-10, 100, 2) is None
    assert Calculator.calculate_cagr(100, -10, 2) is None


def test_cagr_rejects_zero_periods():
    with pytest.raises(ValueError):
        Calculator.calculate_cagr(100, 110, 0)


def test_change_percentage():
    assert Calculator.calculate_change_percentage(100, 110) == 10.0
    assert Calculator.calculate_change_percentage(0, 110) is None
    assert Calculator.calculate_change_percentage(None, 110) is None


def test_rsi_hand_computed_wilder_smoothing():
    # deltas 1, -1, 2 -> initial avg gain/loss 0.5/0.5, then 1.25/0.25 -> RS 5
    assert Calculator.calculate_rsi([1, 2, 1, 3], period=2) == 83.33


def test_rsi_only_gains_is_100():
    assert Calculator.calculate_rsi(list(range(1, 31))) == 100.0


def test_rsi_only_losses_is_0():
    assert Calculator.calculate_rsi(list(range(30, 0, -1))) == 0.0


def test_rsi_flat_price_is_neutral():
    assert Calculator.calculate_rsi([10.0] * 30) == 50.0


def test_rsi_needs_more_than_period_prices():
    assert Calculator.calculate_rsi([1.0] * 14) is None


def test_average():
    assert Calculator.calculate_average([1, 2, 3]) == 2.0
    assert Calculator.calculate_average([]) is None
