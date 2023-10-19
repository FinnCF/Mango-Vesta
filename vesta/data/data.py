from solana.rpc.api import Client as SolClient
from etherscan import Etherscan
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
from typing import Union, Type, List, Dict
from .jupiter import Jupiter
import requests
from .coingecko import CoinGecko
from ..token.token import Token
from .moralis import MoralisClient
from .ethplorer import Ethplorer
from .pythpy import PythPyClient

class Data:
    """
    Given a 'Token' data type, provides functionality to derive all available information from ethereum and solana - including:
    - price and volume history
    - days traded
    - days since last transaction
    - holders
    - transactions
    """

    def __init__(
        self,
        etherscan_client: Etherscan,
        web3_client: Web3,
        sol_client: SolClient,
        moralis_client: MoralisClient,
    ) -> None:
        self.etherscan_client = etherscan_client
        self.web3_client = web3_client
        self.sol_client = sol_client
        self.moralis_client = moralis_client 

        """ New instances of the 'Jupiter' class used in Vesta's Data module. """
        self.coingecko = CoinGecko()
        self.ethplorer = Ethplorer()
        self.pythpy = PythPyClient(self.sol_client)
        self.jupiter = Jupiter(self.coingecko)

    def get_eth_earliest_transaction_hash(self, token: Token) -> str:
        """
        Retrieves the transaction hash of a contract creation, if available.
        If a contract creation transaction cannot be found, returns the earliest transaction involving the contract.
        After this is used, you can use Infura to get the block data (number etc).

        Args:
            contract_address (str): The address of the contract.

        Returns:
            The transaction hash as a string.
        """
        try:
            # Retrieve the first transaction by address in ascending order
            tx_list = self.etherscan_client.get_normal_txs_by_address_paginated(
                address=token.eth_address,
                page=1,
                offset=1,
                startblock=0,
                endblock=99999999,
                sort="asc",
            )

            # Check if the list is empty
            if len(tx_list) == 0:
                print("No transaction found for this address.")
                return None

            # Retrieve the first transaction
            tx = tx_list[0]

            # Check if this is a contract creation transaction
            if tx["to"] == "":
                return tx["hash"]
            else:
                return tx["hash"]

        except Exception as e:
            print(f"Failed to get earliest transaction hash: {e}")
            raise e

    def get_eth_contract_creation_timestamp_block_hash(self, token: Token):
        """
        Retrieves the contract creation timestamp, block number, and transaction hash.

        Args:
            contract_address (str): The address of the contract.

        Returns:
            A tuple containing the contract creation timestamp (int),
            block number (int), and transaction hash (str).
        """
        creation_hash = None
        try:
            # Get the earliest transaction hash for contract creation
            creation_hash = self.get_eth_earliest_transaction_hash(token=token)
        except Exception as e:
            print(f"Error while getting contract creation transaction hash: {e}")
            raise ValueError

        creation_block_number = None
        tx_receipt = None
        try:
            # Get the transaction receipt to retrieve the block number
            tx_receipt = self.web3_client.eth.get_transaction_receipt(creation_hash)
            creation_block_number = tx_receipt["blockNumber"]
        except Exception as e:
            print(f"Error while getting block number: {e}")
            raise ValueError

        creation_timestamp = None
        try:
            # Get the block timestamp using the block number
            creation_timestamp = self.web3_client.eth.get_block(creation_block_number)["timestamp"]
        except Exception as e:
            print(f"Error while getting timestamp: {e}")
            raise ValueError

        return creation_timestamp, creation_block_number, creation_hash

