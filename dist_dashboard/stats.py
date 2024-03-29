from functools import lru_cache

import numpy as np
import pandas as pd
from scipy import stats


SEED = 12345  # For reproducability

distribution_functions = {
    "Normal": stats.norm,
    "Poisson": stats.poisson,
    "Bernoulli": stats.bernoulli,
    "Uniform": stats.uniform,
    "Geometric": stats.geom,
    "Alpha": stats.alpha,
    "Students t": stats.t,
    "Beta": stats.beta,
    "Chi Squared": stats.chi2,
    "Exponential": stats.expon,
    "F": stats.f,
    "Gamma": stats.gamma,
    "Pareto": stats.pareto,
    "Binomial": stats.binom,
    "Negative Binomial": stats.nbinom,
}


def validate_parameters(distribution: str, parameters: tuple) -> tuple:
    """Check parameters to ensure that they are appropriate for the given
    distribution.

    Args:
        distribution (str): Name of probability distribution.
        parameters (tuple): Parameter values for `distribution`.

    Returns:
        tuple: Validated parameter list.
    """
    # Remove `parameter2`==None in distributions with single parameter.
    param_tuple = tuple(param for param in parameters if param is not None)

    if distribution in {"Bernoulli", "Geometric"}:
        # Probability must be in the range [0, 1]
        return param_tuple if 0 <= param_tuple[0] <= 1 else (0.5,)
    elif distribution in {"Binomial", "Negative Binomial"}:
        # Number of trials must be an integer
        n = round(param_tuple[0])
        # Probability must be in the range [0, 1]
        probabilty = param_tuple[1] if 0 <= param_tuple[1] <= 1 else 0.5
        return (n, probabilty)
    else:
        return param_tuple


def get_summary_statistics(data: pd.Series) -> dict:
    """Compute descriptive statistics for the generated sample.

    Args:
        data (pandas.Series): Sample values.

    Returns:
        dict: Summary statistics.
    """
    q1, q2, q3 = np.quantile(data, [0.25, 0.5, 0.75])
    return {
        "Count": len(data),
        "Mean": data.mean(),
        "Standard Deviation": data.std(),
        "Minimum": data.min(),
        "Q1": q1,
        "Median": q2,
        "Q3": q3,
        "Maximum": data.max(),
        "Mode": stats.mode(data, keepdims=False).mode,
    }


@lru_cache(maxsize=10)
def process_random_sample(
    distribution: str, size: int, parameters: tuple
) -> dict:
    """Generate a sample of the specified probability distribution using the
    given parameters, then compute summary statistics.

    Args:
        distribution (str): Name of probabiltiy distribution.
        size (int): Desired sample size.
        parameters (tuple): Parameter values for `distribution`.

    Returns:
        dict: Sample as a numpy array, plus parameters applied & summary
        statistics.
    """
    parameters = validate_parameters(distribution, parameters)
    sample_data = pd.Series(
        distribution_functions[distribution].rvs(
            *parameters, size=size, random_state=SEED
        ),
        name=f"{distribution}-sample",
    )
    return {
        "data": sample_data,
        "parameters": parameters,
        "summary_statistics": get_summary_statistics(sample_data),
    }
