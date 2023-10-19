

class Utils:
    """
    Contains utility methods.
    """

    def __init__(self) -> None:

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
            creation_hash = self.get_earliest_transaction_hash(contract_address=contract_address)
        except Exception as e:
            logger.error(f"Error while getting contract creation transaction hash: {e}")
            raise ValueError

        creation_block_number = None
        tx_receipt = None
        try:
            # Get the transaction receipt to retrieve the block number
            tx_receipt = self.web3.eth.get_transaction_receipt(creation_hash)
            creation_block_number = tx_receipt['blockNumber']
        except Exception as e:
            logger.error(f"Error while getting block number: {e}")
            raise ValueError

        creation_timestamp = None
        try:
            # Get the block timestamp using the block number
            creation_timestamp = self.web3.eth.get_block(creation_block_number)['timestamp']
        except Exception as e:
            logger.error(f"Error while getting timestamp: {e}")
            raise ValueError

        return creation_timestamp, creation_block_number, creation_hash