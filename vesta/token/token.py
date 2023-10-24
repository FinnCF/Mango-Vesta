from dataclasses import dataclass, field, InitVar
from eth_typing import Address
from web3 import Web3
from typing import Optional
import re
import requests

class Token:
    def __init__(self, symbol: str, coingecko_id: str, sol_address: str, eth_address: Address, sol_decimals: int, eth_decimals: int, oracle_address: str) -> None:
        # Validation
        if not sol_address or not eth_address:
            raise ValueError("All fields must be non-empty.")

        if not Web3.is_address(eth_address):
            raise ValueError(f"{eth_address} is not a valid Ethereum address.")

        if len(sol_address) != 44 or not re.match("^[A-Za-z0-9]*$", sol_address):
            raise ValueError(f"{sol_address} is not a valid Solana address.")

        # Assigning values to attributes
        self.symbol = symbol
        self.coingecko_id = coingecko_id
        self.sol_address = sol_address
        self.eth_address = eth_address
        self.sol_decimals = sol_decimals
        self.eth_decimals = eth_decimals
        self.oracle_address = oracle_address

