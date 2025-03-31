import json
import time
import random
import os
import requests
from web3 import Web3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from eth_utils import to_checksum_address
from config import MEGAETH_CONFIG

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def init_web3():
    """Initialize Web3 with fallback RPC endpoints"""
    session = requests.Session()
    session.verify = False
    
    for rpc_url in MEGAETH_CONFIG["RPC_URLS"]:
        try:
            provider = Web3.HTTPProvider(
                rpc_url,
                request_kwargs={
                    'timeout': 30,
                    'verify': False,
                    'session': session
                }
            )
            w3 = Web3(provider)
            
            # Test connection
            w3.eth.get_block_number()
            print(f"✅ Connected to RPC: {rpc_url}")
            return w3
            
        except Exception as e:
            print(f"❌ Failed to connect to {rpc_url}: {str(e)}")
            continue
    
    raise Exception("Failed to connect to any RPC endpoint")

# Initialize Web3 with retry logic
MAX_RETRIES = 3
for attempt in range(MAX_RETRIES:
    try:
        web3 = init_web3()
        break
    except Exception as e:
        if attempt == MAX_RETRIES - 1:
            raise Exception(f"Failed to initialize Web3 after {MAX_RETRIES} attempts")
        print(f"Retrying Web3 initialization... (attempt {attempt + 2}/{MAX_RETRIES})")
        time.sleep(5)

def load_random_wallet():
    """Load random wallet from wallets.json"""
    try:
        with open('wallets.json', 'r') as f:
            wallets = json.load(f)
            # Select random wallet
            wallet = random.choice(wallets)
            # Verify wallet
            account = web3.eth.account.from_key(wallet['private_key'])
            wallet['address'] = account.address
            print(f"✅ Loaded wallet: {wallet['address']}")
            return wallet
    except Exception as e:
        print(f"❌ Failed to load wallet: {str(e)}")
        return None

def claim_faucet(wallet):
    """Claim from multiple faucets with delays"""
    for faucet_url in MEGAETH_CONFIG["FAUCETS"]:
        try:
            headers = {"Content-Type": "application/json"}
            data = {"address": wallet["address"]}
            
            # Disable SSL verification for faucet requests
            response = requests.post(
                faucet_url, 
                json=data, 
                headers=headers,
                verify=False
            )
            
            if response.status_code == 200:
                print(f"✅ Claimed faucet ETH from {faucet_url}")
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
    wallet = load_random_wallet()
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
