import numpy as np
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


def process_parameters(distribution, parameters):
    """Validate the parameters to ensure they are appropriate for the given
    distribution.

    Parameters
    ----------
    distribution : str
        The name of the probability distribution.
    parameters : list
        A list of parameter values for the distribution.

    Returns
    -------
    A list of valid parameter values.
    """
    # The default value for parameter2 in distributions having no second
    # parameter is `None`.
    param_list = [param for param in parameters if param is not None]

    if distribution in {"Bernoulli", "Geometric"}:
        # These have only one parameter - probability
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


def get_summary_statistics(data):
    """Get basic descriptive statistics.

    Parameters
    ----------
    data : array-like
        An array of numerical values.

    Returns
    -------
    A dictionary of various summary statistics.
    """
    q1, q2, q3 = np.quantile(data, [0.25, 0.5, 0.75])
    summary_stats = {
        "Count": len(data),
        "Mean": data.mean(),
        "Standard Deviation": data.std(),
        "Minimum": data.min(),
        "Q1": q1,
        "Median": q2,
        "Q3": q3,
        "Maximum": data.max(),
        "Mode": stats.mode(data)[0][0],  # mode is nested in ModeResult
    }
    return {key: round(value, 4) for key, value in summary_stats.items()}


def process_random_sample(distribution, size, parameters):
    """Generate a sample of the specified probability distribution using the
    given parameters, then compute summary statistics.

    Parameters
    ----------
    distribution : str
        The name of the distribution.
    size : int
        The desired sample size.
    parameters : list
        A list of parameter values

    Returns
    -------
    A random sample of the specified probability distribution as a numpy array,
    plus the parameters applied, and summary statistics.
    """
    # Validate parameters
    parameters = process_parameters(distribution, parameters)
    # Get a random sample
    sample = distribution_functions[distribution].rvs(*parameters, size=size)

    return {
        "data": sample,
        "parameters": parameters,
        "summary_statistics": get_summary_statistics(sample),
    }
