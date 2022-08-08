import numpy as np
import pandas as pd
from scipy import stats

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


def process_parameters(distribution: str, parameters: list) -> list:
    """Validate the parameters to ensure they are appropriate for the given
    distribution.

    Args:
        distribution (str): Name of probability distribution.
        parameters (list): Parameter values for `distribution`.

    Returns:
        list: Validated parameter list.
    """
    # Remove `parameter2`==None in distributions with single parameter.
    param_list = [param for param in parameters if param is not None]

    if distribution in {"Bernoulli", "Geometric"}:
        # Probability must be in the range [0, 1]
        return param_list if 0 <= param_list[0] <= 1 else [0.5]
    elif distribution in {"Binomial", "Negative Binomial"}:
        # Number of trials must be an integer
        n = round(param_list[0])
        # Probability must be in the range [0, 1]
        probabilty = param_list[1] if 0 <= param_list[1] <= 1 else 0.5
        return [n, probabilty]
    else:
        return param_list


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
        "Mode": stats.mode(data, keepdims=False).mode
    }


def process_random_sample(
    distribution: str, size: int, parameters: list
) -> dict:
    """Generate a sample of the specified probability distribution using the
    given parameters, then compute summary statistics.

    Args:
        distribution (str): Name of probabiltiy distribution.
        size (int): Desired sample size.
        parameters (list): Parameter values for `distribution`.

    Returns:
        dict: Sample as a numpy array, plus parameters applied & summary
        statistics.
    """
    parameters = process_parameters(distribution, parameters)
    sample_data = pd.Series(
        distribution_functions[distribution].rvs(*parameters, size=size),
        name=f"{distribution}-sample",
    )
    return {
        "data": sample_data,
        "parameters": parameters,
        "summary_statistics": get_summary_statistics(sample_data),
    }
