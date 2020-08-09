#  from datetime import datetime
import numpy as np
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
    mode
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
    if len(params) < 2 and not 0 <= params[-1] <= 1:
        return [0.5]
    return params if 0 <= params[-1] <= 1 else params[:-1] + (0.5,)


def get_random_sample(distribution, size, parameters):
    """
    Returns a random sample of size {size} with the given {parameters},
    for the specified {distribution}.
    """
    if distribution in {"Bernoulli", "Geometric"}:
        parameters = parameters[:-1]

    probabilistic_dists = {"Negative Binomial", "Binomial", "Geometric",
                           "Bernoulli"}
    if distribution in probabilistic_dists:
        parameters = validate_prob(parameters)
    try:
        return distributions[distribution].rvs(*parameters, size=size)
    except KeyError as absent_key:
        return f'Distribution {absent_key} not yet included.'


def descriptive_stats(data):
    """
    Returns basic descriptive statistics for the data
    """
    q1, q2, q3 = np.quantile(data, [0.25, 0.5, 0.75])
    stats = {'Count': len(data),
             'Mean': data.mean(),
             'Standard Deviation': data.std(),
             'Minimum': data.min(),
             'Q1': q1,
             'Median': q2,
             'Q3': q3,
             'Maximum': data.max(),
             'Mode': mode(data)[0][0]  # mode is nested in ModeResult class
             }
    return {key: round(value, 4) for key, value in stats.items()}
