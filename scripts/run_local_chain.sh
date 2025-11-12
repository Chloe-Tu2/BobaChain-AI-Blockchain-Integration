#!/bin/bash

# This script runs a local blockchain instance using Ganache CLI for testing purposes.

# Check if Ganache CLI is installed
if ! command -v ganache-cli &> /dev/null
then
    echo "Ganache CLI could not be found. Please install it globally using npm:"
    echo "npm install -g ganache-cli"
    exit
fi

# Start Ganache CLI with specified options
ganache-cli --port 8545 --networkId 5777 --accounts 10 --defaultBalanceEther 1000 --mnemonic "candy maple cake sugar pudding cream honey rich smooth crumble sweet treat" &

# Wait for Ganache to start
sleep 5

echo "Local blockchain is running on http://localhost:8545"