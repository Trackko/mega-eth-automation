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
    for rpc_url in MEGAETH_CONFIG["RPC_URLS"]:
        try:
            # Create Web3 instance with simple configuration
            provider = Web3.HTTPProvider(
                rpc_url,
                request_kwargs={'timeout': 30}
            )
            w3 = Web3(provider)
            
            # Test connection
            block_number = w3.eth.get_block_number()
            print(f"✅ Connected to RPC: {rpc_url} (Block: {block_number})")
            return w3
            
        except Exception as e:
            print(f"❌ Failed to connect to {rpc_url}: {str(e)}")
            continue
    
    raise Exception("Failed to connect to any RPC endpoint")

# Initialize Web3 with retry logic
MAX_RETRIES = 3

def setup_web3():
    for attempt in range(MAX_RETRIES):
        try:
            return init_web3()
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise Exception(f"Failed to initialize Web3 after {MAX_RETRIES} attempts")
            print(f"Retrying Web3 initialization... (attempt {attempt + 2}/{MAX_RETRIES})")
            time.sleep(5)

# Initialize Web3
web3 = setup_web3()

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

def claim_all_faucets(wallet):
    """Claim from all available faucets with delays"""
    print(f"\n🚰 Attempting to claim from {len(MEGAETH_CONFIG['FAUCETS'])} faucets...")
    
    for faucet_url in MEGAETH_CONFIG['FAUCETS']:
        try:
            print(f"\n📍 Claiming from: {faucet_url}")
            
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            data = {"address": wallet["address"]}
            
            response = requests.post(
                faucet_url,
                json=data,
                headers=headers,
                verify=False,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Successfully claimed from {faucet_url}")
                
                # Random delay between faucet claims
                delay = random.randint(*MEGAETH_CONFIG["DELAYS"]["BETWEEN_FAUCETS"])
                print(f"⏳ Waiting {delay} seconds before next claim...")
                time.sleep(delay)
            else:
                print(f"❌ Failed to claim from {faucet_url}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error claiming from {faucet_url}: {str(e)}")
            continue

def perform_random_interactions(wallet):
    """Perform random interactions with different protocols"""
    # Determine number of transactions for today
    num_txs = random.randint(*MEGAETH_CONFIG["DELAYS"]["DAILY_TX_COUNT"])
    print(f"\n🎲 Planning {num_txs} transactions for today")
    
    # Get all possible interaction types
    interaction_types = list(MEGAETH_CONFIG["INTERACTIONS"].keys())
    
    for tx_num in range(num_txs):
        try:
            # Choose random interaction type
            interaction_type = random.choice(interaction_types)
            projects = MEGAETH_CONFIG["INTERACTIONS"][interaction_type]
            project = random.choice(projects)
            
            print(f"\n🔄 Transaction {tx_num + 1}/{num_txs}")
            print(f"📍 Interacting with: {project['name']} ({project['url']})")
            
            # Perform interaction based on type
            if interaction_type == "SWAPS":
                # Add swap logic here
                pass
            elif interaction_type == "LIQUIDITY":
                # Add liquidity logic here
                pass
            elif interaction_type == "NFT":
                # Add NFT interaction logic here
                pass
            
            # Random delay between transactions
            delay = random.randint(*MEGAETH_CONFIG["DELAYS"]["BETWEEN_TXS"])
            print(f"⏳ Waiting {delay} seconds before next transaction...")
            time.sleep(delay)
            
        except Exception as e:
            print(f"❌ Error in transaction {tx_num + 1}: {str(e)}")
            continue

def main():
    try:
        # Load random wallet
        wallet = load_random_wallet()
        if not wallet:
            raise Exception("No valid wallet found")
            
        print(f"🏁 Starting automation with wallet: {wallet['address']}")
        
        # Check initial balance
        balance = web3.eth.get_balance(wallet['address'])
        print(f"💰 Initial balance: {web3.from_wei(balance, 'ether')} ETH")
        
        # Claim from faucets if balance is low
        if balance < web3.to_wei(0.1, 'ether'):
            print("⚠️ Low balance detected, claiming from faucets...")
            claim_all_faucets(wallet)
            
            # Wait for faucet transactions to process
            time.sleep(60)
            
            # Check new balance
            new_balance = web3.eth.get_balance(wallet['address'])
            print(f"💰 New balance after claims: {web3.from_wei(new_balance, 'ether')} ETH")
        
        # Perform random interactions
        perform_random_interactions(wallet)
        
        print("\n✅ Daily automation completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Automation failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
