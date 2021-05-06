import numpy as np
from scipy import stats


distributions = {
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


def get_random_sample(distribution, size, parameters):
    """Generate a sample with the specified probability distribution, using
    the given parameters.

    Parameters
    ----------
    distribution : str
        The name of the distribution
    size : int
        The desired sample size
    parameters : int, float
        Parameter values

    Returns
    -------
    The specified sample as a numpy array.
    """
    parameters = [param for param in parameters if param is not None]

    try:
        # Get a sample with the set parameters
        sample = distributions[distribution].rvs(*parameters, size=size)
    except (ValueError, TypeError):
        # Missing positional args cause a TypeError('_parse_args_rvs() missing
        # 1 required positional argument').
        # Invalid args raise a ValueError('Domain error in arguments').

        # Get a sample with default paramerters
        sample = distributions[distribution].rvs(1, 1, size=size)

    return sample


def summary_stats(data):
    """Get basic descriptive statistics for the given data.

    Parameters
    ----------
    data : array-like
        An array of numerical values.

    Returns
    -------
    A dictionary of various summary statistics.
    """
    q1, q2, q3 = np.quantile(data, [0.25, 0.5, 0.75])
    _stats = {'Count': len(data),
              'Mean': data.mean(),
              'Standard Deviation': data.std(),
              'Minimum': data.min(),
              'Q1': q1,
              'Median': q2,
              'Q3': q3,
              'Maximum': data.max(),
              'Mode': stats.mode(data)[0][0]  # mode is nested in ModeResult
              }
    return {key: round(value, 4) for key, value in _stats.items()}
