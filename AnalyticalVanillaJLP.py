from vesta.main import Vesta
from vesta.constants import tokens
from web3 import Web3
from vesta.token import Token
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator


# Instantiate the web3 researc provider with etherscan and infura
vsta = Vesta(web3_provider=Web3.HTTPProvider(''), etherscan_api_key_token='', moralis_api_key='')
JLP = Token(**tokens.get("JLP"))

# Hourly data of 31 previous days (1 month)
price = 2.032
supply = 55_505_350.027
risk_free_rate = 0.05

# Parameters
time_steps = 718
T = 1 #Denoting a month (Average DeFi loan length)
t = 0
sigma = 4 * (31/365)

# Parameter settings estimation
init_asset_weights = [0.66, 0.75]
init_liab_weight = 1
maint_asset_weights = [0.75, 0.9]
maint_liab_weight = 1
deposit_limits_and_slippages = [{750_000: 0.88}, {1_000_000: 1.16}, {2_000_000: 1.53}, {5_000_000: 1.67}, {5_000_000: 1.67}, {5_000_000: 1.673}, {10_000_000: 1.67}, {20_000_000: 1.67}, {30_000_000: 1.673}, {30_000_000: 1.673}, {30_000_000: 1.673}, {50_000_000: 1.673} ]
remaining_time_values = np.linspace(T - t, 0, 718)  # From T-t to 0

# Loop to calculate and print the summary for each setting
master_df = pd.DataFrame()
for init_weight in init_asset_weights:
    for maint_weight in maint_asset_weights:
        if maint_weight > init_weight: # If maint = init then loan is initialised on liqudation price (unfortunate...)
            for deposit_slippage in deposit_limits_and_slippages:
                for deposit_limit, slippage in deposit_slippage.items():
                    current_risks_df = vsta.risk.calculate_current_values_vanilla(vsta, price, T, t, risk_free_rate, sigma, init_weight, maint_weight, 1, 1, deposit_limit, slippage, supply)
                    print('--------------')
                    print(f"Summary of Current Exposure and Risks for Setting - Init: {init_weight}, Maint: {maint_weight}, Limit: {deposit_limit}, Slippage: {slippage}:")
                    print(current_risks_df)
                    master_df = pd.concat([master_df, current_risks_df], ignore_index=True)
master_df.to_csv('new.csv')

# Observing nature of the put option.
price_range = np.linspace(0.1, price * 2, 250)  
time_periods_for_plot = np.linspace(0, 0.99, 5)

# Plotting
fig, axs = plt.subplots(3, 1, figsize=(12, 30))

# Titles and labels for each subplot
titles = ['Value vs. Price', 'Delta vs. Price', 'Gamma vs. Price']
y_labels = ['Value', 'Delta', 'Gamma']

for i, (ax, title, y_label) in enumerate(zip(axs, titles, y_labels)):
    for t in time_periods_for_plot:
        liq_price = (price * init_asset_weights[0]) / maint_asset_weights[0]
        if i == 0:
            values = [vsta.analytical.vanilla_put_price(p, liq_price, T, t, risk_free_rate, sigma) for p in price_range]
        elif i == 1:
            values = [vsta.analytical.vanilla_put_delta(p, liq_price, T, t, risk_free_rate, sigma) for p in price_range]
        elif i == 2:
            values = [vsta.analytical.vanilla_put_gamma(p, liq_price, T, t, risk_free_rate, sigma) for p in price_range]
        ax.plot(price_range, values, label=f'Time to Expiry: {round(100 * (T-t)) / 100}')

    # Set common properties for all plots
    ax.set_title(title)
    ax.set_xlabel('Price')
    ax.set_ylabel(y_label)
    ax.axvline(x=liq_price, color='red', linestyle='--', label='Liquidation Price')
    ax.legend(title='Time Periods', loc='upper left')
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.grid(visible=True, which='both', linestyle='--', linewidth=0.5)

plt.tight_layout()
plt.show()
