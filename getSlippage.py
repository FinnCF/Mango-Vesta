from vesta.main import Vesta
from vesta.constants import tokens
from web3 import Web3
from vesta.token import Token
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from vesta.pricing.optimisers import Optimisers
from scipy import stats
from scipy.stats import gaussian_kde
import time

# Instantiate the web3 researc provider with etherscan and infura
vsta = Vesta(web3_provider=Web3.HTTPProvider(''), etherscan_api_key_token='', moralis_api_key='')
JLP = Token(**tokens.get("JLP"))

slippage = {}
for value in [1_000_000]:
    total = []
    iterations = 5
    for i in range(iterations):
        slippage_at_liquidation = vsta.data.jupiter.get_usdc_swap_price_slippage(JLP, value)
        print(slippage_at_liquidation)
        total.append(slippage_at_liquidation)
        time.sleep(20)
    slippage[value] = max(total)
    print(f'Max for value {value}: ', max(total))
    time.sleep(5)
print(slippage)
