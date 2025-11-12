from web3 import Web3
import json

# Connect to local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Load the smart contract
def load_contract():
    with open('boba-chain/contracts/BatchTracker.json') as f:
        contract_data = json.load(f)
    contract_address = contract_data['address']
    return w3.eth.contract(address=contract_address, abi=contract_data['abi'])

# Deploy the smart contract
def deploy_contract():
    # Set the default account (the first account in the local node)
    w3.eth.defaultAccount = w3.eth.accounts[0]

    # Load the contract's Solidity code
    with open('boba-chain/contracts/BatchTracker.sol') as f:
        contract_source_code = f.read()

    # Compile the contract
    compiled_contract = w3.eth.contract(abi=contract_source_code['abi'], bytecode=contract_source_code['evm']['bytecode']['object'])

    # Deploy the contract
    tx_hash = compiled_contract.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    print(f"Contract deployed at address: {tx_receipt.contractAddress}")

if __name__ == "__main__":
    deploy_contract()