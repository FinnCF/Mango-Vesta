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

class Analytical:

    @staticmethod
    def _d1(S, K, T, t, r, sigma):
        remaining_time = T - t
        if remaining_time > 0:
            return (np.log(S / K) + (r + 0.5 * sigma**2) * remaining_time) / (sigma * np.sqrt(remaining_time))
        else:
            return None

    @staticmethod
    def _d2(d1, sigma, remaining_time):
        if d1 is not None and remaining_time > 0:
            return d1 - sigma * np.sqrt(remaining_time)
        else:
            return None

    @staticmethod
    def binary_call_price(S, K, T, t, r, sigma, payoff):
        remaining_time = T - t
        d1 = Analytical._d1(S, K, T, t, r, sigma)
        d2 = Analytical._d2(d1, sigma, remaining_time)

        if d2 is not None:
            return payoff * np.exp(-r * remaining_time) * norm.cdf(d2)
        else:
            return 0

    @staticmethod
    def binary_put_price(S, K, T, t, r, sigma, payoff):
        remaining_time = T - t
        if remaining_time > 0:
            d1 = Analytical._d1(S, K, T, t, r, sigma)
            d2 = Analytical._d2(d1, sigma, remaining_time)

            if d2 is not None:
                return payoff * np.exp(-r * remaining_time) * (1 - norm.cdf(d2))
            else:
                return 0
        else:
            # At expiry, return the intrinsic value of the binary put option
            return payoff if S < K else 0

    @staticmethod
    def binary_put_delta(S, K, T, t, r, sigma):
        remaining_time = T - t
        d1 = Analytical._d1(S, K, T, t, r, sigma)
        d2 = Analytical._d2(d1, sigma, remaining_time)

        if d2 is not None:
            numerator = - (np.exp(-r * remaining_time) * norm.pdf(d2))
            denom = sigma * S * np.sqrt(remaining_time)
            return numerator / denom
        else:
            return 0

    @staticmethod
    def binary_put_gamma(S, K, T, t, r, sigma):
        remaining_time = T - t
        d1 = Analytical._d1(S, K, T, t, r, sigma)
        d2 = Analytical._d2(d1, sigma, remaining_time)

        if d1 is not None and d2 is not None:
            gamma = -np.exp(-r * remaining_time) * norm.pdf(d2) * (d1 / (S**2 * sigma**2 * remaining_time))
            return gamma
        else:
            return 0

    @staticmethod
    def binary_put_theta(S, K, T, t, r, sigma):
        remaining_time = T - t
        d1 = Analytical._d1(S, K, T, t, r, sigma)
        d2 = Analytical._d2(d1, sigma, remaining_time)

        if d1 is not None and d2 is not None:
            numerator1 = r * np.exp(-r * remaining_time) * (1 - norm.cdf(d2))
            numerator2 = - np.exp(-r * remaining_time) * norm.pdf(d2) * (d1 / (2 * remaining_time)) 
            numerator3 = - (r + (sigma**2 / 2)) / sigma
            return numerator1 + numerator2 * numerator3
        else:
            return 0

    @staticmethod
    def binary_put_speed(S, K, T, t, r, sigma):
        remaining_time = T - t
        d1 = Analytical._d1(S, K, T, t, r, sigma)
        d2 = Analytical._d2(d1, sigma, remaining_time)

        if d1 is not None and d2 is not None:
            numerator1 = np.exp(-r * remaining_time) * norm.pdf(d2)
            numerator2 = - 2 * d1 + (1 - d1 * d2) / (sigma * remaining_time)
            denom1 = (sigma ** 2) * (S **3) * remaining_time
            return (numerator1 * numerator2) / denom1
        else:
            return 0

    @staticmethod
    def binary_put_vega(S, K, T, t, r, sigma):
        remaining_time = T - t
        d1 = Analytical._d1(S, K, T, t, r, sigma)
        d2 = Analytical._d2(d1, sigma, remaining_time)

        if d2 is not None:
            return np.exp(-r * remaining_time) * norm.pdf(d2) * (np.sqrt(remaining_time) + (d2 / sigma))
        else:
            return 0

    @staticmethod
    def vanilla_put_price(S, K, T, t, r, sigma):
        remaining_time = T - t
        d1 = Analytical._d1(S, K, T, t, r, sigma)
        d2 = Analytical._d2(d1, sigma, remaining_time)

        if d1 is not None and d2 is not None:
            return K * np.exp(-r * remaining_time) * norm.cdf(-d2) - S * norm.cdf(-d1)
        else:
            return 0

    @staticmethod
    def vanilla_put_delta(S, K, T, t, r, sigma):
        remaining_time = T - t
        d1 = Analytical._d1(S, K, T, t, r, sigma)
        if d1 is not None:
            return norm.cdf(d1) - 1
        else:
            return 0

    @staticmethod
    def vanilla_put_gamma(S, K, T, t, r, sigma):
        remaining_time = T - t
        d1 = Analytical._d1(S, K, T, t, r, sigma)
        if d1 is not None:
            return norm.pdf(d1) / (S * sigma * np.sqrt(remaining_time))
        else:
            return 0

    @staticmethod
    def vanilla_put_theta(S, K, T, t, r, sigma):
        remaining_time = T - t
        d1 = Analytical._d1(S, K, T, t, r, sigma)
        d2 = Analytical._d2(d1, sigma, remaining_time)

        if d1 is not None and d2 is not None:
            first_term = S * sigma * norm.pdf(d1) / (2 * np.sqrt(remaining_time))
            second_term = r * K * np.exp(-r * remaining_time) * norm.cdf(-d2)
            return -first_term - second_term
        else:
            return 0

    @staticmethod
    def vanilla_put_speed(S, K, T, t, r, sigma):
        remaining_time = T - t
        d1 = Analytical._d1(S, K, T, t, r, sigma)
        if d1 is not None:
            return -norm.pdf(d1) / (S**2 * sigma * np.sqrt(remaining_time)) * (d1 / (S * sigma * np.sqrt(remaining_time)) + 1)
        else:
            return 0

    @staticmethod
    def vanilla_put_vega(S, K, T, t, r, sigma):
        remaining_time = T - t
        d1 = Analytical._d1(S, K, T, t, r, sigma)
        if d1 is not None:
            return S * np.sqrt(remaining_time) * norm.pdf(d1)
        else:
            return 0
