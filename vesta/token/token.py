from dataclasses import dataclass, field, InitVar
from eth_typing import Address
from web3 import Web3
from typing import Optional
import re
import requests

class Token:
    def __init__(self, 
                 type: str,
                 symbol: str, 
                 coingecko_id: str, 
                 sol_address: str, 
                 eth_address: Address, 
                 sol_decimals: int, 
                 eth_decimals: int, 
                 oracle_address: str) -> None:


        if(type == 'eth'):

            if not eth_address:
                raise ValueError("Ethereum Address field must be non-empty.")

            if not Web3.is_address(eth_address):
                raise ValueError(f"{eth_address} is not a valid Ethereum address.")

        self.type = type
        self.symbol = symbol
        self.coingecko_id = coingecko_id
        self.sol_address = sol_address
        self.eth_address = eth_address
        self.sol_decimals = sol_decimals
        self.eth_decimals = eth_decimals
        self.oracle_address = oracle_address

