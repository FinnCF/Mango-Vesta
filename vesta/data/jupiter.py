from solana.rpc.api import Client as SolClient
from aioetherscan import Client as EtherscanClient
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
from typing import Optional, Dict, Any
import requests
from vesta.token import Token
from .coingecko import CoinGecko

class Jupiter:
    def __init__(self, coingecko: CoinGecko) -> None:
        """
        Initializes a new instance of the Jupiter class.

        Parameters:
        coingecko (CoinGecko): An instance of the CoinGecko class used to retrieve token prices.

        """
        self.coingecko = coingecko
        
    def get_usdc_swap_price_slippage(self, token: Token, usdc_quantity: int) -> Optional[Dict[str, Any]]:
        """
        Calculates the price impact of selling usdc_quantity worth of the token for USDC.

        Parameters:
        token (Token): The token to be traded.
        usdc_quantity (int): The amount of USDC that will be traded into.

        Returns:
        Optional[Dict[str, Any]]: The response from the quote API, or None if an error occurs.
        """
        # Retrieve the current price of the token in terms of USDC.
        price = self.coingecko.get_price(token)
        if not price:
            raise ValueError(f'Could not retrieve price for {token.symbol} in liquidity swapping calculations.')
        
        # Calculate the amount of tokens needed to get the desired USDC value,
        # and adjust for the token's decimal representation in Solana.
        starting_in = usdc_quantity / price
        starting_in_adj = int(starting_in * 10**token.sol_decimals)
        
        # Build the URL for the quote API request.
        url = (
            f'https://quote-api.jup.ag/v6/quote?'
            f'inputMint={token.sol_address}&'
            f'swapMode=ExactIn&'
            f'outputMint=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v&'
            f'amount={starting_in_adj}&'
            f'slippageBps=30&'
            f'onlyDirectRoutes=false&'
            f'asLegacyTransaction=false&'
            f'experimentalDexes=Jupiter%20LO'
        )
        
        try:
            response_API = requests.get(url)
            response_json = response_API.json()

            if 'error' in response_json and response_json['error'] == 'The route plan does not consume all the input amount, please lower your input amount':
                # If not enough liquidity to even route towards the token, return 100 price impact. To indicate it would almost entirely remove the market. 
                return 100
            
            response_API.raise_for_status()
            return float(response_API.json()['priceImpactPct']) * 100
        except requests.RequestException as e:
            # Log the exception (consider using a logging library).
            print(f'An error occurred: {e}')
            return None
