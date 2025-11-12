"""
Blockchain service module for interacting with the BatchTracker smart contract.
Handles Web3 connections, contract interactions, and blockchain data retrieval.
"""

from web3 import Web3
import json
import os
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class BlockchainService:
    """Service for interacting with the BatchTracker smart contract on the blockchain."""

    def __init__(self, provider_url: str = "http://localhost:8545", contract_address: Optional[str] = None):
        """
        Initialize the blockchain service.

        :param provider_url: The URL of the blockchain provider (default: local Ganache)
        :param contract_address: The address of the deployed BatchTracker contract
        """
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.provider_url = provider_url
        self.contract_address = contract_address
        self.contract = None
        self.contract_abi = None

        # Attempt to connect and load the contract
        try:
            if not self.w3.is_connected():
                logger.warning(f"Failed to connect to blockchain provider: {provider_url}")
            else:
                logger.info(f"Successfully connected to blockchain at {provider_url}")
                self._load_contract()
        except Exception as e:
            logger.error(f"Error initializing blockchain service: {str(e)}")

    def _load_contract(self):
        """Load the BatchTracker contract ABI and initialize the contract instance."""
        try:
            # Try to load the contract ABI from a JSON file
            abi_path = os.path.join(os.path.dirname(__file__), "..", "..", "contracts", "BatchTracker.json")
            
            # Fallback to a basic ABI definition if file doesn't exist
            if os.path.exists(abi_path):
                with open(abi_path, 'r') as f:
                    contract_data = json.load(f)
                    self.contract_abi = contract_data.get('abi', contract_data)
            else:
                # Minimal ABI for the functions we need
                self.contract_abi = self._get_default_abi()

            if self.contract_address and self.contract_abi:
                self.contract = self.w3.eth.contract(
                    address=Web3.to_checksum_address(self.contract_address),
                    abi=self.contract_abi
                )
                logger.info(f"Contract loaded at address: {self.contract_address}")
        except Exception as e:
            logger.error(f"Error loading contract: {str(e)}")

    @staticmethod
    def _get_default_abi() -> List[Dict]:
        """
        Get the default ABI for the BatchTracker contract.
        
        :return: List of ABI definitions for BatchTracker functions
        """
        return [
            {
                "inputs": [
                    {"internalType": "string", "name": "_name", "type": "string"},
                    {"internalType": "string", "name": "_origin", "type": "string"}
                ],
                "name": "createBatch",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "_batchId", "type": "uint256"},
                    {"internalType": "string", "name": "_step", "type": "string"}
                ],
                "name": "addTrackingStep",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256", "name": "_batchId", "type": "uint256"}],
                "name": "getBatchHistory",
                "outputs": [
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "origin", "type": "string"},
                    {"internalType": "string[]", "name": "trackingHistory", "type": "string[]"},
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "batchCount",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]

    def is_connected(self) -> bool:
        """
        Check if the service is connected to the blockchain.

        :return: True if connected, False otherwise
        """
        try:
            return self.w3.is_connected()
        except Exception as e:
            logger.error(f"Error checking connection: {str(e)}")
            return False

    def get_batch_count(self) -> Optional[int]:
        """
        Get the total number of batches on the blockchain.

        :return: The batch count or None if there's an error
        """
        try:
            if not self.contract:
                logger.error("Contract not loaded")
                return None
            return self.contract.functions.batchCount().call()
        except Exception as e:
            logger.error(f"Error getting batch count: {str(e)}")
            return None

"""
Blockchain service module for interacting with the BatchTracker smart contract.
Handles Web3 connections, contract interactions, and blockchain data retrieval.
"""

from web3 import Web3
import json
import os
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class BlockchainService:
    """Service for interacting with the BatchTracker smart contract on the blockchain."""

    def __init__(self, provider_url: str = "http://localhost:8545", contract_address: Optional[str] = None):
        """
        Initialize the blockchain service.

        :param provider_url: The URL of the blockchain provider (default: local Ganache)
        :param contract_address: The address of the deployed BatchTracker contract
        """
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.provider_url = provider_url
        self.contract_address = contract_address
        self.contract = None
        self.contract_abi = None
        self.private_key = os.getenv('BLOCKCHAIN_PRIVATE_KEY')  # Optional private key for signing
        self.from_address = os.getenv('BLOCKCHAIN_FROM_ADDRESS')  # Optional from address

        # Attempt to connect and load the contract
        try:
            if not self.w3.is_connected():
                logger.warning(f"Failed to connect to blockchain provider: {provider_url}")
            else:
                logger.info(f"Successfully connected to blockchain at {provider_url}")
                self._load_contract()
                self._setup_sender_account()
        except Exception as e:
            logger.error(f"Error initializing blockchain service: {str(e)}")

    def _setup_sender_account(self):
        """Setup the sender account for transactions."""
        try:
            # Use configured address if provided
            if self.from_address:
                self.from_address = Web3.to_checksum_address(self.from_address)
                logger.info(f"Using configured sender address: {self.from_address}")
            else:
                # Default to first available account (Ganache has unlocked accounts by default)
                accounts = self.w3.eth.accounts
                if accounts:
                    self.from_address = accounts[0]
                    logger.info(f"Using default sender address: {self.from_address}")
                else:
                    logger.warning("No accounts available on blockchain")
        except Exception as e:
            logger.error(f"Error setting up sender account: {str(e)}")

    def _load_contract(self):
        """Load the BatchTracker contract ABI and initialize the contract instance."""
        try:
            # Try to load the contract ABI from a JSON file
            abi_path = os.path.join(os.path.dirname(__file__), "..", "..", "contracts", "BatchTracker.json")
            
            # Fallback to a basic ABI definition if file doesn't exist
            if os.path.exists(abi_path):
                with open(abi_path, 'r') as f:
                    contract_data = json.load(f)
                    self.contract_abi = contract_data.get('abi', contract_data)
                logger.info(f"Loaded contract ABI from {abi_path}")
            else:
                # Minimal ABI for the functions we need
                self.contract_abi = self._get_default_abi()
                logger.info("Using default contract ABI")

            if self.contract_address and self.contract_abi:
                self.contract = self.w3.eth.contract(
                    address=Web3.to_checksum_address(self.contract_address),
                    abi=self.contract_abi
                )
                logger.info(f"Contract loaded at address: {self.contract_address}")
        except Exception as e:
            logger.error(f"Error loading contract: {str(e)}")

    @staticmethod
    def _get_default_abi() -> List[Dict]:
        """
        Get the default ABI for the BatchTracker contract.
        
        :return: List of ABI definitions for BatchTracker functions
        """
        return [
            {
                "inputs": [
                    {"internalType": "string", "name": "_name", "type": "string"},
                    {"internalType": "string", "name": "_origin", "type": "string"}
                ],
                "name": "createBatch",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "_batchId", "type": "uint256"},
                    {"internalType": "string", "name": "_step", "type": "string"}
                ],
                "name": "addTrackingStep",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256", "name": "_batchId", "type": "uint256"}],
                "name": "getBatchHistory",
                "outputs": [
                    {"internalType": "string", "name": "name", "type": "string"},
                    {"internalType": "string", "name": "origin", "type": "string"},
                    {"internalType": "string[]", "name": "trackingHistory", "type": "string[]"},
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "batchCount",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]

    def is_connected(self) -> bool:
        """
        Check if the service is connected to the blockchain.

        :return: True if connected, False otherwise
        """
        try:
            return self.w3.is_connected()
        except Exception as e:
            logger.error(f"Error checking connection: {str(e)}")
            return False

    def get_batch_count(self) -> Optional[int]:
        """
        Get the total number of batches on the blockchain.

        :return: The batch count or None if there's an error
        """
        try:
            if not self.contract:
                logger.error("Contract not loaded")
                return None
            return self.contract.functions.batchCount().call()
        except Exception as e:
            logger.error(f"Error getting batch count: {str(e)}")
            return None

    def create_batch(self, name: str, origin: str, from_address: Optional[str] = None) -> Optional[str]:
        """
        Create a new batch on the blockchain.

        :param name: The name of the batch
        :param origin: The origin of the batch
        :param from_address: The address to send the transaction from (uses default if not provided)
        :return: The transaction hash or None if there's an error
        """
        try:
            if not self.contract:
                raise ValueError("Contract not loaded")

            sender = from_address or self.from_address
            if not sender:
                raise ValueError("No sender address available")

            # Build the transaction
            tx = self.contract.functions.createBatch(name, origin).build_transaction({
                'from': sender,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(sender)
            })

            # Sign and send the transaction
            if self.private_key:
                # If private key is provided, sign with it
                signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)
                tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            else:
                # Otherwise, use Ganache's unlocked account (no signature needed)
                tx_hash = self.w3.eth.send_transaction(tx)

            logger.info(f"Batch created with transaction hash: {tx_hash.hex()}")
            return tx_hash.hex()
        except Exception as e:
            logger.error(f"Error creating batch: {str(e)}")
            return None

    def add_tracking_step(self, batch_id: int, step: str, from_address: Optional[str] = None) -> Optional[str]:
        """
        Add a tracking step to a batch on the blockchain.

        :param batch_id: The ID of the batch
        :param step: The tracking step to add
        :param from_address: The address to send the transaction from (uses default if not provided)
        :return: The transaction hash or None if there's an error
        """
        try:
            if not self.contract:
                raise ValueError("Contract not loaded")

            sender = from_address or self.from_address
            if not sender:
                raise ValueError("No sender address available")

            # Build the transaction
            tx = self.contract.functions.addTrackingStep(batch_id, step).build_transaction({
                'from': sender,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(sender)
            })

            # Sign and send the transaction
            if self.private_key:
                # If private key is provided, sign with it
                signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)
                tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            else:
                # Otherwise, use Ganache's unlocked account (no signature needed)
                tx_hash = self.w3.eth.send_transaction(tx)

            logger.info(f"Tracking step added with transaction hash: {tx_hash.hex()}")
            return tx_hash.hex()
        except Exception as e:
            logger.error(f"Error adding tracking step: {str(e)}")
            return None

    def get_batch(self, batch_id: int) -> Optional[Dict]:
        """
        Retrieve batch information from the blockchain.

        :param batch_id: The ID of the batch to retrieve
        :return: A dictionary with batch information or None if there's an error
        """
        try:
            if not self.contract:
                raise ValueError("Contract not loaded")

            batch_data = self.contract.functions.getBatchHistory(batch_id).call()
            return {
                'id': batch_id,
                'name': batch_data[0],
                'origin': batch_data[1],
                'tracking_history': batch_data[2],
                'timestamp': batch_data[3]
            }
        except Exception as e:
            logger.error(f"Error retrieving batch {batch_id}: {str(e)}")
            return None

    def get_all_batches(self) -> Optional[List[Dict]]:
        """
        Retrieve all batches from the blockchain.

        :return: A list of batch dictionaries or None if there's an error
        """
        try:
            batch_count = self.get_batch_count()
            if batch_count is None or batch_count == 0:
                return []

            batches = []
            for batch_id in range(1, batch_count + 1):
                batch = self.get_batch(batch_id)
                if batch:
                    batches.append(batch)

            return batches
        except Exception as e:
            logger.error(f"Error retrieving all batches: {str(e)}")
            return None

    def get_batch(self, batch_id: int) -> Optional[Dict]:
        """
        Retrieve batch information from the blockchain.

        :param batch_id: The ID of the batch to retrieve
        :return: A dictionary with batch information or None if there's an error
        """
        try:
            if not self.contract:
                raise ValueError("Contract not loaded")

            batch_data = self.contract.functions.getBatchHistory(batch_id).call()
            return {
                'id': batch_id,
                'name': batch_data[0],
                'origin': batch_data[1],
                'tracking_history': batch_data[2],
                'timestamp': batch_data[3]
            }
        except Exception as e:
            logger.error(f"Error retrieving batch {batch_id}: {str(e)}")
            return None

    def get_all_batches(self) -> Optional[List[Dict]]:
        """
        Retrieve all batches from the blockchain.

        :return: A list of batch dictionaries or None if there's an error
        """
        try:
            batch_count = self.get_batch_count()
            if batch_count is None or batch_count == 0:
                return []

            batches = []
            for batch_id in range(1, batch_count + 1):
                batch = self.get_batch(batch_id)
                if batch:
                    batches.append(batch)

            return batches
        except Exception as e:
            logger.error(f"Error retrieving all batches: {str(e)}")
            return None
