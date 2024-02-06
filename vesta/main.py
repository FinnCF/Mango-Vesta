from vesta.functions.functions import Functions
from vesta.data.data import Data
from vesta.pricing.processes import Processes
from vesta.pricing.optimisers import Optimisers
from vesta.pricing.analytical import Analytical
from vesta.pricing.risk import Risk
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
from solana.rpc.api import Client as SolClient
from typing import Union, Type
from vesta.token.token import Token
from vesta.tokenfactors.tokenfactors import TokenFactors
from tqdm import tqdm
from etherscan import Etherscan
from vesta.data.moralis import MoralisClient
from .rankings import risk_ranking_parameters

class Vesta:
    """
    Main client class that provides access to all Vesta functionality.
    """

    def __init__(self, 
                 web3_provider: Union[str, HTTPProvider, IPCProvider, WebsocketProvider], 
                 etherscan_api_key_token: str,
                 moralis_api_key: str
                 ) -> None:

        self.etherscan = Etherscan(etherscan_api_key_token)  
        self.web3_client = Web3(web3_provider)
        self.sol_client = SolClient("https://api.devnet.solana.com")
        self.moralis_client = MoralisClient(moralis_api_key)
        self.processes = Processes()
        self.optimisers = Optimisers()
        self.analytical = Analytical()
        self.risk = Risk()

        # New instances of the 'Functions' and 'Data' classes used in Vesta. 
        self.data = Data(self.etherscan, self.web3_client, self.sol_client, self.moralis_client)

        # Little ASCII banner. 
        self.print_ascii()

    def print_ascii(self) -> None:
        ascii_art = r"""
            .-----------------------------------------------------------------------.
            |                                                                       |
            |                                                           _           |
            |   /\/\    __ _  _ __    __ _   ___    /\   /\   ___  ___ | |_   __ _  |
            |  /    \  / _` || '_ \  / _` | / _ \   \ \ / /  / _ \/ __|| __| / _` | |
            | / /\/\ \| (_| || | | || (_| || (_) |   \ V /  |  __/\__ \| |_ | (_| | |
            | \/    \/ \__,_||_| |_| \__, | \___/     \_/    \___||___/ \__| \__,_| |
            |                        |___/                                          |
            |                                                                       |
            '-----------------------------------------------------------------------'     
                 ---- 🥭 Mango Vesta Risk Parameter Optimiser 🥭 ----
          """
        print(ascii_art)

    def rate(self, token: Token) -> list:
        """
        Given a 'Token' data type, rates the token based on the Vesta model.
        The rating is computed as a weighted sum of normalized factors.
        """
        # Define factors and their weights (gammas)
        factors = {
            'calculate_mean_slippage': 0.2, 
            'calculate_market_cap_rank': 0.08,  
            'calculate_alexa_rank': 0.05,  
            'calculate_market_cap': 0.05,  
            'calculate_fully_diluted_valuation': 0.05,  
            'calculate_coingecko_rank': 0.03, 
            'calculate_24h_volume': 0.05,  
            'calculate_returns_volatility': 0.2, 
            'calculate_age': 0.08,  
            'calculate_token_transactions': 0.1,  
            'calculate_top_holders_HHI': 0.05,  
            'calculate_token_tickers_length': 0.03,  
            'calculate_oracle_confidence': 0.05 
        }
        
        assert round(sum(factors.values())) == 1, 'Total Gammas MUST equal one in Vesta Model'        

        with tqdm(total=len(factors) + 1, desc="Calculating Factors") as pbar:

            pbar.set_description(f"{token.symbol}: Calculating Total Valid Weight")

            # Initialize a variable to keep track of the total valid weight
            total_valid_weight = 0
            method_results = {}
            token_factors = TokenFactors(self.data, token)
            for method_name, gamma in factors.items():
                pbar.set_description(f"{token.symbol}: Calculating {method_name}...")
                pbar.update(1)
                method = getattr(token_factors, method_name, None)
                method_result = method() if method is not None else None
                method_results[method_name] = method_result
                if method_result is not None:
                    total_valid_weight += gamma
                    pbar.set_description(f"{token.symbol}: Calculated {method_name}: {method_result}")
            assert total_valid_weight > 0, 'No valid factors, cannot calculate rating'
            pbar.set_description(f"{token.symbol}: Valid Weight: {total_valid_weight}")
            pbar.update(1)
            
            total_value = 0
            for method_name, gamma in factors.items():
                factor_value = method_results[method_name]
                if factor_value is not None: 
                    total_value += (gamma / total_valid_weight) * factor_value
            ranking = self.rate_total_value(total_value)
            pbar.set_description(f'{token.symbol} Ranked with {total_value}, {ranking} with Vesta Risk Paramers: ', risk_ranking_parameters[ranking])
        return [token.symbol, method_results, ranking, total_value]
    
    def rate_total_value(self, total_value: float) -> str:
        match total_value:
            case _ if 0.9 <= total_value <= 1:
                return 'AAA'
            case _ if 0.8 <= total_value < 0.9:
                return 'AA'
            case _ if 0.7 <= total_value < 0.8:
                return 'A'
            case _ if 0.6 <= total_value < 0.7:
                return 'B'
            case _ if 0.5 <= total_value < 0.6:
                return 'BB'
            case _ if 0.4 <= total_value < 0.5:
                return 'BBB'
            case _ if 0.3 <= total_value < 0.4:
                return 'C'
            case _ if 0.2 <= total_value < 0.3:
                return 'CC'
            case _ if 0.1 <= total_value < 0.2:
                return 'CCC'
            case _ if 0.0 <= total_value < 0.1:
                return 'D'
            case _:
                raise ValueError(f'Invalid rating value: {total_value}')
