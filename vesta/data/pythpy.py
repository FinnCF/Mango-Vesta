import requests
import logging
import pandas as pd
from typing import Optional
from vesta.token import Token
from moralis import evm_api
from solana.rpc.api import Client as SolClient
import asyncio
from pythclient.pythaccounts import PythPriceAccount, PythPriceStatus
from pythclient.solana import SolanaClient, SolanaPublicKey, PYTHNET_HTTP_ENDPOINT, PYTHNET_WS_ENDPOINT

class PythPyClient:
    """
    A class to interact with the Pyth Contracts to fetch cryptocurrency data.
    """

    def __init__(self, sol_client: SolClient):
        self.sol_client = sol_client

    def get_pyth_data(self, token: Token) -> Optional[float]:
        return asyncio.run(self._get_data(token))

    async def _get_data(self, token: Token) -> Optional[float]:
        account_key = SolanaPublicKey(token.oracle_address)
        solana_client = SolanaClient(endpoint=PYTHNET_HTTP_ENDPOINT, ws_endpoint=PYTHNET_WS_ENDPOINT)
        price: PythPriceAccount = PythPriceAccount(account_key, solana_client)
        try:
            await price.update()
            price_status = price.aggregate_price_status
            if price_status == PythPriceStatus.TRADING:
                return {'price': price.aggregate_price, 'confidence': price.aggregate_price_confidence_interval}
            else:
                logging.warning(f"Price is not valid now. Status is {price_status}")
                return None 
        finally:
            await solana_client.close()  

