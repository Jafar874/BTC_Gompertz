import numpy as np
from scipy.optimize import curve_fit
from utils import *

if __name__ == "__main__":
    days_since_inception, price_log10, _ = get_data('./data/btc-usd-max.csv')
    best_loss = np.inf
    best_params = None
    n_iterations = 1000
    bounds = [[0, 0], [np.inf, np.inf]]
    model_log10 = log10_transform(model)

    for i in range(n_iterations):
        initial_guess = [
            np.random.uniform(0, 100),
            np.random.rand(),
        ]

        try:
            # Fit the model to the data
            params, covariance = curve_fit(model_log10, days_since_inception, price_log10, p0=initial_guess, bounds=bounds, maxfev=int(1e6))
        
            # Calculate the residuals and the loss (sum of squared residuals)
            residuals = price_log10 - model_log10(days_since_inception, *params)
            loss = np.sum(residuals**2)

            # Check if this fit is better (lower loss) than the previous best
            if loss < best_loss:
                best_loss = loss
                best_params = params
        except Exception as e:
            # In case curve_fit fails (e.g., due to invalid initial guesses)
            print(f"Error fitting with initial guess {initial_guess}: {e}")

    # Output the best parameters and the corresponding loss
    if best_params is not None:
        b, c = best_params
        print(f'Best fitted parameters: b={b}, c={c}')
    else:
        print("No valid fit found.")
