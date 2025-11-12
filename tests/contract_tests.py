from web3 import Web3
import pytest

# Connect to the local Ethereum blockchain
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Load the compiled contract
with open('boba-chain/contracts/BatchTracker.json') as f:
    contract_json = json.load(f)
    BatchTracker = w3.eth.contract(
        address='0xYourContractAddress',  # Replace with your deployed contract address
        abi=contract_json['abi']
    )

@pytest.fixture
def deploy_contract():
    # Deploy the contract before each test
    account = w3.eth.accounts[0]
    tx_hash = BatchTracker.constructor().transact({'from': account})
    w3.eth.waitForTransactionReceipt(tx_hash)
    return BatchTracker

def test_create_batch(deploy_contract):
    batch_tracker = deploy_contract
    account = w3.eth.accounts[0]
    
    # Create a new batch
    tx_hash = batch_tracker.functions.createBatch("Boba Tea", "Taiwan").transact({'from': account})
    w3.eth.waitForTransactionReceipt(tx_hash)

    # Verify the batch was created
    batch = batch_tracker.functions.getBatch(0).call()
    assert batch[0] == "Boba Tea"
    assert batch[1] == "Taiwan"

def test_add_tracking_step(deploy_contract):
    batch_tracker = deploy_contract
    account = w3.eth.accounts[0]
    
    # Create a new batch
    tx_hash = batch_tracker.functions.createBatch("Boba Tea", "Taiwan").transact({'from': account})
    w3.eth.waitForTransactionReceipt(tx_hash)

    # Add a tracking step
    tx_hash = batch_tracker.functions.addTrackingStep(0, "Harvested").transact({'from': account})
    w3.eth.waitForTransactionReceipt(tx_hash)

    # Verify the tracking step was added
    tracking_steps = batch_tracker.functions.getTrackingSteps(0).call()
    assert "Harvested" in tracking_steps

def test_get_batch_history(deploy_contract):
    batch_tracker = deploy_contract
    account = w3.eth.accounts[0]
    
    # Create a new batch
    tx_hash = batch_tracker.functions.createBatch("Boba Tea", "Taiwan").transact({'from': account})
    w3.eth.waitForTransactionReceipt(tx_hash)

    # Add tracking steps
    batch_tracker.functions.addTrackingStep(0, "Harvested").transact({'from': account})
    batch_tracker.functions.addTrackingStep(0, "Processed").transact({'from': account})

    # Get batch history
    history = batch_tracker.functions.getBatchHistory(0).call()
    assert len(history) == 2  # Ensure there are two tracking steps
    assert "Harvested" in history
    assert "Processed" in history