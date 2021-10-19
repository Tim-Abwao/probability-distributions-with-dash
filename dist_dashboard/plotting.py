import plotly.express as px
from plotly.graph_objects import Figure
from pandas.core.series import Series


def customize_figure(fig: Figure) -> Figure:
    """Update the layout and style of plotly figures.

    Parameters
    ----------
    fig : plotly.graph_objs._figure.Figure
        The figure to modify

    Returns
    -------
    plotly.graph_objs._figure.Figure
        A customized figure.
    """
    fig.update_xaxes(fixedrange=True, title="Values", title_font_size=12)
    fig.update_yaxes(fixedrange=True, title_font_size=12)
    fig.update_layout(
        font_family="Courier New",
        paper_bgcolor="#205050",
        plot_bgcolor="#205050",
        margin={"l": 60, "t": 40, "r": 10, "b": 10},
        title_font_size=13,
        template="plotly_dark",
    )
    return fig


def plot_ecdf(data: Series, distribution: str) -> Figure:
    """Get an Empirical Cummulative Distribution plot of the given data.

    Parameters
    ----------
    data : Series
        The data to plot
    distribution : str
        The data's probability distribution

    Returns
    -------
    plotly.graph_objs._figure.Figure
        A plotly figure.
    """
    fig = px.ecdf(
        x=data,
        color_discrete_sequence=["cyan"],
        lines=False,
        markers=True,
        title=f"ECDF Plot <i>({distribution} Distribution)</i>",
    )
    return customize_figure(fig)


def plot_histogram(data: Series, distribution: str) -> Figure:
    """Get a histogram of the given data.

    Parameters
    ----------
    data : Series
        The data to plot
    distribution : str
        The data's probability distribution

    Returns
    -------
    plotly.graph_objs._figure.Figure
        A plotly figure
    """
    fig = px.histogram(
        x=data,
        nbins=50,
        opacity=0.9,
        color_discrete_sequence=["cyan"],
        title=f"Histogram <i>({distribution} Distribution)</i>",
    )
    return customize_figure(fig)


def plot_violin(data: Series, distribution: str) -> Figure:
    """Get a violin-plot of the given data.

    Parameters
    ----------
    data : Series
        The data to plot
    distribution : str
        The data's probability distribution

    Returns
    -------
    Figure
        A plotly figure.
    """
    fig = px.violin(
        x=data,
        box=True,
        points="all",
        color_discrete_sequence=["cyan"],
        title=f"Violin Plot <i>({distribution} Distribution)</i>",
    )
    return customize_figure(fig)
