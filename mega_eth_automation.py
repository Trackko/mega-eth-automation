import json
import time
import random
import os
import requests
from web3 import Web3

# ========== CONFIG ==========
RPC_URL = "https://rpc.megaeth.io"  # MegaETH Testnet RPC

# Load wallets from wallets.json
def load_wallets():
    try:
        with open('wallets.json', 'r') as f:
            wallets_data = json.load(f)
            print(f"✅ Loaded {len(wallets_data)} wallets from wallets.json")
            return wallets_data
    except FileNotFoundError:
        print("❌ wallets.json not found")
        return []
    except json.JSONDecodeError:
        print("❌ Invalid JSON format in wallets.json")
        return []

# Initialize wallets
wallets = load_wallets()

# Update transaction targets from wallet addresses
TRANSACTION_TARGETS = [wallet['address'] for wallet in wallets]

FAUCETS = [
    "https://testnet.megaeth.com/#3",
]

web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Global index tracker for faucet claiming
FAUCET_INDEX_FILE = "faucet_index.json"

# Load faucet index
if os.path.exists(FAUCET_INDEX_FILE):
    with open(FAUCET_INDEX_FILE, "r") as f:
        faucet_index = json.load(f)
else:
    faucet_index = {"last_wallet": 0}

# ========== FUNCTIONS ==========

def claim_faucet(wallet):
    """ Claim ETH from a faucet. """
    faucet_url = random.choice(FAUCETS)
    headers = {"Content-Type": "application/json"}
    
    data = {
        "address": wallet["address"]
    }

    response = requests.post(faucet_url, json=data, headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Claimed faucet ETH for {wallet['address']}")
    else:
        print(f"❌ Failed to claim faucet for {wallet['address']}")

def send_transaction(private_key, to_address, amount_eth):
    """ Send a transaction with a random gas fee and delay. """
    try:
        account = web3.eth.account.from_key(private_key)
        nonce = web3.eth.get_transaction_count(account.address)
        
        # Validate to_address
        if not Web3.is_address(to_address):
            raise ValueError(f"Invalid Ethereum address: {to_address}")
            
        txn = {
            'to': Web3.to_checksum_address(to_address),
            'value': web3.to_wei(amount_eth, 'ether'),
            'gas': random.randint(21000, 50000),
            'gasPrice': web3.to_wei(random.randint(5, 50), 'gwei'),
            'nonce': nonce,
        }

        signed_txn = web3.eth.account.sign_transaction(txn, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"✅ Sent {amount_eth} ETH from {account.address} to {to_address} → {tx_hash.hex()}")
        
    except ValueError as e:
        print(f"❌ Transaction failed: {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

def execute_random_transaction(wallet):
    """ Perform different transaction types randomly. """
    transaction_type = random.choice(["send", "swap", "liquidity", "nft"])

    if transaction_type == "send":
        # Choose a random target address that isn't the sender
        to_address = random.choice([addr for addr in TRANSACTION_TARGETS 
                                  if addr.lower() != wallet["address"].lower()])
        amount_eth = random.uniform(0.001, 0.01)  # Random amount between 0.001 and 0.01 ETH
        send_transaction(wallet["private_key"], to_address, amount_eth)
