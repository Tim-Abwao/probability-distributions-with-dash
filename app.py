import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output  # State

from stats_functions import descriptive_stats, get_random_sample

distributions = pd.read_csv('distributions.csv', index_col=0).fillna('N/A')


app = dash.Dash(__name__, title="Statistical Distributions Sampler",
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'
                            }])

app.layout = html.Div([
    # Top level heading
    dcc.Markdown(["""
    # Statistical Distribution Sampler

    This simple dashboard let's you try various statistical distributions,
    set parameters, and see their effect in real time.
    """]),
    html.Div([
        #  Distributions drop-down menu
        html.Div(id='parameters', children=[
             html.Label("Statistical distribution:", className='param-label',
                        htmlFor='select-distribution'),
             dcc.Dropdown(id='select-distribution',
                          options=[{'label': dist, 'value': dist}
                                   for dist in distributions.index],
                          value='Normal'),
             html.Label(id='param1name', className='param-label',
                        htmlFor='parameter1'),
             dcc.Slider(id='parameter1',
                        min=0.5, max=10, step=0.5, value=10),
             html.Label(id='param2name', className='param-label',
                        htmlFor='parameter2'),
             dcc.Slider(id='parameter2',
                        min=0.001, max=10, step=0.5, value=10),
             html.Label("Sample size (n):", className='param-label',
                        htmlFor='sample-size'),
             dcc.Slider(id='sample-size', min=10, max=500, value=20,
                        step=10, included=False,
                        marks={i: {'label': f'{i}'}
                               for i in range(0, 500, 50)})
             ]),
        html.Div(html.Table(id='summary-stats'), className='stats')
        ], className='parameters'),
    html.Div([
        html.Div(dcc.Graph(id='histogram')),
        html.Div(dcc.Graph(id='violinplot')),
    ], className='graphics',)
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
               Output('violinplot', 'figure'),
               Output('summary-stats', 'children')],
              [Input('select-distribution', 'value'),
               Input('sample-size', 'value'),
               Input('parameter1', 'value'),
               Input('parameter2', 'value')])
def create_sample(distribution, size, *parameters):
    sample = get_random_sample(distribution, size, parameters)
    fig1 = px.histogram(x=sample, marginal='rug')
    fig2 = px.violin(y=sample, box=True, points='all')

    sample_stats = [html.Th('Summary Statistics:')] + \
                   [html.Tr([html.Td(f'{name}:'), html.Td(value)])
                    for name, value in descriptive_stats(sample).items()]

    return fig1, fig2, sample_stats


if __name__ == '__main__':
    app.run_server(debug=True)
