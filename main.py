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
        'to': Web3.toChecksumAddress("0xRecipientAddress"),
        'value': web3.toWei(0.01, 'ether'),
        'gas': 21000,
        'gasPrice': web3.toWei('5', 'gwei'),
        'nonce': web3.eth.getTransactionCount(wallet['address'])
    }
    signed_txn = web3.eth.account.sign_transaction(txn, wallet['private_key'])
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f"Transaction sent: {tx_hash.hex()}")

# Run transactions
for wallet in wallets:
    send_transaction(wallet)
