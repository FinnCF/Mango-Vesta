# Mango Vesta
Mango Vesta is a risk assessment framework designed to evaluate the riskiness of assets in the Mango Markets DeX. The framework aggregates, normalizes, and weighs various risk factors, outputting a comprehensive risk score that can help in setting collateral requirements. 

See below for more detailed explanations of the Mango Markets protocol.
[https://docs.mango.markets](https://docs.mango.markets) 


## Installation

Simply install using pip3:

pip3 install mango-vesta

# Usage

Simply initiate the Vesta object using your web3 provider, etherscan API key and moralis api key, then construct a token object, and use it as a parameter in the .rate method. 

```python
from vesta.main import Vesta
from vesta.constants import tokens
from web3 import Web3
from vesta.token import Token

# Instantiate the web3 research provider with etherscan and infura
vsta = Vesta(
    web3_provider=Web3.HTTPProvider('https://mainnet.infura.io/v3/your-infura-project-id'),
    etherscan_api_key_token='your-etherscan-api-key',
    moralis_api_key='your-moralis-api-key'
)

# Get a token object for a specific token
chai = Token(**tokens.get("CHAI"))

# Get the risk rating for the token
vsta.rate(chai)
```

## Token Object Config

Tokens are formatted as so:
```
tokens = {
    "CHAI": {
        "symbol": "CHAI",
        "sol_address": "3jsFX1tx2Z8ewmamiwSU851GzyzM2DJMq7KWW5DM8Py3",  # Empty or equivalent Solana representation
        "sol_decimals": 8,
        "sol_created_at_block": 0,
        "eth_address": "0x06AF07097C9Eeb7fD685c692751D5C66dB49c215",  # CHAI's Ethereum address
        "eth_decimals": 18,
        "eth_created_at_block": 9666693,
        "bridging_entity": "Wormhole",
        "origin": "eth",
        'oracle_address': "CtJ8EkqLmeYyGB8s4jevpeNsvmD4dxVR2krfsDLcvV8Y"
    },
}
```

## Contributing

We welcome contributions to Mango Vesta. Please feel free to submit pull requests, create issues or spread the word.
