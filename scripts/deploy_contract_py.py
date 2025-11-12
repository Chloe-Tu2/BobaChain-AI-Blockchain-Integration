#!/usr/bin/env python3
"""
Compile and deploy BatchTracker.sol to a local Ganache node (http://127.0.0.1:8545)

Requirements:
    pip install py-solc-x web3

Usage:
    1. Start Ganache (or Docker compose): ganache-cli --port 8545
    2. Run: python scripts/deploy_contract_py.py

This script will compile `contracts/BatchTracker.sol`, deploy it to the node,
and write `contracts/BatchTracker.json` with the deployed address and ABI so the
backend can auto-load it.
"""
import json
import os
from web3 import Web3
from solcx import compile_source, install_solc


def compile_contract(sol_path: str):
    with open(sol_path, 'r', encoding='utf-8') as f:
        source = f.read()

    # Ensure solc is installed
    try:
        install_solc('0.8.0')
    except Exception:
        # install_solc may raise if already installed; ignore
        pass

    compiled = compile_source(source, output_values=['abi', 'bin'], solc_version='0.8.0')
    # The key will be '<stdin>:BatchTracker' or file path; find the contract
    for key, value in compiled.items():
        if key.endswith(':BatchTracker'):
            return value['abi'], value['bin']
    raise RuntimeError('BatchTracker contract not found in compilation output')


def deploy(abi, bytecode, provider_url='http://127.0.0.1:8545'):
    w3 = Web3(Web3.HTTPProvider(provider_url))
    if not w3.is_connected():
        raise RuntimeError(f'Unable to connect to blockchain at {provider_url}')

    # Use the first account (Ganache provides unlocked accounts)
    acct = w3.eth.accounts[0]
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor().transact({'from': acct})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    address = tx_receipt.contractAddress
    return address


def write_artifact(path: str, address: str, abi):
    data = {
        'address': address,
        'abi': abi
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sol_path = os.path.join(repo_root, 'contracts', 'BatchTracker.sol')
    out_path = os.path.join(repo_root, 'contracts', 'BatchTracker.json')

    print('Compiling contract...')
    abi, bytecode = compile_contract(sol_path)
    print('Connecting to local blockchain...')
    address = deploy(abi, bytecode)
    print(f'Deployed BatchTracker at: {address}')
    write_artifact(out_path, address, abi)
    print(f'Wrote artifact to: {out_path}')


if __name__ == '__main__':
    main()
