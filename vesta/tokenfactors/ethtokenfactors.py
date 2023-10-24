from vesta.data.data import Data
from vesta.token.token import Token
from vesta.functions.functions import Functions
from typing import List
import pandas as pd
import numpy as np
import time

class TokenFactors:
    """
    A class to calculate token factors for Ethereum tokens.
    """

    def __init__(self, data: Data, token: Token):
        # Initialize with data and token objects, and retrieve token data and historical market data.
        self.functions = Functions()
        self.data = data
        self.token = token
        self.token_data = self.data.coingecko.get_token_data(token)
        self.token_historical_market_data = self.data.coingecko.get_historical_market_data(token)
        self.get_wallet_stats = self.data.moralis_client.get_eth_wallet_stats(token)
        self.oracle_data = self.data.pythpy.get_pyth_data(token)

    def calculate_mean_slippage(self, usdc_values: List[int] = [1000, 2000, 5000, 10000, 100000]) -> float:
        # Calculate the mean slippage for specified USDC values by fetching the slippage for each value,
        # summing them up and dividing by the number of values.

        # Introducing a sleep to alieviate the rate limit of the Jupiter API.
        slippages = []
        for value in usdc_values:
            slippages.append(self.data.jupiter.get_usdc_swap_price_slippage(self.token, value))
            time.sleep(2)
        mean_slippage = sum(slippages) / len(slippages)
        return self.functions.invrational_1(mean_slippage, 1, 1, 10)

    def calculate_market_cap(self) -> float:
        # Fetch and return the market cap of the token using an inverse rational transformation.
        market_cap = self.token_data['market_data']['market_cap']['usd']
        if market_cap == 0: return None
        return self.functions.invrational_2(market_cap, 1, 1, 10 ** -6.3)
    
    def calculate_market_cap_rank(self) -> float:
        # Fetch and return the market cap rank of the token using an inverse rational transformation.
        market_cap_rank = self.token_data['market_cap_rank']
        if market_cap_rank == None: return None
        return self.functions.invrational_1(market_cap_rank, 1, 1, 5000)

    def calculate_fully_diluted_valuation(self) -> float:
        # Fetch and return the fully diluted valuation of the token using an inverse rational transformation.
        fully_diluted_valuation = self.token_data['market_data']['fully_diluted_valuation']['usd']
        return self.functions.invrational_2(fully_diluted_valuation, 1, 1, 10 ** -8)
    
    def calculate_24h_volume(self) -> float:
        # Fetch and return the 24-hour trading volume of the token using an inverse rational transformation.
        _24h_volume = self.token_data['market_data']['total_volume']['usd']
        if _24h_volume == 0: return None
        return self.functions.genlogistic_1(_24h_volume, 1, 1, 50, 50000)
    
    def calculate_returns_volatility(self) -> float:
        # Calculate the volatility of the token by computing the standard deviation of the log returns.
        log_returns = np.log(self.token_historical_market_data['price']/self.token_historical_market_data['price'].shift(1)).dropna()
        volatility = log_returns.std()
        return self.functions.genlogistic_2(volatility, 1, 1, 50, 0.03)
    
    def calculate_token_tickers_length(self) -> float:
        # Total amount of tickers (more is safer)
        tickers_length = len(self.token_data['tickers'])
        return self.functions.invrational_2(tickers_length, 1, 1, 0.3)

    def calculate_alexa_rank(self) -> float:
        # Fetch and return the Alexa rank of the token's website using an inverse rational transformation.
        alexa_rank = self.token_data['public_interest_stats']['alexa_rank']
        if alexa_rank == None: return None
        return self.functions.invrational_1(alexa_rank, 1, 1, 1000000)

    def calculate_coingecko_rank(self) -> float:
        coingecko_rank = self.token_data['coingecko_rank']
        return self.functions.invrational_1(coingecko_rank, 1, 1, 1000)
    
    def calculate_age(self) -> float:
        # Fetch and return the CoinGecko rank of the token using an inverse rational transformation.
        (creation_timestamp, creation_block_number, creation_hash) = self.data.get_eth_contract_creation_timestamp_block_hash(self.token)
        creation_datetime = pd.to_datetime(creation_timestamp, unit='s')
        age = (pd.to_datetime('today') - creation_datetime).days
        return self.functions.genlogistic_1(age, 1, 1, 50, 150)
    
    def calculate_token_transactions(self) -> float:
        # Fetch and return the CoinGecko rank of the token using an inverse rational transformation.
        transactions = float(self.get_wallet_stats['transactions']['total'])
        return self.functions.genlogistic_1(transactions, 1, 1, 50, 3000)
    
    def calculate_top_holders_HHI(self) -> float:
        # The Herfindahl-Hirschman Index (HHI) as a measurement of the concentration. 
        holders = self.data.ethplorer.get_eth_top_holders(self.token)
        holders = holders.sort_values(by='balance')
        holders['share']  = holders['share']  / 100
        others = 1 - sum(holders['share']) # All other outside 100 holders (seen as one holder)
        holders['share_squared'] = holders['share'] ** 2
        HHI = holders['share_squared'].sum() + (others ** 2)
        return self.functions.genlogistic_2(HHI, 1, 1, 50, 0.05)
    
    def calculate_oracle_confidence(self) -> float:
        # Fetch and return the CoinGecko rank of the token using an inverse rational transformation.
        confidence = float((100 * self.oracle_data['confidence']) / self.oracle_data['price'])
        return self.functions.genlogistic_2(confidence, 1, 1, 50, 0.05)
