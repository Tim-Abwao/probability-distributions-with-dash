import json

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output, State

from distributions_dashboard.utils import process_random_sample

with open("distributions_dashboard/distributions.json") as file:
    distribution_data = json.load(file)

param_ticks = [0, 0.5, 1, 2.5, 5, 7.5, 10]  # for parameter sliders


app = Dash(
    name="distributions_dashboard",
    title="Probability Distributions Sampler",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }
    ],
)


app.layout = html.Div(
    [
        # Main title
        html.H1("Probability Distribution Sampler"),
        # Dashboard content
        html.Div(
            className="content",
            children=[
                # Side-bar
                html.Div(
                    className="side-bar",
                    children=[
                        # Distribution selector
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
                        # Distribution description
                        html.H3(id="distribution-name"),
                        html.Div(className="description", id="description"),
                    ],
                ),
                # Graphs & Summary statistics
                html.Div(
                    className="statistics-and-plots",
                    children=[
                        # Histogram
                        dcc.Loading(
                            color="cyan",
                            children=[html.Div(dcc.Graph(id="histogram"))],
                        ),
                        # Violin plot
                        dcc.Loading(
                            color="cyan",
                            children=[html.Div(dcc.Graph(id="violin-plot"))],
                        ),
                        # Summary statistics table
                        html.Div(
                            className="stats-table",
                            children=[html.Table(id="summary-stats")],
                        ),
                        # Sample download button
                        html.Div(
                            [
                                html.Div(id="current-params"),
                                html.Button(
                                    "Download sample",
                                    id="sample-download-button",
                                    className="custom-button",
                                ),
                                dcc.Download(id="download-sample"),
                            ]
                        ),
                        dcc.Store(id="sample-store"),
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
    """Set the parameter labels and sliders for parameters of the selected
    distribution.

    Parameters
    ----------
    distribution : str
        The name of the currently selected distribution.

    Returns
    -------
    tuple
        Parameter label(s) and slider(s).
    """
    distr_data = distribution_data[distribution]
    num_params = distr_data["num_params"]

    param_sliders = [
        (
            html.Label(
                distr_data[f"param{idx}"] + ":",
                id=f"param{idx}_name",
                htmlFor=f"parameter{idx}",
            ),
            dcc.Slider(
                id=f"parameter{idx}",
                min=0.05,
                max=distr_data[f"param{idx}_max"],
                step=0.01,
                value=distr_data[f"param{idx}_max"] / 2,
                tooltip={"placement": "top"},
                marks={i: {"label": f"{i}"} for i in param_ticks},
            ),
        )
        for idx in range(1, num_params + 1)
    ]

    if num_params < 2:
        # Ensure a component with id 'parameter2' exists, since it is expected
        # in other callbacks.
        param_sliders.append(
            (dcc.Input(id="parameter2", value=None, type="hidden"),)
        )
    return sum(param_sliders, start=())  # Concatenate


@app.callback(
    [
        Output("distribution-name", "children"),
        Output("description", "children"),
    ],
    [Input("current-distribution", "value")],
)
def show_distribution_info(distribution: str) -> tuple:
    """Display a brief summary of the selected distribution's characteristics.

    Parameters
    ----------
    distribution : str
        The name of the current distribution

    Returns
    -------
    tuple
        The distribution name, a brief summary, and a link to Wikipedia for
        more info.
    """
    title = f"Current selection: {distribution} Distribution"
    summary = [
        html.P(desc)
        for desc in distribution_data[distribution]["summary"].split(">")
    ]
    wiki_link = [
        html.A(
            "Learn more...",
            className="wiki-link",
            href=distribution_data[distribution]["wiki_link"],
        )
    ]
    return title, summary + wiki_link


@app.callback(
    [
        Output("histogram", "figure"),
        Output("violin-plot", "figure"),
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

    Parameters
    ----------
    distribution : str
        The name of the currently selected distribution
    size : int
        The set sample size
    *parameters : int, floaf
        1 or 2 parameter values, depending on the distribution

    Returns
    -------
    tuple
        A histogram, a violin_plot, a table of summary statistics, the
        currently specified parameters and a csv file with the sample data for
        download.
    """
    sample = process_random_sample(distribution, size, parameters)

    histogram = px.histogram(
        x=sample["data"],
        nbins=50,
        height=320,
        opacity=0.9,
        template="plotly_dark",
        color_discrete_sequence=["cyan"],
        title=f"Histogram <i>({distribution} Distribution)</i>",
    )
    histogram.update_xaxes(fixedrange=True, title="Values")
    histogram.update_yaxes(fixedrange=True, title="Frequency")
    histogram.update_layout(
        font_family="Courier New",
        paper_bgcolor="#205050",
        plot_bgcolor="#205050",
        title_font_size=14
    )

    violin_plot = px.violin(
        x=sample["data"],
        box=True,
        points="all",
        height=320,
        template="plotly_dark",
        color_discrete_sequence=["cyan"],
        title=f"Violin Plot <i>({distribution} Distribution)</i>",
    )
    violin_plot.update_xaxes(fixedrange=True, title="Values")
    violin_plot.update_yaxes(fixedrange=True)
    violin_plot.update_layout(
        font_family="Courier New",
        paper_bgcolor="#205050",
        plot_bgcolor="#205050",
        title_font_size=14
    )

    parameters = sample["parameters"]
    summary_statistics = sample["summary_statistics"]
    summary_statistics_table = [html.Th("Summary Statistics")] + [
        html.Tr([html.Td(f"{name}:"), html.Td(value)])
        for name, value in summary_statistics.items()
    ]

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

    Parameters
    ----------
    clicks : int
        The number of clicks on the download button.
    data : dict
        A dictionary with the sample data.

    Returns
    -------
    dict
        The current sample's data and metadata for download.
    """
    if clicks == 0:
        return dict(content="", filename="", type="text/plain")
    else:
        return data


if __name__ == "__main__":
    app.run_server(debug=True)
