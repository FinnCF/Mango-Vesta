from dataclasses import dataclass, field, InitVar
from eth_typing import Address
from web3 import Web3
from typing import Optional
import re
import requests

class Token:
    def __init__(self, symbol: str, sol_address: str, eth_address: Address, sol_decimals: int, eth_decimals: int,
                 sol_created_at_block: int, eth_created_at_block: int, origin: str, bridging_entity: str, oracle_address: str) -> None:
        # Validation
        if not sol_address or not eth_address or not origin or not bridging_entity:
            raise ValueError("All fields must be non-empty.")

        if not Web3.is_address(eth_address):
            raise ValueError(f"{eth_address} is not a valid Ethereum address.")

        if len(sol_address) != 44 or not re.match("^[A-Za-z0-9]*$", sol_address):
            raise ValueError(f"{sol_address} is not a valid Solana address.")

        # Assigning values to attributes
        self.symbol = symbol
        self.sol_address = sol_address
        self.eth_address = eth_address
        self.sol_decimals = sol_decimals
        self.eth_decimals = eth_decimals
        self.sol_created_at_block = sol_created_at_block
        self.eth_created_at_block = eth_created_at_block
        self.origin = origin
        self.bridging_entity = bridging_entity
        self.oracle_address = oracle_address
