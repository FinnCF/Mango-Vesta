from vesta.main import Vesta
from vesta.constants import tokens
from web3 import Web3
from vesta.token import Token
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
from tqdm import tqdm
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Instantiate the web3 research provider with etherscan and infura (replace with actual keys)
vsta = Vesta(web3_provider=Web3.HTTPProvider(''), etherscan_api_key_token='', moralis_api_key='')
JLP = Token(**tokens.get("JLP"))

# Initialize the dictionary to store slippage data
slippage = {}

# Progress bar setup
total_values = np.linspace(0, 50_000_000, 51)
pbar = tqdm(total=len(total_values), desc="Calculating Slippage")

print(total_values)
for value in total_values:
    if value == 0:
        continue
    total = []
    iterations = 6
    for i in range(iterations):
        # Simulate slippage data retrieval (replace with actual data retrieval)
        slippage_at_liquidation = vsta.data.jupiter.get_usdc_swap_price_slippage(JLP, value)
        logging.info(f'Slippage at {value}: {slippage_at_liquidation}')
        total.append(slippage_at_liquidation)
        time.sleep(20)  # Simulate delay

    slippage[value] = np.median(total)
    logging.info(f'Max slippage for value {value}: {np.median(total)}')
    pbar.update(1)

# Close the progress bar
pbar.close()

# Convert the data to a DataFrame
df_slippage = pd.DataFrame(list(slippage.items()), columns=['Value', 'Max Slippage'])

# Save to CSV
df_slippage.to_csv('Slippage.csv', index=False)
logging.info("Slippage data saved to Slippage.csv")

sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_slippage, x="Value", y="Max Slippage")
plt.title('Slippage Analysis')
plt.xlabel('Value')
plt.ylabel('Max Slippage')
plt.savefig('Slippage_Plot.png')
logging.info("Slippage plot saved to Slippage_Plot.png")
plt.show()
