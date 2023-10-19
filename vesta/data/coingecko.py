import requests
import logging
import pandas as pd
from typing import Optional
from vesta.token import Token

class CoinGecko:
    """
    A class to interact with the CoinGecko API to fetch cryptocurrency data.
    """

    def get_price(self, token: Token) -> Optional[float]:
        """
        Fetches the current price of a specified token in USD.

        Parameters:
        token (Token): The token for which to fetch the price.

        Returns:
        float | None: The current price in USD or None if an error occurs.
        """
        try:
            response_API = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={token.symbol.lower()}&vs_currencies=usd')
            if response_API.status_code == 200:
                response_json = response_API.json()
                return response_json.get(token.symbol.lower(), {}).get('usd', 0.0)
            else:
                logging.warning(f'Failed to fetch price. HTTP Status Code: {response_API.status_code}')
                return None
        except Exception as e:
            logging.error(f'Error fetching price: {e}')
            return None

    def get_token_data(self, token: Token) -> Optional[dict]:
        """
        Fetches data for a specified token.

        Parameters:
        token (Token): The token for which to fetch data.

        Returns:
        dict | None: A dictionary containing token data or None if an error occurs.
        """
        try:
            response_API = requests.get(f'https://api.coingecko.com/api/v3/coins/{token.symbol.lower()}')
            if response_API.status_code == 200:
                response_json = response_API.json()
                return response_json
            else:
                logging.warning(f'Failed to fetch token data. HTTP Status Code: {response_API.status_code}')
                return None
        except Exception as e:
            logging.error(f'Error fetching token data: {e}')
            return None

    def get_historical_market_data(self, token: Token, days: int = 30, base_currency: str = 'usd') -> pd.DataFrame:
        """
        Fetches historical market data for a specified token. Roughly hourly. 

        Parameters:
        token (Token): The token for which to fetch historical data.
        days (int, optional): The number of past days to fetch data for. Defaults to 30.
        base_currency (str, optional): The base currency against which to fetch historical data. Defaults to 'usd'.

        Returns:
        pd.DataFrame | None: A DataFrame containing historical market data or None if an error occurs.
        """
        try:
            response_API = requests.get(f'https://api.coingecko.com/api/v3/coins/{token.symbol.lower()}/market_chart?vs_currency={base_currency}&days={days}')
            if response_API.status_code == 200:
                response_json = response_API.json()
                df_prices = pd.DataFrame(response_json['prices'], columns=['timestamp', 'price'])
                df_volume = pd.DataFrame(response_json['total_volumes'], columns=['timestamp', 'volume'])
                df = pd.merge(df_prices, df_volume, on='timestamp')
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.set_index('timestamp', inplace=True)
                return df
            else:
                logging.warning(f'Failed to fetch historical market data. HTTP Status Code: {response_API.status_code}')
                return None
        except Exception as e:
            logging.error(f'Error fetching historical market data: {e}')
            return None
