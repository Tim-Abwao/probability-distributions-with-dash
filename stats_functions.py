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


def validate_prob(params):
    """
    Ensure that probabilities are in the range 0 <= p <= 1, or else assign
    a default value of 0.5 to p.
    """
    # Probability (p) is the last value
    if len(params) < 2 and not 0 <= params[-1] <= 1:
        return (0.5,)
    return params if 0 <= params[-1] <= 1 else params[:-1] + (0.5,)


def get_random_sample(distribution, size, parameters):
    """
    Get a sample of the specified distribution with given size and parameters.
    """
    if distribution in {"Bernoulli", "Geometric"}:
        parameters = parameters[:-1]

    if distribution in {"Negative Binomial", "Binomial", "Geometric",
                        "Bernoulli"}:
        parameters = validate_prob(parameters)
    return distributions[distribution].rvs(*parameters, size=size)


def descriptive_stats(data):
    """
    Get basic descriptive statistics for the given data.
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
