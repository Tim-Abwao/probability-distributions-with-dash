import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

from stats_app.utils import process_random_sample

with open("stats_app/distributions.json") as file:
    distribution_data = json.load(file)

param_ticks = [0, 0.5, 1, 2.5, 5, 7.5, 10]  # for parameter sliders


app = dash.Dash(
    "stats_app",
    title="Statistical Distributions Sampler",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }
    ],
)


app.layout = html.Div(
    [
        # Title
        html.H1("Probability Distribution Sampler"),
        # Dashboard components
        html.Div(
            className="content",
            children=[
                # Side-bar with distribution info and parameter-setters
                html.Div(
                    className="side-bar",
                    children=[
                        # Distribution description
                        html.H3(id="distribution-name"),
                        html.Div(className="description", id="description"),
                        # Distribution selector
                        html.Div(
                            [
                                html.Label(
                                    "Statistical distribution:",
                                    className="param-label",
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
                            ]
                        ),
                        # Container for parameter slider(s)
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
                                    className="param-label",
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
                    ],
                ),
                # Graph (histogram + marginal boxplot)
                dcc.Loading(
                    color="cyan",
                    children=[
                        html.Div(
                            className="graph-container",
                            children=[dcc.Graph(id="histogram")],
                        )
                    ],
                ),
                # Summary statistics table
                html.Div(
                    className="stats-table",
                    children=[
                        html.Table(id="summary-stats"),
                        html.Div(id="current-params"),
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
def create_parameter_sliders(distribution):
    """Set the parameter labels and sliders for parameters of the selected
    distribution.

    Parameters
    ----------
    distribution : str
        The name of the currently selected distribution.

    Returns
    -------
    A tuple with the labelled parameter slider components.
    """
    selected_dist_data = distribution_data[distribution]
    num_params = selected_dist_data["num_params"]

    param_sliders = [
        (
            html.Label(
                selected_dist_data[f"param{idx}"] + ":",
                id=f"param{idx}_name",
                className="param-label",
                htmlFor=f"parameter{idx}",
            ),
            dcc.Slider(
                id=f"parameter{idx}",
                min=0.05,
                max=selected_dist_data[f"param{idx}_max"],
                step=0.01,
                value=selected_dist_data[f"param{idx}_max"] / 2,
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
    return sum(param_sliders, start=())  # Concatenate the slider pair


@app.callback(
    [
        Output("distribution-name", "children"),
        Output("description", "children"),
    ],
    [Input("current-distribution", "value")],
)
def show_distribution_info(distribution):
    """Display a brief summary of the selected distribution's characteristics.

    Parameters
    ----------
    distribution : str
        The name of the current distribution

    Returns
    -------
    The distribution's name, a brief summary, and a link to Wikipedia for more
    information.
    """
    title = f"Current selection: {distribution} Distribution"
    text = [
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
    return title, text + wiki_link


@app.callback(
    [
        Output("histogram", "figure"),
        Output("summary-stats", "children"),
        Output("current-params", "children"),
    ],
    [
        Input("current-distribution", "value"),
        Input("sample-size", "value"),
        Input("parameter1", "value"),
        Input("parameter2", "value"),
    ],
)
def create_and_plot_sample(distribution, size, *parameters):
    """
    Create a sample of the selected distribution, using the set parameters,
    then plot a histogram & box-plot. Also, compute descriptive statistics for
    the generated sample.

    Parameters
    ----------
    distribution : str
        The name of the currently selected distribution
    size : int
        The set sample size
    parameters : int, floaf
        Parameter values

    Returns
    -------
    A plotted figure and a table of summary statistics.
    """
    # Generate a ramdom sample
    sample_info = process_random_sample(distribution, size, parameters)
    data = sample_info["data"]
    parameters = sample_info["parameters"]
    summary_statistics = sample_info["summary_statistics"]

    # Plot a histogram with a marginal box-plot
    fig = px.histogram(
        x=data,
        marginal="box",
        nbins=50,
        opacity=0.9,
        template="plotly_dark",
        color_discrete_sequence=["cyan"],
        height=550,
        title=f"{distribution} Sample",
    )
    fig.update_xaxes(fixedrange=True, title="Values")
    fig.update_yaxes(fixedrange=True, title="Frequency")
    fig.update_layout(
        plot_bgcolor="#205050",
        paper_bgcolor="#205050",
        font_family="Courier New",
    )

    # Create a table of summary statistics
    summary_statistics_table = [html.Th("Summary Statistics")] + [
        html.Tr([html.Td(f"{name}:"), html.Td(value)])
        for name, value in summary_statistics.items()
    ]

    # Create a mapping of parameter names and their values
    current_distribution_data = distribution_data.get(distribution)
    param_dict = {
        current_distribution_data.get(f"param{idx}"): value
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

    return fig, summary_statistics_table, parameter_info


if __name__ == "__main__":
    app.run_server(debug=True)
