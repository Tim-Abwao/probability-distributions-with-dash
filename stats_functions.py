#  from datetime import datetime
from statistics import median, mode
from scipy.stats import (
    norm,
    poisson,
    bernoulli,
    uniform,
    geom,
    alpha,
    t,
    beta,
    chi2,
    expon,
    f,
    gamma,
    pareto,
    binom,
    nbinom,
)

distributions = {
    "Normal": norm,
    "Poisson": poisson,
    "Bernoulli": bernoulli,
    "Uniform": uniform,
    "Geometric": geom,
    "Alpha": alpha,
    "Beta": beta,
    "Chi-squared": chi2,
    "Exponential": expon,
    "F": f,
    "Gamma": gamma,
    "Pareto": pareto,
    "Student's t": t,
    "Binomial": binom,
    "Negative Binomial":  nbinom
}


def validate_prob(params):
    """
    Ensures that probabilities are in the range 0 <= p <= 1, or else assigns
    a default value of 0.5 to p. Probability (p) is the last value (index -1)
    """
    return params if 0 <= params[-1] <= 1 else params[:-1] + (0.5,)


def get_random_sample(distribution, size, parameters):
    """
    Returns a random sample of size {size} with the given {parameters},
    for the specified {distribution}.
    """
    params = [param for param in parameters if param != 'N/A']

    probabilistic_dists = {"Negative Binomial", "Binomial", "Geometric",
                           "Bernoulli"}

    if distribution in probabilistic_dists:
        params = validate_prob(params)

    try:
        return distributions[distribution].rvs(*params, size=size)
    except KeyError:
        return 1


def descriptive_stats(data):
    """
    Returns basic descriptive statistics for the data
    """
    stats = {'Count': len(data),
             'Mean': data.mean(),
             'Median': median(data),
             'Standard Deviation': data.std(),
             'Minimum': data.min(),
             'Maximum': data.max()
             }
    try:
        stats['Mode'] = mode(data)
    except ValueError:
        stats['Mode'] = "No unique mode."

    return stats
