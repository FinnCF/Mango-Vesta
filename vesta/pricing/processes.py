from typing import Optional, List
import numpy as np
import pandas as pd
import logging

class Processes:
    """
    A class representing static methods of all different stochastic processes.
    Each process returns a list of arrays of values. 
    """

    @staticmethod
    def merton_jump_diffusion_paths(muS: float, sigmaS: float, muJ: float, sigmaJ: float, lambdaJ: float, npaths: int, T: float, nsteps: int, S0: float, ) -> Optional[pd.DataFrame]:
        """
        Generates paths for the Merton jump-diffusion model.

        Parameters:
        npaths (int): Number of paths to generate.
        T (float): Time horizon.
        nsteps (int): Number of steps in the time horizon.
        muS (float): Expected return of the security over period.
        sigmaS (float): Volatility of the security over T.
        muJ (float): Mean of the jump size.
        sigmaJ (float): Volatility of the jump size.
        lambdaJ (float): Intensity of the jump (expected number of jumps per unit of time).
        S0 (float): Initial price of the security.

        Returns:
        Optional[List[np.ndarray]]: A list of numpy arrays containing the simulated paths, or None in case of an error.
        """
        try:
            dt = T / nsteps  # time step

            # Computing the increments of the GBM
            dW = (muS - 0.5 * sigmaS**2) * dt + sigmaS * np.sqrt(dt) * np.random.randn(nsteps, npaths)

            # Computing the increments of the Non-Central poisson process. 
            dN = np.random.poisson(lambdaJ * dt, (nsteps, npaths))
            dJ = muJ * dN + sigmaJ * np.sqrt(dN) * np.random.randn(nsteps, npaths)

            # Sum the increments of the GBM and the NCPP
            dX = dW + dJ

            # Accumulate the increments
            L = np.vstack((np.zeros((1, npaths)), np.cumsum(dX, axis=0)))

            # Develop a stock price
            X = S0 * np.exp(L)

            return pd.DataFrame(X)

        except Exception as e:
            logging.error(f"Error computing merton paths: {e}")
            return None
