import requests
import logging
import pandas as pd
from typing import Optional
from vesta.token import Token
from moralis import evm_api

class MoralisClient:
    """
    A class to interact with the Moralis API to fetch cryptocurrency data.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

        
    def get_eth_wallet_stats(self, token: Token) -> Optional[float]:
        """
        Fetches the current price of a specified token in USD.

        Parameters:
        token (Token): The token for which to fetch the price.

        Returns:
        float | None: The current price in USD or None if an error occurs.
        """
        try:
            result = evm_api.wallets.get_wallet_stats(
                api_key=self.api_key,
                params={
                    "address": f"{token.eth_address}",
                    "chain": "eth",
                },
            )
            return result
        except Exception as e:
            logging.error(f'Error fetching Moralis transactions: {e}')
            return None