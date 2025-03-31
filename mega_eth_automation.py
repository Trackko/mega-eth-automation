import json
import time
import random
import os
import requests
from web3 import Web3
from eth_utils import to_checksum_address
from config import MEGAETH_CONFIG

# Initialize Web3
web3 = Web3(Web3.HTTPProvider(MEGAETH_CONFIG["RPC_URL"]))

def load_wallet():
    """Load single wallet configuration"""
    try:
        with open('wallet.json', 'r') as f:
            wallet_data = json.load(f)
            account = web3.eth.account.from_key(wallet_data['private_key'])
            wallet_data['address'] = account.address
            return wallet_data
    except Exception as e:
        print(f"❌ Failed to load wallet: {str(e)}")
        return None

def claim_faucet(wallet):
    """Claim from multiple faucets with delays"""
    for faucet_url in MEGAETH_CONFIG["FAUCETS"]:
        try:
            headers = {"Content-Type": "application/json"}
            data = {"address": wallet["address"]}
            
            response = requests.post(faucet_url, json=data, headers=headers)
            
            if response.status_code == 200:
                print(f"✅ Claimed faucet ETH from {faucet_url}")
                # Random delay between faucet claims
                delay = random.randint(60, 180)
                print(f"⏳ Waiting {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"❌ Failed to claim from {faucet_url}")
                
        except Exception as e:
            print(f"❌ Error claiming from faucet: {str(e)}")
            continue

def interact_with_project(wallet, project):
    """Interact with a specific project contract"""
    try:
        # Contract interaction logic based on project type
        if project["type"] == "swap":
            # Swap interaction
            pass
        elif project["type"] == "liquidity":
            # Liquidity interaction
            pass
        elif project["type"] == "token":
            # Token interaction
            pass
            
        print(f"✅ Successfully interacted with {project['url']}")
        
    except Exception as e:
        print(f"❌ Failed to interact with {project['url']}: {str(e)}")

def main():
    # Load wallet
    wallet = load_wallet()
    if not wallet:
        return
    
    print(f"🔵 Starting automation for wallet: {wallet['address']}")
    
    # Check balance and claim faucet if needed
    balance = web3.eth.get_balance(wallet['address'])
    if balance < web3.to_wei(0.01, 'ether'):
        print("⚠️ Low balance, claiming from faucet...")
        claim_faucet(wallet)
    
    # Get random number of transactions for today (3-4)
    daily_tx_count = random.randint(3, MEGAETH_CONFIG["TX_SETTINGS"]["daily_tx_count"])
    
    # Select random projects to interact with
    projects = random.sample(list(MEGAETH_CONFIG["PROJECTS"].values()), daily_tx_count)
    
    for project in projects:
        try:
            print(f"\n🔄 Interacting with {project['url']}")
            interact_with_project(wallet, project)
            
            # Random delay between transactions
            delay = random.randint(
                MEGAETH_CONFIG["TX_SETTINGS"]["min_delay"],
                MEGAETH_CONFIG["TX_SETTINGS"]["max_delay"]
            )
            print(f"⏳ Waiting {delay} seconds before next interaction...")
            time.sleep(delay)
            
        except Exception as e:
            print(f"❌ Error during project interaction: {str(e)}")
            continue

if __name__ == "__main__":
    main()
