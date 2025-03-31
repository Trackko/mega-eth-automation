"""Configuration file for MegaETH automation"""

MEGAETH_CONFIG = {
    "RPC_URLS": [
        "https://carrot.megaeth.com/rpc",
    ],
    
    "FAUCETS": [
        "https://testnet.megaeth.com/#3",
        "https://faucet.trade/megaeth-testnet-eth-faucet",
        "https://www.gas.zip/faucet/megaeth"
    ],
    
    "INTERACTIONS": {
        "SWAPS": [
            {
                "name": "GTE Exchange",
                "url": "https://www.gte.xyz",
                "router": "0xYourGTERouterAddress",
                "tokens": ["TOKEN1", "TOKEN2"]
            },
            {
                "name": "Bebop",
                "url": "https://bebop.xyz",
                "router": "0xYourBebopAddress"
            }
        ],
        "LIQUIDITY": [
            {
                "name": "Teko Finance",
                "url": "https://teko.app",
                "router": "0xYourTekoAddress"
            },
            {
                "name": "CAP Finance",
                "url": "https://cap.app/testnet",
                "router": "0xYourCAPAddress"
            }
        ],
        "NFT": [
            {
                "name": "AWE",
                "url": "https://awe.box",
                "contract": "0xYourAWEAddress"
            },
            {
                "name": "Biomes",
                "url": "https://biomes.aw",
                "contract": "0xYourBiomesAddress"
            }
        ]
    },
    
    "DELAYS": {
        "BETWEEN_FAUCETS": (60, 180),    # 1-3 minutes
        "BETWEEN_TXS": (300, 3600),      # 5-60 minutes
        "DAILY_TX_COUNT": (3, 4)         # 3-4 transactions per day
    }
}