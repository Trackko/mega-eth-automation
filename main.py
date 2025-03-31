from web3 import Web3
import json

# Connect to Mega ETH Testnet
rpc_url = "https://rpc.megaeth.io"
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Load wallet details
with open('wallets.json', 'r') as f:
    wallets = json.load(f)

# Example: Send transactions
def send_transaction(wallet):
    txn = {
        'to': Web3.to_checksum_address("0xRecipientAddress"),
        'value': web3.to_wei(0.01, 'ether'),  # Changed from toWei
        'gas': 21000,
        'gasPrice': web3.to_wei('5', 'gwei'),  # Changed from toWei
        'nonce': web3.eth.get_transaction_count(wallet['address'])  # Changed from getTransactionCount
    }
    signed_txn = web3.eth.account.sign_transaction(txn, wallet['private_key'])
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)  # Changed from sendRawTransaction
    print(f"Transaction sent: {tx_hash.hex()}")

# Run transactions
for wallet in wallets:
    send_transaction(wallet)