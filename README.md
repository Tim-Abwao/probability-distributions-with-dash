# Statistical Distributions Dashboard

A simple web app to help explore some of the most common statistical distributions. Made with [SciPy][1], powered by [Dash][2].

You can [try it out here][3].

[![screen capture](screen.gif)][3]

To run it locally,

1. Download the files, and create a virtual environment:

    ```bash
    git clone https://github.com/Tim-Abwao/statistical-distributions-dash.git
    cd statistical-distributions-dash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the required packages, and launch the app:

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    gunicorn stats_app:server
    ```

    For *Windows* users, consider using [waitress][4] instead:

    ```bash
    pip install waitress
    waitress-serve stats_app:server
    ```

[1]: https://www.scipy.org/
[2]: https://dash.plotly.com/
[3]: https://statistics-distributions.herokuapp.com/
[4]: https://docs.pylonsproject.org/projects/waitress/en/stable/
