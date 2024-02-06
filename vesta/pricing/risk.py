from typing import Optional, List
import numpy as np
import pandas as pd
import logging
from scipy.stats import norm
from typing import Optional, List
import numpy as np
import pandas as pd
import logging
from scipy.stats import norm

class Risk:

    @staticmethod
    def calculate_current_values(vsta, price, T, t, risk_free_rate, sigma, init_asset_weight, maint_asset_weight, init_liab_weight, maint_liab_weight, deposit_limit, slippage, supply):
        """
        Calculate and return current values for given parameters.
        """
        leverage = 1 / (1 - init_asset_weight)
        leverage = 1 / (1 - init_asset_weight)
        liq_price = (price * init_asset_weight) / maint_asset_weight
        price_drop = 100 * ((liq_price - price) / price)
        perc_of_mktcp = 100 * (deposit_limit / (supply * price))
        quantity = deposit_limit / price

        free_collateral_value = deposit_limit * init_asset_weight
        borrowed_value = (free_collateral_value / (1 - init_asset_weight)) / init_liab_weight
        weighted_borrowed_value = borrowed_value * maint_liab_weight
        borrowed_quantity = borrowed_value / price

        shortfall_value = borrowed_quantity * (slippage / 100)
        shortfall_quantity = shortfall_value / price

        current_value = vsta.analytical.binary_put_price(price, liq_price, T, t, risk_free_rate, sigma, 1)
        current_delta = vsta.analytical.binary_put_delta(price, liq_price, T, t, risk_free_rate, sigma)
        current_gamma = vsta.analytical.binary_put_gamma(price, liq_price, T, t, risk_free_rate, sigma)
        current_theta = vsta.analytical.binary_put_theta(price, liq_price, T, t, risk_free_rate, sigma)
        current_speed = vsta.analytical.binary_put_speed(price, liq_price, T, t, risk_free_rate, sigma)
        current_vega = vsta.analytical.binary_put_vega(price, liq_price, T, t, risk_free_rate, sigma)
        current_exposure = vsta.analytical.binary_put_price(price, liq_price, T, t, risk_free_rate, sigma, shortfall_value)
        current_short_positions = current_delta * shortfall_value

        return pd.DataFrame({
            'Underlying (collateral price)': [price],
            'Put value': [current_value],
            'Delta': [current_delta],
            'Gamma': [current_gamma],
            'Vega': [current_vega],
            'Theta': [current_theta],
            'Speed': [current_speed],
            'Initial Asset Weight': [init_asset_weight],
            'Maintenance Asset Weight': [maint_asset_weight],
            'Leverage': [leverage],
            'Liquidation Price': [liq_price],
            'Liqudidation Price Drop (%)': [price_drop],
            'Deposit Limit': [deposit_limit],
            'Percent of Market Cap': [perc_of_mktcp],
            'Slippage %': [slippage],
            'Insurance Fund Risk (Slippage)': [shortfall_value],
            'Exposure': [current_exposure],
            'Short Hedge Required': [current_short_positions]
        })
