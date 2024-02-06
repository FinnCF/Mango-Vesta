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

# Instantiate the web3 researc provider with etherscan and infura
vsta = Vesta(web3_provider=Web3.HTTPProvider(''), etherscan_api_key_token='', moralis_api_key='')
JLP = Token(**tokens.get("JLP"))

# Hourly data of 31 previous days (1 month)
data = vsta.data.coingecko.get_historical_market_data(JLP, 31)
obs = data['price'].values
price = obs[-1]
supply = 46_026_812.892
risk_free_rate = 0.05

# Monte carlo parameters
time_steps = 718
time_limit = 1
monte_carlo_params = {
    "muS": 0.11,         # mu_s 11% a month approx atm. 
    "sigmaS": 5 * (31/365), # sigma_s
    "muJ": 0,            # Increased mu_j for larger jumps
    "sigmaJ": 0.05,      # Increased sigma_j for more variability in jump sizes
    "lambdaJ": 0.5,      # Decreased lambda_j for rarer jumps
    "npaths": 50000,     # Number paths
    "T": 1,              # Time limit
    "nsteps": 718        # Hours division, total timesteps
}

# Monte Carlo Price
total_paths = 10000
# Monte Carlo Price Calculation using parameter unpacking
perturbation = 0.01
paths_asset = vsta.processes.merton_jump_diffusion_paths(
    **monte_carlo_params,  # Unpacks all the parameters from the dictionary
    S0=price           # 'price' is still passed separately
)

final_values_asset = paths_asset.iloc[-1].values

# Liabiiliy simulation for USDC (contstant but used later)
paths_liab = vsta.processes.merton_jump_diffusion_paths(
    0,         
    0,  
    0,         
    0,          
    0, 
    1, 
    1, 
    718, 
    1 
    )
final_values_liab = paths_asset.iloc[-1].values

# Parameter settings estimation
settings = []
init_asset_weights = [0.66]
init_liab_weight = 1
maint_asset_weights = [0.75]
maint_liab_weight = 1
deposit_limits_and_slippages = [{250_000: 0.11}, {500_000: 0.29}, {750_000: 0.88}, {1_000_000: 1.16}, {2_000_000: 2.33}, {5_000_000: 5.83}]

for init_weight in init_asset_weights:
    for maint_weight in maint_asset_weights:
        if(maint_weight > init_weight):   

            # Leverage, Liquidation price, Price drop required to achieve it, Probability of liquidation at current number of paths,
            leverage = 1 / (1 - init_weight)
            liq_price = (price * init_weight) / maint_weight
            price_drop = 100 * ((liq_price - price) / price)
            num_paths_below_liquidation = np.sum(paths_asset.iloc[-1, :] < liq_price)
            prob_liq = 100 * num_paths_below_liquidation / total_paths

            for deposit_slippage in deposit_limits_and_slippages:
                for deposit_limit, slippage in deposit_slippage.items():
                    
                    # Calculating percentage of market cap.
                    perc_of_mktcp = 100 * (deposit_limit / (supply * price))
                    quantity = deposit_limit / price

                    # Borrows calculation.
                    free_collateral_value = deposit_limit * init_weight
                    borrowed_value = (free_collateral_value / (1 - init_weight)) / init_liab_weight 
                    borrowed_value_weighted = borrowed_value * maint_liab_weight

                    # Collaterals Calculation
                    collateral_value =  ((quantity * paths_asset) / (1 - init_weight))
                    collateral_value_weighted = maint_weight * collateral_value
                    collateral_value_weighted_up = collateral_value_weighted * (1 + perturbation)
                    collateral_value_weighted_down = collateral_value_weighted * (1 - perturbation)
                    starting_collateral_value = collateral_value.iloc[0].values[0]
                    starting_collateral_value_weighted = maint_weight * starting_collateral_value 

                    # Insurance fund exposure
                    shortfall_value = borrowed_value_weighted * (slippage / 100) 

                    # Payoff, Delta hedge calculation. 
                    calculated_values = []
                    deltas = []
                    for time_step in range(len(paths_asset)):

                        time_to_expiry = (time_steps - time_step)
                        current_collateral_value_weighted = collateral_value_weighted.iloc[time_step]
                        current_collateral_value_weighted_up = collateral_value_weighted_up.iloc[time_step]
                        current_collateral_value_weighted_down = collateral_value_weighted_down.iloc[time_step]
                        
                        # Calculations of payoffs     
                        payoffs = np.where(current_collateral_value_weighted < borrowed_value_weighted, shortfall_value, 0)
                        average_payoff = np.mean(payoffs)
                        value = np.exp(-0.05*(31/365)*time_to_expiry) * average_payoff
                        calculated_values.append(value)

                        # Delta calculation using central estimation
                        # Perturb the underlying asset price up and down
                        current_collateral_value_weighted_up = current_collateral_value_weighted * (1 + perturbation)
                        current_collateral_value_weighted_down = current_collateral_value_weighted * (1 - perturbation)
                        payoffs_up = np.where(current_collateral_value_weighted_up < borrowed_value_weighted, shortfall_value, 0)
                        payoffs_down = np.where(current_collateral_value_weighted_down < borrowed_value_weighted, shortfall_value, 0)
                        average_payoff_up = np.mean(payoffs_up)
                        average_payoff_down = np.mean(payoffs_down)
                        value_up = np.exp(-0.05 * (31 / 365) * time_to_expiry) * average_payoff_up
                        value_down = np.exp(-0.05 * (31 / 365) * time_to_expiry) * average_payoff_down

                        # Calculate delta for this time step
                        delta = (value_up - value_down) / (price * 2 * perturbation)
                        deltas.append(delta)

                    paths_asset[f'Delta{deposit_limit}_{init_weight}_{maint_weight}'] = deltas

paths_asset['calculated_values'] = calculated_values
print(paths_asset)

plt.figure(1)
plt.plot(paths_asset['calculated_values'])
plt.xlabel('Hours in the future)', fontsize=18)
plt.ylabel('Value of JLP', fontsize = 18)
plt.title('Simulated Paths', fontsize = 18)
plt.show()

plt.figure(1)
plt.plot(paths_asset['Delta'])
plt.xlabel('Hours in the future)', fontsize=18)
plt.ylabel('Value of JLP', fontsize = 18)
plt.title('Simulated Paths', fontsize = 18)
plt.show()
        
df = pd.DataFrame(settings)

# Creating a dictionary of DataFrames for each combination of maint/init weight
tables = {}
for maint_asset_weight in maint_asset_weights:
    for init_asset_weight in init_asset_weights:
        if(maint_asset_weight > init_asset_weight):
            filtered_df = df[(df['maint'] == maint_asset_weight) & (df['init'] == init_asset_weight)]
            if not filtered_df.empty:
                key = f"Maint_{maint_weight}_Init_{init_weight}"
                leverage = filtered_df['Lev'].values[0]
                liq_price = filtered_df['LiqPrice'].values[0]
                perc_drop = filtered_df['PercDrop'].values[0]
                prob_liq = filtered_df['ProbLiq'].values[0]
                filtered_df = filtered_df.drop(['init', 'maint', 'Lev', 'LiqPrice', 'PercDrop', 'ProbLiq'], axis=1)

# Expected, mean and sample path
plt.figure(1)
plt.plot(paths_asset.sample(n=250, axis=1))
plt.xlabel('Hours in the future)', fontsize=18)
plt.ylabel('Value of JLP', fontsize = 18)
plt.title('Simulated Paths', fontsize = 18)
plt.show()

# KDE, Histogram, etc for the final values
kde = gaussian_kde(final_values_asset)
x_kde = np.linspace(min(final_values_asset), max(final_values_asset), 100)
density_kde = kde(x_kde)
plt.figure(figsize=(12, 8))
plt.plot(x_kde, density_kde, color='red', linewidth=2, label='KDE')
plt.hist(final_values_asset, bins=150, label='Histogram', color='lightgrey', density=True, alpha=0.7)
plt.axvline(x=price, color='blue', linestyle='--', linewidth=2, label='Current Price')
for i, setting in enumerate(settings):
    plt.axvline(x=setting['LiqPrice'], color='black', linestyle='-', linewidth=1.5)
    plt.text(setting['LiqPrice'], plt.ylim()[1]*0.5, f"Liquidation at Price {setting['LiqPrice']} Init:{setting['init']}, Maint:{setting['maint']}, Prob:{setting['ProbLiq']}%, Drop: {setting['PercDrop']}%", 
             ha='right', va='center', fontsize=14, rotation=90, color='black')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlabel('Value of JLP', fontsize=18)
plt.ylabel('Density', fontsize=18)
plt.title('Conservative Final Values of JLP After 1 Month\n(Merton Jump-Diffusion Process)', fontsize=18)
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

