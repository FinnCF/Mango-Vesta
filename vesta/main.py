from vesta.functions.functions import Functions
from vesta.data.data import Data
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
from solana.rpc.api import Client as SolClient
from typing import Union, Type
from vesta.token.token import Token
from vesta.tokenfactors.ethtokenfactors import EthTokenFactors
from tqdm import tqdm
from etherscan import Etherscan
from vesta.data.moralis import MoralisClient

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
                 ---- 🥭 Mango Vesta Multifactor Risk Parameter Optimiser 🥭 ----
          """
        print(ascii_art)

    def rate(self, token: Token) -> float:
        """
        Given a 'Token' data type, rates the token based on the Vesta model.
        The rating is computed as a weighted sum of normalized factors.
        """
        # Define factors and their weights (gammas)
        factors = {
            'calculate_mean_slippage': 0.0625,
            'calculate_market_cap_rank':0.0625,
            'calculate_alexa_rank': 0.0625,
            'calculate_market_cap': 0.0625,
            'calculate_fully_diluted_valuation': 0.0625,
            'calculate_coingecko_rank': 0.0625,
            'calculate_24h_volume': 0.0625,
            'calculate_returns_volatility': 0.0625,
            'calculate_abs_normalised_returns_volatility': 0.0625,
            'calculate_volume_volatility':0.0625,
            'calculate_age': 0.0625,
            'calculate_token_transactions': 0.0625,
            'calculate_token_transfers': 0.0625,
            'calculate_top_holders_HHI': 0.0625,
            'calculate_token_tickers_length': 0.0625,
            'calculate_oracle_confidence': 0.0625
        }
        
        assert round(sum(factors.values())) == 1, 'Total Gammas MUST equal one in Vesta Model'        

        with tqdm(total=len(factors) + 1, desc="Calculating Factors") as pbar:
            
            pbar.set_description(f"{token.symbol}: Initializing TokenFactors")
            token_factors = EthTokenFactors(self.data, token)
            pbar.update(1)
            
            total_value = 0
            for method_name, gamma in factors.items():
                pbar.set_description(f"{token.symbol}: Calculating {method_name}...")
                method = getattr(token_factors, method_name)
                factor_value = method()
                total_value += gamma * factor_value
                pbar.set_description(f"{token.symbol}: Calculated {method_name}: {factor_value}")
                pbar.update(1)

            pbar.set_description(f"Rated {token.symbol}: {total_value}, {self.rate_total_value(total_value)}")

        return total_value
    
    def rate_total_value(self, total_value: float) -> str:
        match total_value:
            case _ if 0.0 <= total_value < 0.1:
                return 'D'
            case _ if 0.1 <= total_value < 0.2:
                return 'CCC'
            case _ if 0.2 <= total_value < 0.3:
                return 'CC'
            case _ if 0.3 <= total_value < 0.4:
                return 'C'
            case _ if 0.4 <= total_value <= 0.5:
                return 'BBB'
            case _ if 0.5 <= total_value <= 0.6:
                return 'BB'
            case _ if 0.6 <= total_value <= 0.7:
                return 'B'
            case _ if 0.7 <= total_value <= 0.8:
                return 'AAA'
            case _ if 0.8 <= total_value <= 0.9:
                return 'AA'
            case _ if 0.9 <= total_value <= 1:
                return 'A'
            case _:
                raise ValueError(f'Invalid rating value: {total_value}')
