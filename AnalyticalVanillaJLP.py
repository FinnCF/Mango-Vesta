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
deposit_limits_and_slippages = [{750_000: 0.88}, {1_000_000: 1.16}, {2_000_000: 2.33}, {5_000_000: 5.83}]
columns = ['Time', 'Analytical_Value', 'Delta', 'Short_Position', 'Gamma', 'Theta', 'Speed', 'Vega', 'Setting']
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

                    # Insurance fund exposure (payoff as the)
                    shortfall_value = borrowed_value_weighted * (slippage / 100) 
                    shortfall_quantity = shortfall_value / price

                    # Greeks and Price
                    values = [vsta.analtical.vanilla_put_price(price, liq_price, T, t, risk_free_rate, 5 * (31/365)) for t in remaining_time_values]
                    deltas = [vsta.analtical.vanilla_put_delta(price, liq_price, T, t, risk_free_rate, 5 * (31/365)) for t in remaining_time_values]
                    gammas = [vsta.analtical.vanilla_put_gamma(price, liq_price, T, t, risk_free_rate, 5 * (31/365)) for t in remaining_time_values]
                    thetas = [vsta.analtical.vanilla_put_theta(price, liq_price, T, t, risk_free_rate, 5 * (31/365)) for t in remaining_time_values]
                    speed = [vsta.analtical.vanilla_put_speed(price, liq_price, T, t, risk_free_rate, 5 * (31/365)) for t in remaining_time_values]
                    vegas = [vsta.analtical.vanilla_put_vega(price, liq_price, T, t, risk_free_rate, 5 * (31/365)) for t in remaining_time_values]
                    short_positions = [-delta * shortfall_value for delta in deltas]

                    # Create a temporary DataFrame
                    temp_df = pd.DataFrame({
                        'Time': remaining_time_values,
                        'Analytical_Value': values,
                        'Delta': deltas, # wrt S
                        'Short_Position': short_positions,
                        'Gamma': gammas, # wrt S wrt S
                        'Theta': thetas, # wrt t
                        'Speed': speed, # wrt S wrt S wrt S
                        'Vega': vegas, # wrt sigma
                        'Setting': [f"Init: {init_weight}, Maint: {maint_weight}, Limit: {deposit_limit}, Slippage: {slippage}"] * len(remaining_time_values)
                    })
                    df = pd.concat([df, temp_df], ignore_index=True)

df.to_csv('Output.csv')
fig, axes = plt.subplots(2, 2, figsize=(10, 12))  
metrics = ['Analytical_Value', 'Delta', 'Gamma', 'Short_Position']
for i, metric in enumerate(metrics):
    row, col = divmod(i, 2) 
    for setting, group in df.groupby('Setting'):
        ax = group.plot(x='Time', y=metric, ax=axes[row, col], label=setting)
    axes[row, col].set_title(f'{metric} To Expiry')
    axes[row, col].set_ylabel(metric)
plt.tight_layout()
plt.show()

price_range = np.linspace(0.1, price * 2, 500)  
time_periods_for_plot = np.linspace(0, 1, 15)

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    values = [vsta.analtical.vanilla_put_price(p, liq_price, T, t, risk_free_rate, 5 * (31/365)) for p in price_range]
    ax.plot(price_range, values, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Value for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Value')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    deltas_for_prices = [vsta.analtical.vanilla_put_delta(p, liq_price, T, t, risk_free_rate, 5 * (31/365)) for p in price_range]
    ax.plot(price_range, deltas_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Delta vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Delta')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    gammas_for_prices = [vsta.analtical.vanilla_put_gamma(p, liq_price, T, t, risk_free_rate, 5 * (31/365)) for p in price_range]
    ax.plot(price_range, gammas_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Delta vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Gamma')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    thetas_for_prices = [vsta.analtical.vanilla_put_theta(p, liq_price, T, t, risk_free_rate, 5 * (31/365)) for p in price_range]
    ax.plot(price_range, thetas_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Theta vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Theta')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    speed_for_prices = [vsta.analtical.vanilla_put_speed(p, liq_price, T, t, risk_free_rate, 5 * (31/365)) for p in price_range]
    ax.plot(price_range, speed_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Speed vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Speed')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    vega_for_prices = [vsta.analtical.vanilla_put_vega(p, liq_price, T, t, risk_free_rate, 5 * (31/365)) for p in price_range]
    ax.plot(price_range, vega_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Vega vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Vega')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


