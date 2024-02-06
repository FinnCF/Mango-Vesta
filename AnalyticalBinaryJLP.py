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
price = 2
supply = 46_026_812.892
risk_free_rate = 0.05

# Parameters
time_steps = 718
T = 1 #Denoting a month (Average DeFi loan length)
t = 0
sigma = 5 * (31/365)

# Parameter settings estimation
init_asset_weights = [0.66, 0.75]
init_liab_weight = 1
maint_asset_weights = [0.75, 0.9]
maint_liab_weight = 1
deposit_limits_and_slippages = [{750_000: 0.88}, {1_000_000: 1.16}, {2_000_000: 2.33}, {5_000_000: 5.83}]
remaining_time_values = np.linspace(T - t, 0, 718)  # From T-t to 0

# Instantiate the web3 research provider with etherscan and infura
vsta = Vesta(web3_provider=Web3.HTTPProvider(''), etherscan_api_key_token='', moralis_api_key='')
JLP = Token(**tokens.get("JLP"))

# Parameters
price = 2
supply = 46_026_812.892
risk_free_rate = 0.05
time_steps = 718
T = 1  # Denoting a month (Average DeFi loan length)
t = 0 # starting from 0 (now)
sigma = 5 * (31/365) # Sigma as 40% monthly (conservative)

init_asset_weights = [0.66, 0.75]
init_liab_weight = 1
maint_asset_weights = [0.75, 0.9]
maint_liab_weight = 1
deposit_limits_and_slippages = [{750_000: 0.88}, {1_000_000: 1.16}, {2_000_000: 2.33}, {5_000_000: 5.83}]

# Loop to calculate and print the summary for each setting
master_df = pd.DataFrame()
for init_weight in init_asset_weights:
    for maint_weight in maint_asset_weights:
        if maint_weight > init_weight: # If maint = init then loan is initialised on liqudation price (unfortunate...)
            for deposit_slippage in deposit_limits_and_slippages:
                for deposit_limit, slippage in deposit_slippage.items():
                    current_risks_df = vsta.risk.calculate_current_values(vsta, price, T, t, risk_free_rate, sigma, init_weight, maint_weight, 1, 1, deposit_limit, slippage, supply)
                    print('--------------')
                    print(f"Summary of Current Exposure and Risks for Setting - Init: {init_weight}, Maint: {maint_weight}, Limit: {deposit_limit}, Slippage: {slippage}:")
                    print(current_risks_df)
                    master_df = pd.concat([master_df, current_risks_df], ignore_index=True)
master_df.to_csv('new.csv')

# Observing nature of the put option.
price_range = np.linspace(0.1, price * 2, 500)  
time_periods_for_plot = np.linspace(0.01, 1, 20)
fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    liq_price = liq_price = (price * init_asset_weights[0]) / maint_asset_weights[0]
    values = [vsta.analytical.binary_put_price(p, liq_price, T, t, risk_free_rate, sigma, 1) for p in price_range]
    ax.plot(price_range, values, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Value for Different Time Periods against Price')
ax.set_xlabel('Price')
ax.set_ylabel('Value')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    liq_price = liq_price = (price * init_asset_weights[0]) / maint_asset_weights[0]
    deltas_for_prices = [vsta.analytical.binary_put_delta(p, liq_price, T, t, risk_free_rate, sigma) for p in price_range]
    ax.plot(price_range, deltas_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Delta vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Delta')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    liq_price = liq_price = (price * init_asset_weights[0]) / maint_asset_weights[0]
    gammas_for_prices = [vsta.analytical.binary_put_gamma(p, liq_price, T, t, risk_free_rate, sigma) for p in price_range]
    ax.plot(price_range, gammas_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Gamma vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Gamma')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    liq_price = liq_price = (price * init_asset_weights[0]) / maint_asset_weights[0]
    thetas_for_prices = [vsta.analytical.binary_put_theta(p, liq_price, T, t, risk_free_rate, sigma) for p in price_range]
    ax.plot(price_range, thetas_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Theta vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Theta')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    liq_price = liq_price = (price * init_asset_weights[0]) / maint_asset_weights[0]
    speed_for_prices = [vsta.analytical.binary_put_speed(p, liq_price, T, t, risk_free_rate, sigma) for p in price_range]
    ax.plot(price_range, speed_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Speed vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Speed')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    liq_price = liq_price = (price * init_asset_weights[0]) / maint_asset_weights[0]
    vega_for_prices = [vsta.analytical.binary_put_vega(p, liq_price, T, t, risk_free_rate, sigma) for p in price_range]
    ax.plot(price_range, vega_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Vega vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Vega')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
