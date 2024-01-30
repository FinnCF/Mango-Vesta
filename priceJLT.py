from vesta.main import Vesta
from vesta.constants import tokens
from web3 import Web3
from vesta.token import Token
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from vesta.pricing.optimisers import Optimisers

# Days looking behind for calibration of paths


# Instantiate the web3 researc provider with etherscan and infura
vsta = Vesta(web3_provider=Web3.HTTPProvider(''), etherscan_api_key_token='', moralis_api_key='')
JLP = Token(**tokens.get("JLP"))

# Hourly data of 31 previous days
data = vsta.data.coingecko.get_historical_market_data(JLP, 31)
data['lret'] = np.log(data['price'] / data['price'].shift(1))
obs = data['price'].values
mean_log_return = np.nanmean(data['lret'])  # Handle NaN values
std_log_return = np.nanstd(data['lret'])  # Standard deviation for volatility

initial_params = [
    0.05 / 31,         # mu_s
    std_log_return * 3,  # sigma_s
    0.03,              # Increased mu_j for larger jumps
    0.0001,              # Increased sigma_j for more variability in jump sizes
    0.05             # Decreased lambda_j for rarer jumps
] 

bounds = [
    (-0.01, 0.01),   # Bounds for mu_s
    (0, 0.03),       # Bounds for sigma_s
    (-0.2, 0.3),     # Bounds for mu_j
    (0, 0.05),        # Bounds for sigma_j
    (0, 0.1)           # Bounds for lambda_j
]

result = minimize(vsta.optimisers.least_squares_obj, initial_params, args=(vsta.processes.merton_jump_diffusion_paths, 1, 31, 718, obs[0], obs), method='L-BFGS-B', bounds=bounds)
print(result.x)

path_df_final = vsta.processes.merton_jump_diffusion_paths(*result.x, 10, 31, 718, obs[0])

# Expected, mean and sample path
plt.figure(1)
plt.plot(path_df_final)
plt.plot(obs)
plt.xlabel('t')
plt.ylabel('X')
plt.title('Paths of a Merton jump-diffusion process')
plt.show()



