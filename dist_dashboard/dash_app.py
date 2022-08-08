import json

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

from dist_dashboard import plotting
from dist_dashboard.stats import process_random_sample

with open("dist_dashboard/distributions.json") as file:
    distribution_data = json.load(file)

PARAM_SLIDER_TICKS = [0, 0.5, 1, 2.5, 5, 7.5, 10]
PLOT_CONFIG = {"displayModeBar": False}

app = Dash(
    name="dist_dashboard",
    title="Probability Distributions Sampler",
    external_scripts=["https://cdn.plot.ly/plotly-cartesian-2.6.0.min.js"],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }
    ],
)


app.layout = html.Div(
    [
        html.H1("Probability Distribution Sampler"),
        html.Div(
            className="content",
            children=[
                # Input & descriptions side-bar
                html.Div(
                    className="side-bar",
                    children=[
                        # Distribution selector
                        html.Div(
                            id="distribution-menu",
                            children=[
                                html.Label(
                                    "Select distribution:",
                                    htmlFor="current-distribution",
                                ),
                                dcc.Dropdown(
                                    id="current-distribution",
                                    value="Normal",
                                    clearable=False,
                                    searchable=False,
                                    options=[
                                        {"label": dist, "value": dist}
                                        for dist in distribution_data
                                    ],
                                ),
                            ],
                        ),
                        # Parameter slider(s)
                        html.Div(
                            id="distribution-param-sliders",
                            children=[
                                dcc.Slider(id="parameter1"),
                                dcc.Slider(id="parameter2"),
                            ],
                        ),
                        # Sample size slider
                        html.Div(
                            id="sample-size-slider",
                            children=[
                                html.Label(
                                    "Sample size (n):",
                                    htmlFor="sample-size",
                                ),
                                dcc.Slider(
                                    id="sample-size",
                                    min=10,
                                    max=300,
                                    value=100,
                                    step=10,
                                    included=False,
                                    tooltip={"placement": "top"},
                                    marks={
                                        i: {"label": f"{i}"}
                                        for i in range(0, 500, 50)
                                    },
                                ),
                            ],
                        ),
                        # Parameter info
                        html.Div(id="current-params"),
                        # Distribution description
                        html.Div(className="description", id="description"),
                    ],
                ),
                # Histogram & violin-plot
                html.Div(
                    className="histogram-and-violin",
                    children=[
                        # Histogram
                        dcc.Loading(
                            color="cyan",
                            children=[
                                dcc.Graph(id="histogram", config=PLOT_CONFIG)
                            ],
                        ),
                        # Violin plot
                        dcc.Loading(
                            color="cyan",
                            children=[
                                dcc.Graph(id="violin-plot", config=PLOT_CONFIG)
                            ],
                        ),
                    ],
                ),
                # ECDF-plot & summary statistics table
                html.Div(
                    className="ecdf-and-stats",
                    children=[
                        # ECDF plot
                        dcc.Loading(
                            color="cyan",
                            children=[
                                dcc.Graph(id="ecdf-plot", config=PLOT_CONFIG)
                            ],
                        ),
                        # Summary statistics table
                        html.Div(
                            className="stats-table",
                            children=[html.Table(id="summary-stats")],
                        ),
                        dcc.Store(id="sample-store"),
                        # Sample download button
                        html.Button(
                            "Download sample",
                            id="sample-download-button",
                            className="custom-button",
                        ),
                        dcc.Download(id="download-sample"),
                    ],
                ),
            ],
        ),
    ]
)


@app.callback(
    Output("distribution-param-sliders", "children"),
    Input("current-distribution", "value"),
)
def create_parameter_sliders(distribution: str) -> tuple:
    """Get the parameter labels & sliders for parameters of the selected
    distribution.

    Args:
        distribution (str): The name of the currently selected distribution.

    Returns"
        tuple: Parameter labels and sliders.
    """
    dist_data = distribution_data[distribution]
    num_params = dist_data["num_params"]

    param_sliders = [
        (
            html.Label(
                dist_data[f"param{idx}"] + ":",
                id=f"param{idx}_name",
                htmlFor=f"parameter{idx}",
            ),
            dcc.Slider(
                id=f"parameter{idx}",
                min=0.05,
                max=dist_data[f"param{idx}_max"],
                step=0.01,
                value=dist_data[f"param{idx}_max"] / 2,
                tooltip={"placement": "top"},
                marks={i: {"label": f"{i}"} for i in PARAM_SLIDER_TICKS},
            ),
        )
        for idx in range(1, num_params + 1)
    ]

    if num_params < 2:
        # Ensure a component with id 'parameter2' exists, since it is expected
        # in other callbacks.
        param_sliders.append(
            (dcc.Input(id="parameter2", value=None, type="hidden"))
        )
    return sum(param_sliders, start=())  # Concatenate


@app.callback(
    [Output("description", "children")],
    [Input("current-distribution", "value")],
)
def show_distribution_info(distribution: str) -> list:
    """Get a brief summary of the selected distribution.

    Args:
        distribution (str): The name of the current distribution.

    Returns:
        list: A brief summary of the distribution, and a link to it's page on
        Wikipedia.
    """
    dist_data = distribution_data[distribution]
    summary = [
        html.P(paragraph) for paragraph in dist_data["summary"].split(">")
    ]
    wiki_link = [
        html.A(
            "Learn more...",
            className="wiki-link",
            href=dist_data["wiki_link"],
        )
    ]
    return [summary + wiki_link]


@app.callback(
    [
        Output("histogram", "figure"),
        Output("violin-plot", "figure"),
        Output("ecdf-plot", "figure"),
        Output("summary-stats", "children"),
        Output("current-params", "children"),
        Output("sample-store", "data"),
    ],
    [
        Input("current-distribution", "value"),
        Input("sample-size", "value"),
        Input("parameter1", "value"),
        Input("parameter2", "value"),
    ],
)
def create_and_plot_sample(distribution: str, size: int, *parameters) -> tuple:
    """Create a sample of the specified distribution using the provided
    parameters, then plot a histogram & violin-plot, and compute descriptive
    statistics.

    Args:
        distribution (str): The name of the currently selected distribution.
        size (int): The desired sample size.
        *parameters (tuple): 1 or 2 parameter values, as per the distribution.

    Returns:
        tuple: A histogram, a violin_plot, an ecdf-plot, a table of summary
        statistics, the currently specified parameters and a csv file with the
        sample data for download.
    """
    sample = process_random_sample(distribution, size, parameters)

    histogram = plotting.plot_histogram(sample["data"], distribution)
    violin_plot = plotting.plot_violin(sample["data"], distribution)
    ecdf_plot = plotting.plot_ecdf(sample["data"], distribution)

    summary_statistics = sample["summary_statistics"]
    summary_statistics_table = [html.Th("Summary Statistics")] + [
        html.Tr([html.Td(f"{name}:"), html.Td(value)])
        for name, value in summary_statistics.items()
    ]

    parameters = sample["parameters"]
    param_dict = {
        distribution_data[distribution].get(f"param{idx}"): value
        for idx, value in enumerate(parameters, start=1)
    }
    param_dict["Sample Size"] = size
    parameter_info = [
        html.H3("Parameters: "),
        html.P(
            [
                ", ".join(
                    [f"{key}: {value}" for key, value in param_dict.items()]
                )
            ]
        ),
    ]

    sample_csv_download = {
        "content": sample["data"].to_csv(index=False),
        "filename": f"{distribution}-sample.csv",
        "type": "text/csv",
    }
    return (
        histogram,
        violin_plot,
        ecdf_plot,
        summary_statistics_table,
        parameter_info,
        sample_csv_download,
    )


@app.callback(
    Output("download-sample", "data"),
    Input("sample-download-button", "n_clicks"),
    State("sample-store", "data"),
)
def download_sample(clicks: int, data: dict) -> dict:
    """Retrieve the current sample data for download whenever a user clicks on
    the sample download button.

    Args:
        clicks (int): The number of clicks on the download button.
        data (dict): Sample values & meta-data.

    Returns:
        dict: Sample values and metadata for download.
    """
    if clicks == 0:
        return dict(content="", filename="", type="text/plain")
    else:
        return data
