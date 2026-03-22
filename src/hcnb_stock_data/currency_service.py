import requests
from typing import Dict, Optional


class CurrencyService:

    def __init__(self, base_currency: str = "USD"):
        self.base_currency = base_currency.upper()
        self.api_url = f"https://open.er-api.com/v6/latest/{self.base_currency}"
        self.rates = None
        self.last_update = None

    def fetch_rates(self) -> Dict[str, float]:
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()

            if "rates" not in data:
                raise ValueError("Invalid API response: 'rates' key not found")

            self.rates = data["rates"]
            self.last_update = data.get("time_last_update_utc", None)

            return self.rates
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Failed to fetch exchange rates: {str(e)}")

    def get_rate(self, currency: str) -> Optional[float]:
        if self.rates is None:
            self.fetch_rates()

        return self.rates.get(currency.upper())

    def get_all_rates(self) -> Dict[str, float]:
        if self.rates is None:
            self.fetch_rates()

        return self.rates

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        if self.rates is None:
            self.fetch_rates()

        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency == self.base_currency:
            if to_currency not in self.rates:
                raise ValueError(f"Currency {to_currency} not found")
            return amount * self.rates[to_currency]

        if to_currency == self.base_currency:
            if from_currency not in self.rates:
                raise ValueError(f"Currency {from_currency} not found")
            return amount / self.rates[from_currency]

        if from_currency not in self.rates or to_currency not in self.rates:
            raise ValueError(f"Currency not found")

        amount_in_base = amount / self.rates[from_currency]
        return amount_in_base * self.rates[to_currency]

    def get_supported_currencies(self) -> list:
        if self.rates is None:
            self.fetch_rates()
        return list(self.rates.keys())
