import requests

class FearGreedIndex:


    def __init__(self):
        self.url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://edition.cnn.com/markets/fear-and-greed",
            "Origin": "https://edition.cnn.com",
            "Connection": "keep-alive",
        }

    def get_value(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return round(data["fear_and_greed"]["score"], 2)
        else:
            raise Exception("Request failed:", response.status_code)
