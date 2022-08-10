# Probability Distribution Sampler

A dashboard to help explore some of the most common probability distributions. Powered by [Dash][dash] & [SciPy][scipy].

You can [try it out here][app-link].

[![screen capture](screencast.gif)][app-link]

## Running locally

1. Download the files, and create a virtual environment:

    ```bash
    git clone https://github.com/Tim-Abwao/probability-distributions-with-dash.git
    cd probability-distributions-with-dash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the required packages, and launch the app:

    ```bash
    pip install -U pip
    pip install -r requirements.txt
    waitress-serve dist_dashboard:server
    ```

[dash]: https://dash.plotly.com/
[scipy]: https://scipy.org/
[app-link]: https://probability-distributions.herokuapp.com/
