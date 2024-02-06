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
                    borrowed_quantity = borrowed_value / price

                    # Insurance fund exposure (payoff of binary)
                    shortfall_value = borrowed_quantity * (slippage / 100) 
                    shortfall_quantity = shortfall_value / price

                    # Current greeks (t=0, now)
                    current_value = vsta.analtical.binary_put_price(price, liq_price, T, t, risk_free_rate, sigma, 1)
                    current_delta = vsta.analtical.binary_put_delta(price, liq_price, T, 0, risk_free_rate, sigma)
                    current_gamma = vsta.analtical.binary_put_gamma(price, liq_price, T, 0, risk_free_rate, sigma)
                    current_theta = vsta.analtical.binary_put_theta(price, liq_price, T, 0, risk_free_rate, sigma)
                    current_speed = vsta.analtical.binary_put_speed(price, liq_price, T, 0, risk_free_rate, sigma)
                    current_vega = vsta.analtical.binary_put_vega(price, liq_price, T, 0, risk_free_rate, sigma)
                    current_exposure = vsta.analtical.binary_put_price(price, liq_price, T, 0, risk_free_rate, sigma, shortfall_value)
                    current_short_positions = current_delta * shortfall_value

                    # Create and print the Summary of Current Exposure and Risks table for the setting
                    current_risks_df = pd.DataFrame({
                        'Underlying': [price],
                        'Value': [current_value],
                        'Delta': [current_delta],
                        'Gamma': [current_gamma],
                        'Vega': [current_vega],
                        'Theta': [current_theta],
                        'Speed': [current_speed],
                        'Initial Weight': [init_weight],
                        'Maintenance Weight': [maint_weight],
                        'Leverage': [leverage],
                        'Liquidation Price': [liq_price],
                        'Required Price Drop (%)': [price_drop],
                        'Deposit Limit': [deposit_limit],
                        'Slippage': [slippage],
                        'Slippage Insurance Fund Risk': [shortfall_value],
                        'Exposure': [current_exposure],
                        'Short Hedge Required': [current_short_positions]
                    }, index=[0])  # Adding index=[0] to create a single row DataFrame
                    transposed_risks_df = current_risks_df.T
                    transposed_risks_df.columns = ['']

                    # Print the transposed DataFrame
                    print(f"Summary of Current Exposure and Risks for Setting - Init: {init_weight}, Maint: {maint_weight}, Limit: {deposit_limit}, Slippage: {slippage}:")
                    print(transposed_risks_df)


price_range = np.linspace(0.1, price * 2, 500)  
time_periods_for_plot = np.linspace(0, 1, 20)

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    values = [vsta.analtical.binary_put_price(p, liq_price, T, t, risk_free_rate, sigma, shortfall_value) for p in price_range]
    ax.plot(price_range, values, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Value for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Value')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    deltas_for_prices = [vsta.analtical.binary_put_delta(p, liq_price, T, t, risk_free_rate, sigma) for p in price_range]
    ax.plot(price_range, deltas_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Delta vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Delta')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    gammas_for_prices = [vsta.analtical.binary_put_gamma(p, liq_price, T, t, risk_free_rate, sigma) for p in price_range]
    ax.plot(price_range, gammas_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Gamma vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Gamma')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    thetas_for_prices = [vsta.analtical.binary_put_theta(p, liq_price, T, t, risk_free_rate, sigma) for p in price_range]
    ax.plot(price_range, thetas_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Theta vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Theta')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    speed_for_prices = [vsta.analtical.binary_put_speed(p, liq_price, T, t, risk_free_rate, sigma) for p in price_range]
    ax.plot(price_range, speed_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Speed vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Speed')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
for t in time_periods_for_plot:
    vega_for_prices = [vsta.analtical.binary_put_vega(p, liq_price, T, t, risk_free_rate, sigma) for p in price_range]
    ax.plot(price_range, vega_for_prices, label=f'Time to Expiry: {T-t} Years')
ax.set_title('Vega vs. Price for Different Time Periods to Expiry')
ax.set_xlabel('Price')
ax.set_ylabel('Vega')
ax.legend(title='Time Periods', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

