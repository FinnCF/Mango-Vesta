from typing import Optional, List
import numpy as np
import pandas as pd
import logging
from scipy.stats import norm

class Analytical:

    @staticmethod
    def binary_call_price(S, K, T, t, r, sigma, payoff):
        remaining_time = T - t
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * remaining_time) / (sigma * np.sqrt(remaining_time))
        d2 = d1 - (sigma * np.sqrt(remaining_time))
        return payoff * np.exp(-r * remaining_time) * norm.cdf(d2)
    
    @staticmethod
    def binary_put_price(S, K, T, t, r, sigma, payoff):
        remaining_time = T - t
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * remaining_time) / (sigma * np.sqrt(remaining_time))
        d2 = d1 - (sigma * np.sqrt(remaining_time))
        return payoff * np.exp(-r * remaining_time) * (1 - norm.cdf(d2))
    
    @staticmethod
    def binary_put_delta(S, K, T, t, r, sigma, payoff):
        remaining_time = T - t
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * remaining_time) / (sigma * np.sqrt(remaining_time))
        d2 = d1 - (sigma * np.sqrt(remaining_time))
        numerator = - (np.exp(-r * remaining_time) * norm.pdf(d2))
        denom = sigma * S * np.sqrt(remaining_time)
        return numerator / denom    

    @staticmethod
    def binary_call_delta(S, K, T, t, r, sigma, payoff):
        remaining_time = T - t
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * remaining_time) / (sigma * np.sqrt(remaining_time))
        d2 = d1 - (sigma * np.sqrt(remaining_time))
        numerator = - (np.exp(-r * remaining_time) * norm.pdf(d2))
        denom = sigma * S * np.sqrt(remaining_time)
        return numerator / denom    
    
    @staticmethod
    def binary_put_gamma(S, K, T, t, r, sigma, payoff):
        remaining_time = T - t
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * remaining_time) / (sigma * np.sqrt(remaining_time))
        d2 = d1 - sigma * np.sqrt(remaining_time)
        gamma = -np.exp(-r * remaining_time) * norm.pdf(d2) * (d1 / (S**2 * sigma**2 * remaining_time))
        adjusted_gamma = gamma * payoff
        return adjusted_gamma
    
    @staticmethod
    def binary_call_gamma(S, K, T, t, r, sigma, payoff):
        remaining_time = T - t
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * remaining_time) / (sigma * np.sqrt(remaining_time))
        d2 = d1 - sigma * np.sqrt(remaining_time)
        gamma = np.exp(-r * remaining_time) * norm.pdf(d2) * (d1 / (S**2 * sigma**2 * remaining_time))
        adjusted_gamma = gamma * payoff
        return adjusted_gamma