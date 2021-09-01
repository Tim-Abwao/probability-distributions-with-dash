# Probability Distribution Sampler

A dashboard to help explore some of the most common probability distributions. Powered by [Dash][1].

You can [try it out here][2].

[![screen capture](screen.gif)][2]

## Run locally

1. Download the files, and create a virtual environment:

    ```bash
    git clone https://github.com/Tim-Abwao/probability-distributions-with-dash.git
    cd probability-distributions-with-dash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the required packages, and launch the app:

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    waitress-serve distributions_dashboard:server
    ```

[1]: https://dash.plotly.com/
[2]: https://probability-distributions.herokuapp.com/
