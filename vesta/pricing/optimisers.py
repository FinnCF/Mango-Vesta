from typing import Optional, List, Callable
import numpy as np
import pandas as pd
import logging

class Optimisers:
    """
    A class representing static methods of all different stochastic processes.
    Each process returns a list of arrays of values. 
    """

    @staticmethod
    def least_squares_obj(params: List[float], model: Callable, npaths: int, T: float, nsteps: int, S0: float, obs: np.ndarray) -> float:
        """
        Objective function for least squares optimization.

        Parameters:
        params (List[float]): Parameters to optimize.
        model (Callable): Stochastic model to generate paths.
        npaths (int): Number of paths.
        T (float): Time horizon.
        nsteps (int): Number of time steps.
        S0 (float): Initial stock price.
        obs (np.ndarray): Observed data for comparison.

        Returns:
        float: The sum of squared differences between the model output and observed data.
        """
        try:
            path_df = model(*params, npaths, T, nsteps, S0)
            path_vals = path_df.iloc[:, 0].values
            out = np.sum((obs - path_vals) ** 2)
            return out
        except Exception as e:
            logging.error(f"Error in least_squares_obj: {e}")
            # Optionally, you can re-raise the exception if you want it to propagate
            raise