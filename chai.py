from vesta.main import Vesta
from vesta.constants import tokens
from web3 import Web3
from vesta.token import Token
import pandas as pd
import time

# Instantiate the web3 researc provider with etherscan and infura
vsta = Vesta(
    web3_provider=Web3.HTTPProvider(''), 
    etherscan_api_key_token='', 
    moralis_api_key='')
chai = Token(**tokens.get("CHAI"))

# Initialize empty list to hold dictionaries
rankings_list = []

# Iterate over tokens
for token in tokens:
    token_chosen = Token(**tokens.get(token))
    [symbol, method_results, ranking, total_value] = vsta.rate(token_chosen)
    method_results['symbol'] = symbol
    method_results['total_value'] = total_value
    method_results['ranking'] = ranking
    rankings_list.append(method_results)
    time.sleep(15)

# Convert list of dictionaries to DataFrame
rankings = pd.DataFrame(rankings_list)
print(rankings)
rankings.to_csv('rankings.csv', index=False)
