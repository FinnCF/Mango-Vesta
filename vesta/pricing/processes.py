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
        

