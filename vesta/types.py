from dataclasses import dataclass, field, InitVar
from eth_typing import Address
from web3 import Web3
from typing import Optional
import re

@dataclass
class TheGraphUniswapV3Pool:
    address: str
    liquidity: str
    created_at_timestamp: str
    created_at_block_number: str
    total_value_locked_token1: str
    sqrt_price: str
    tick: Optional[int]
    token0_address: str
    token0_symbol: str
    token0_totalSupply: int
    token1_address: str
    token1_symbol: str
    token1_totalSupply: int
    fee_tier: int

    def __repr__(self):
        return (f'TheGraphUniswapV3Pool(id={self.address}, '
                f'liquidity={self.liquidity}, '
                f'created_at_timestamp={self.created_at_timestamp}, '
                f'created_at_block_number={self.created_at_block_number}, '
                f'total_value_locked_token1={self.total_value_locked_token1}, '
                f'sqrt_price={self.sqrt_price}, '
                f'tick={self.tick}, '
                f'token0_address={self.token0_address}, '
                f'token0_symbol={self.token0_symbol}, '
                f'token0_totalSupply={self.token0_totalSupply}, '
                f'token1_address={self.token1_address}, '
                f'token1_symbol={self.token1_symbol}, '
                f'token1_totalSupply={self.token1_totalSupply}, '
                f'fee_tier={self.fee_tier})')