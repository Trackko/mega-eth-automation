"""Configuration file for MegaETH automation"""

MEGAETH_CONFIG = {
    "RPC_URLS": [
        "https://rpc.testnet.megaeth.io",
        "https://megaeth-testnet.rpc.io",
        "http://rpc.megaeth.io"  # Fallback HTTP endpoint
    ],
    "EXPLORER": "https://megaexplorer.xyz",
    
    # Faucets ordered by priority
    "FAUCETS": [
        "https://testnet.megaeth.com/#3",
    ],
    
    # Project contracts and interactions
    "PROJECTS": {
        "gte": {
            "url": "https://www.gte.xyz",
            "contract": "0xYourGTEContractAddress",
            "type": "swap"
        },
        "teko": {
            "url": "https://teko.app",
            "contract": "0xYourTekoContractAddress",
            "type": "liquidity"
        },
        "xl_meme": {
            "url": "https://testnet.xlmeme.com/megaeth",
            "contract": "0xYourXLMemeContractAddress",
            "type": "token"
        }
    },
    
    # Transaction settings
    "TX_SETTINGS": {
        "min_delay": 3600,  # 1 hour
        "max_delay": 15000,  # 7 hour
        "daily_tx_count": 3 or 4,   # Daily transaction count
        "gas_multiplier": 1.1
    }
}