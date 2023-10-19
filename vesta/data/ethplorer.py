import requests
import logging
import pandas as pd
from typing import Optional
from vesta.token import Token
from moralis import evm_api
import pandas as pd

class Ethplorer:
    """
    A class to interact with the Moralis API to fetch cryptocurrency data.
    """

    @staticmethod
    def get_eth_top_holders(token: Token) -> pd.DataFrame:
        """
        Fetches the current price of a specified token in USD.

        Parameters:
        token (Token): The token for which to fetch the price.

        Returns:
        float | None: The current price in USD or None if an error occurs.
        """
        try:
            response_API = requests.get(f'https://api.ethplorer.io/getTopTokenHolders/{token.eth_address}?apiKey=freekey&limit=1000')
            if response_API.status_code == 200:
                response_json = response_API.json()
                return pd.DataFrame(response_json['holders'])
            else:
                logging.warning(f'Failed to fetch price. HTTP Status Code: {response_API.status_code}')
                return None
        except Exception as e:
            logging.error(f'Error fetching price: {e}')
            return None