import time
from vesta.main import Vesta
from vesta.constants import tokens
from web3 import Web3
from vesta.token import Token
import pandas as pd

# Instantiate Vesta and Token
vsta = Vesta(web3_provider=Web3.HTTPProvider(''), etherscan_api_key_token='', moralis_api_key='')
JLP = Token(**tokens.get("JLP"))

# Parameters
supply = 46_026_812.892
risk_free_rate = 0.05
T = 1  # Denoting a month (Average DeFi loan length)
t = 0
sigma = 5 * (31/365)
init_asset_weight = 0.66
init_liab_weight = 1
maint_asset_weight = 0.75
maint_liab_weight = 1
deposit_limit = 1_000_000
slippage = 1.16

# DataFrame to store the results
results_df = pd.DataFrame()

try:
    while True:

        obs = vsta.data.coingecko.get_historical_market_data(JLP, 1)
        price = obs['price'].values[-1]

        current_risks_df = vsta.risk.calculate_current_values(vsta, price, T, t, risk_free_rate, sigma, init_asset_weight, maint_asset_weight, 1, 1, deposit_limit, slippage, supply)
        results_df = pd.concat([results_df, current_risks_df], ignore_index=True)
        
        print(results_df)

        # Gecko updates every 30 seconds  
        time.sleep(40)

except KeyboardInterrupt:
    print("Polling stopped.")

