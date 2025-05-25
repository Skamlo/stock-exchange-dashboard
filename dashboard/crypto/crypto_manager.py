from binance.client import Client
from typing import List, Union
import requests
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("COINMARKETCAP_API_KEY")

class CryptoManager:
    def __init__(self):
        self._client = Client()
        self.selected_coins = ["BTC", "ETH", "XRP", "SOL", "DOGE"]
        self.coinmarketcap_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        self.coinmarketcap_headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": API_KEY,
        }


    def get_selected_coins(self) -> List[str]:
        """
        Method is for selecting list of coins.

        Returns:
            List[str]: list of coins names
        """
        return self.selected_coins

    def get_coins(self) -> List[str]:
        """
        Method is for selecting list of coins.

        Returns:
            List[str]: list of coins names
        """
        exchange_info = self._client.get_exchange_info()
        return sorted({s['baseAsset'] for s in exchange_info['symbols']})

    def get_coin_prices(self, coin: str, start_date: str, end_date: str, interval: str = "1d") -> List[dict]:
        """
        Methods for seelcting a coin prices from a time range.

        Args:
            coin (str): coin name
            start_date (str): left side of time range (in year-month-day format e.g. 2005-04-02)
            end_date (str): right side of time range (in year-month-day format e.g. 2005-04-02)
            interval (str): space between each data point (e.g. "1m", "1h", "1d", "1w", "1M")

        Returns:
            List[dict]: list of data samples in format:
            ```json
            {
                'timestamp': ...,
                'open': ...,
                'high': ...,
                'low': ...,
                'close': ...,
                'volume': ...
            }
            ```
        """
        symbol = coin.upper() + "USDT"
        try:
            klines = self._client.get_historical_klines(
                symbol,
                interval,
                start_str=start_date,
                end_str=end_date
            )

            return [
                {
                    "timestamp": int(k[0]),
                    "open": float(k[1]),
                    "high": float(k[2]),
                    "low": float(k[3]),
                    "close": float(k[4]),
                    "volume": float(k[5]),
                }
                for k in klines
            ]
        except Exception as e:
            print(f"Error fetching historical prices: {e}")
            return []

    def get_coin_info(self, coin: str) -> dict:
        """
        Method retunds basic information about coin.

        Args:
            coin (str): coin name
        
        Returns:
            dict: dictionary with coin parameters (i.e. "symbol", "status", "baseAsset", "quoteAsset", "orderTypes", "isSpotTradingAllowed", "isMarginTradingAllowed", "filters")
        """
        coin = coin.upper()
        symbol = coin + "USDT"
        exchange_info = self._client.get_exchange_info()
        for s in exchange_info['symbols']:
            if s['symbol'] == symbol:
                return {
                    key: value for key, value in s.items()
                    if key in [
                        "symbol", "status", "baseAsset", "quoteAsset",
                        "orderTypes", "isSpotTradingAllowed",
                        "isMarginTradingAllowed", "filters"
                    ]
                }
        return {}

    def get_coin_market_cap(self, coin: Union[str, List[str]]) -> Union[float, List[float]]:
        if isinstance(coin, str):
            coin = [coin]

        params = {
            "symbol": ",".join(coin),
        }

        response = requests.get(self.coinmarketcap_url, headers=self.coinmarketcap_headers, params=params)
        data = response.json()

        if response.status_code != 200 or "data" not in data:
            raise Exception(f"Failed to fetch data: {data.get('status', {}).get('error_message', 'Unknown error')}")

        market_caps = [data["data"][symbol]["quote"]["USD"]["market_cap"] for symbol in coin]

        return market_caps[0] if len(market_caps) == 1 else market_caps

    def get_fear_and_greed_index(self, date: str = None) -> float:
        """
        Gets the Fear & Greed Index from alternative.me.
        Optionally filters by a given date (format: 'YYYY-MM-DD').

        Args:
            date (str, optional): Date to filter for. Defaults to None.

        Returns:
            float: Fear & Greed Index value or -1.0 on failure.
        """
        url = "https://api.alternative.me/fng/?limit=100"  # max 100 entries
        response = requests.get(url)

        if not response.ok:
            return -1.0

        data = response.json().get('data', [])

        if not date:
            return float(data[0]['value']) if data else -1.0

        for entry in data:
            entry_date = datetime.utcfromtimestamp(int(entry['timestamp'])).strftime('%Y-%m-%d')
            if entry_date == date:
                return float(entry['value'])

        return -1.0

    def get_coin_trading_volume(self, coin: str) -> float:
        """
        Returns the 24h trading volume in USD for the given coin (via USDT pair).

        Returns:
            float: 24h trading volume in USD
        """
        symbol = coin.upper() + "USDT"
        try:
            ticker = self._client.get_ticker(symbol=symbol)
            return float(ticker["quoteVolume"])  # volume in USDT = USD
        except Exception as e:
            print(f"Error fetching volume for {symbol}: {e}")
            return 0.0
        
    def get_top_n_coin_volumes(self, n: int=10) -> List[dict]:
        """
        Returns 24h trading volumes in USD for the top N coins (by USDT volume).

        Args:
            n (int): number of coins

        Return:
            List[dict]: list of dictionaries in format:
            ```json
            {
                "symbol": "BTC",
                "volume": 2137
            }
            ```
        """
        try:
            tickers = self._client.get_ticker()
            usdt_tickers = [
                {"symbol": t["symbol"], "volume": float(t["quoteVolume"])}
                for t in tickers
                if t["symbol"].endswith("USDT") and float(t["quoteVolume"]) > 0
            ]
            # Sort by volume descending
            sorted_volumes = sorted(usdt_tickers, key=lambda x: x["volume"], reverse=True)
            return sorted_volumes[:n]
        except Exception as e:
            print(f"Error fetching top volumes: {e}")
            return []


    def get_dominance(self, coin) -> float:
        """
        Estimates Crypto coin dominance based on USDT volume (Binance approximation).

        Returns:
            float: coin dominance in %
        """
        tickers = self._client.get_ticker()
        coin_volume = 0
        total_volume = 0
        for t in tickers:
            if t["symbol"].endswith("USDT"):
                vol = float(t["quoteVolume"])
                total_volume += vol
                if t["symbol"] == coin + "USDT":
                    coin_volume = vol
        return round((coin_volume / total_volume) * 100, 2) if total_volume > 0 else 0.0

    def get_total_crypto_market_cap(self) -> float:
        """
        Returns:
            float: total market cap of crypto
        """
        url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(url)
        data = response.json()
        total_market_cap = data['data']['total_market_cap']['usd']
        return total_market_cap
    
    def get_dataframe(self) -> pd.DataFrame:
        coins = self.get_selected_coins()
        data = []

        try:
            market_caps = self.get_coin_market_cap(coins)
            if isinstance(market_caps, float):
                market_caps = [market_caps]
        except Exception as e:
            print(f"Error fetching market caps: {e}")
            market_caps = [None] * len(coins)

        for idx, coin in enumerate(coins):
            symbol = coin.upper() + "USDT"
            price = None
            volume = None

            try:
                ticker = self._client.get_ticker(symbol=symbol)
                price = float(ticker["lastPrice"])
                volume = float(ticker["quoteVolume"])
            except Exception as e:
                print(f"Error fetching ticker for {symbol}: {e}")

            market_cap = market_caps[idx] if idx < len(market_caps) else None

            data.append({
                "Coin": coin,
                "Price": price,
                "Volume": volume,
                "MarketCap": market_cap,
            })

        df = pd.DataFrame(data)
        return df
