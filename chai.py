from vesta.main import Vesta
from vesta.constants import tokens
from web3 import Web3
from vesta.token import Token
import time

# Instantiate the web3 researc provider with etherscan and infura
vsta = Vesta(
    web3_provider=Web3.HTTPProvider('https://mainnet.infura.io/v3/bd65e1b7072a41afa017a3f519f94e70'), 
    etherscan_api_key_token='YH3MU89IDWFIFABFF4VMYEHNBV9HGX3BHU', 
    moralis_api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImVjMzQ4Y2I2LTU1YmMtNGU0My1iNWY5LTc3YTNjYmYwZjZkNyIsIm9yZ0lkIjoiNTAwMDEiLCJ1c2VySWQiOiI0OTY1OCIsInR5cGVJZCI6IjI1NDFhNTZjLWE2MjEtNGJiMy04YjZlLTA2OGRlNTY0NzE0MiIsInR5cGUiOiJQUk9KRUNUIiwiaWF0IjoxNjk3NDg2OTg1LCJleHAiOjQ4NTMyNDY5ODV9.zvAk6YCAL1oYdMF4T7gw9RIF19Hbve4L6qUJS1I8hsQ')
chai = Token(**tokens.get("CHAI"))

for token in tokens:
    vsta.rate(Token(**tokens.get(token)))
    time.sleep(0.1)

