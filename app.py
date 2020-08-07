import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output  # State
import pandas as pd
from stats_functions import get_random_sample
import plotly.express as px

distributions = pd.read_csv('distributions.csv', index_col=0).fillna('N/A')


app = dash.Dash(__name__)

app.layout = html.Div([
    # Top level heading
    html.H1("Statistical Distribution Sampler"),

    #  Distributions drop-down menu
    html.Div(id='parameters', style={'width': 400}, children=[
             html.Label("Statistical distribution:",
                        htmlFor='select-distribution'),
             dcc.Dropdown(id='select-distribution',
                          options=[{'label': dist, 'value': dist}
                                   for dist in distributions.index],
                          value='Normal'),
             html.Label(id='param1name'),
             dcc.Slider(id='parameter1',
                        min=0.5, max=10, step=0.5, value=0.5),
             html.Label(id='param2name'),
             dcc.Slider(id='parameter2',
                        min=0.001, max=10, step=0.5, value=0.5),
             html.Label("Sample size (n):", htmlFor='sample-size'),
             dcc.Slider(id='sample-size', min=10, max=10000, step=10,
                        value=20)
             ]),
    dcc.Graph(id='histogram'),
    dcc.Graph(id='boxplot'),
    dcc.Graph(id='violinplot')

])


@app.callback([Output('param1name', 'children'),
               Output('param2name', 'children'),
               Output('parameter2', 'disabled')],
              [Input('select-distribution', 'value')])
def set_parameters(distribution):
    dist_data = distributions.loc[distribution]
    num_params = dist_data['#parameters']
    param1_name, param2_name = dist_data['param1'], dist_data['param2']
    return param1_name, param2_name, True if num_params < 2 else False


@app.callback([Output('histogram', 'figure'),
               Output('boxplot', 'figure'),
               Output('violinplot', 'figure')],
              [Input('select-distribution', 'value'),
               Input('sample-size', 'value'),
               Input('parameter1', 'value'),
               Input('parameter2', 'value')])
def create_sample(distribution, size, *parameters):
    sample = get_random_sample(distribution, size, parameters)
    fig1 = px.histogram(x=sample, width=640, height=480)
    fig2 = px.box(y=sample, width=640, height=480)
    fig3 = px.violin(y=sample, width=640, height=480)
    return fig1, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True)
