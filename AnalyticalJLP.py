from vesta.main import Vesta
from vesta.constants import tokens
from web3 import Web3
from vesta.token import Token
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Instantiate the web3 researc provider with etherscan and infura
vsta = Vesta(web3_provider=Web3.HTTPProvider(''), etherscan_api_key_token='', moralis_api_key='')
JLP = Token(**tokens.get("JLP"))

# Hourly data of 31 previous days (1 month)
data = vsta.data.coingecko.get_historical_market_data(JLP, 31)
obs = data['price'].values
price = obs[-1]
supply = 46_026_812.892
risk_free_rate = 0.05

# Parameters
time_steps = 718
T = 1 #Denoting a month (Average DeFi loan length)
t = 0

# Parameter settings estimation
settings = []
init_asset_weights = [0.66]
init_liab_weight = 1
maint_asset_weights = [0.75]
maint_liab_weight = 1
deposit_limits_and_slippages = [{250_000: 0.11}, {500_000: 0.29}, {750_000: 0.88}, {1_000_000: 1.16}, {2_000_000: 2.33}]
columns = ['Time', 'Analytical_Value', 'Delta', 'Short_Position', 'Gamma', 'Setting']
df = pd.DataFrame(columns=columns)
remaining_time_values = np.linspace(T - t, 0, 718)  # From T-t to 0

for init_weight in init_asset_weights:
    for maint_weight in maint_asset_weights:
        if(maint_weight > init_weight):   

            # Leverage, Liquidation price, Price drop required to achieve it, Probability of liquidation at current number of paths,
            leverage = 1 / (1 - init_weight)
            liq_price = (price * init_weight) / maint_weight
            price_drop = 100 * ((liq_price - price) / price)

            for deposit_slippage in deposit_limits_and_slippages:
                for deposit_limit, slippage in deposit_slippage.items():
                    
                    # Calculating percentage of market cap.
                    perc_of_mktcp = 100 * (deposit_limit / (supply * price))
                    quantity = deposit_limit / price

                    # Borrows calculation.
                    free_collateral_value = deposit_limit * init_weight
                    borrowed_value = (free_collateral_value / (1 - init_weight)) / init_liab_weight 
                    borrowed_value_weighted = borrowed_value * maint_liab_weight

                    # Insurance fund exposure (payoff of binary)
                    shortfall_value = borrowed_value_weighted * (slippage / 100) 

                    # Greeks and Price
                    values = [vsta.analtical.binary_put_price(price, liq_price, T, t, risk_free_rate, 5 * (31/365), shortfall_value) for t in remaining_time_values]
                    deltas = [vsta.analtical.binary_put_delta(price, liq_price, T, t, risk_free_rate, 5 * (31/365), shortfall_value) for t in remaining_time_values]
                    gammas = [vsta.analtical.binary_put_gamma(price, liq_price, T, t, risk_free_rate, 5 * (31/365), shortfall_value) for t in remaining_time_values]
                    short_positions = [-delta * shortfall_value for delta in deltas]

                    # Create a temporary DataFrame
                    temp_df = pd.DataFrame({
                        'Time': remaining_time_values,
                        'Analytical_Value': values,
                        'Delta': deltas,
                        'Short_Position': short_positions,
                        'Gamma': gammas,
                        'Setting': [f"Init: {init_weight}, Maint: {maint_weight}, Limit: {deposit_limit}, Slippage: {slippage}"] * len(remaining_time_values)
                    })

                    df = pd.concat([df, temp_df], ignore_index=True)

df.to_csv('Output.csv')
fig, axes = plt.subplots(4, 1, figsize=(10, 12))

# Plot Analytical Value
for setting, group in df.groupby('Setting'):
    group.plot(x='Time', y='Analytical_Value', ax=axes[0], label=setting)
axes[0].set_title('Analytical Value To Expiry')
axes[0].set_ylabel('Analytical Value')
axes[0].legend(title='Settings', bbox_to_anchor=(1.05, 1), loc='upper left')

# Plot Delta
for setting, group in df.groupby('Setting'):
    group.plot(x='Time', y='Delta', ax=axes[1], label=setting)
axes[1].set_title('Delta To Expiry')
axes[1].set_ylabel('Delta')
axes[1].legend(title='Settings', bbox_to_anchor=(1.05, 1), loc='upper left')

# Plot Gamma
for setting, group in df.groupby('Setting'):
    group.plot(x='Time', y='Gamma', ax=axes[2], label=setting)
axes[2].set_title('Gamma To Expiry')
axes[2].set_ylabel('Gamma')
axes[2].legend(title='Settings', bbox_to_anchor=(1.05, 1), loc='upper left')

# Plot Shorts
for setting, group in df.groupby('Setting'):
    group.plot(x='Time', y='Short_Position', ax=axes[3], label=setting)
axes[3].set_title('Short Position to Expiry')
axes[3].set_ylabel('Short Position')
axes[3].legend(title='Settings', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Additional Plot: Price vs. Delta for Different Time Periods
price_range = np.linspace(0, price * 2, 500)  # Example price range: 80% to 120% of last observed price
time_periods_for_plot = np.linspace(0, 1, 25)

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    deltas_for_prices = [vsta.analtical.binary_put_delta(p, liq_price, T, t, risk_free_rate, 5 * (31/365), shortfall_value) for p in price_range]
    ax.plot(price_range, deltas_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Delta vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Delta')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    deltas_for_prices = [vsta.analtical.binary_call_gamma(p, liq_price, T, t, risk_free_rate, 5 * (31/365), shortfall_value) for p in price_range]
    ax.plot(price_range, deltas_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Delta vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Gamma')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
