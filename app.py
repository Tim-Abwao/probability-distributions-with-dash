import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from stats_functions import descriptive_stats, get_random_sample
import json

with open('distributions.json') as file:
    dist_data = json.load(file)

param_ticks = [0, 0.5, 1, 2.5, 5, 7.5, 10]  # for parameter sliders


app = dash.Dash(
    __name__,
    title="Statistical Distributions Sampler",
    meta_tags=[{'name': 'viewport',
                'content': 'width=device-width, initial-scale=1.0'}]
)

server = app.server

app.layout = html.Div([
    # Top level heading
    dcc.Markdown(["""
    # Statistical Distribution Sampler

    This simple dashboard let's you try various statistical distributions,
    set parameters, and see their effect in real time.
    """]),
    html.Div([
        # Selected distribution's description
        html.Div(id='description', className='description'),

        # Distribution and parameter selection
        html.Div(id='parameters', children=[
            # Distribution drop-down menu
            html.Label("Statistical distribution:", className='param-label',
                       htmlFor='select-distribution'),
            dcc.Dropdown(id='select-distribution', value='Normal',
                         options=[{'label': dist, 'value': dist}
                                  for dist in dist_data],
                         style={'color': 'teal'}
                         ),
            # Parameter 1 slider
            html.Label(id='param1name', className='param-label',
                       htmlFor='parameter1'),
            dcc.Slider(id='parameter1', included=False, min=0.05, max=10,
                       step=0.01, value=5, tooltip={'placement': 'top'},
                       marks={i: {'label': f'{i}'} for i in param_ticks}),

            # Parameter 2 slider
            html.Label(id='param2name', className='param-label',
                       htmlFor='parameter2'),
            dcc.Slider(id='parameter2', included=False, min=0.05, max=10,
                       step=0.01, value=5, tooltip={'placement': 'top'},
                       marks={i: {'label': f'{i}'} for i in param_ticks}),

            # Sample size slider
            html.Label("Sample size (n):", className='param-label',
                       htmlFor='sample-size'),
            dcc.Slider(id='sample-size', min=10, max=300, value=100,
                       step=10, included=False, tooltip={'placement': 'top'},
                       marks={i: {'label': f'{i}'}
                              for i in range(0, 500, 50)})
            ]),

        # Summary-statistics table
        html.Div([html.Table(id='summary-stats'),
                  html.P(id='current-params')], className='stats'),
        ], className='parameters'),

    # Container for the graphs
    html.Div([
        html.Div(dcc.Graph(id='histogram')),
        html.Div(dcc.Graph(id='violinplot')),
    ], className='graphics')
])


@app.callback([Output('param1name', 'children'),
               Output('param2name', 'children'),
               Output('parameter2', 'disabled')],
              [Input('select-distribution', 'value')])
def set_parameters(distribution):
    """
    Set the parameter labels for the selected distribution. Additionally,
    disable 2nd parameter slider if the distribution doesn't require it.
    """
    dist = dist_data[distribution]
    param1_name, param2_name = dist['param1'], dist['param2']
    num_params = dist['num_params']
    omit_param2 = True if num_params < 2 else False
    return param1_name, param2_name, omit_param2


@app.callback([Output('parameter1', 'max'),
               Output('parameter2', 'max')],
              [Input('param1name', 'children'),
               Input('param2name', 'children')])
def scale_probability_slider(*param_names):
    """
    Rescale a parameter slider to the range [0, 1] if it is a probability.
    """
    maximum = [1 if 'Prob' in name else 10 for name in param_names]
    return maximum


@app.callback(Output('current-params', 'children'),
              [Input('param1name', 'children'),
               Input('parameter1', 'value'),
               Input('param2name', 'children'),
               Input('parameter2', 'value'),
               Input('sample-size', 'value')])
def display_current_params(nam1, val1, nam2, val2, n):
    """Display the current parameters as name:value pairs."""
    if nam2 == 'N/A':
        nam2_val2 = ''
    else:
        nam2_val2 = f' {nam2}: {val2},'
    return [html.B('Parameters: '),
            f'{nam1}: {val1},{nam2_val2} Sample size: {n}']


@app.callback(Output('description', 'children'),
              [Input('select-distribution', 'value')])
def show_description(distribution):
    """Display selected distribution's summary information."""
    return ([html.H3(f'Current selection: {distribution} Distribution')]
            + [html.P(desc)
               for desc in [dist_data[distribution]['summary'].split('>')]
            + [html.A('Learn more...', className='wiki-link',
               href=dist_data[distribution]['wiki_link'])]])


@app.callback([Output('histogram', 'figure'),
               Output('violinplot', 'figure'),
               Output('summary-stats', 'children')],
              [Input('select-distribution', 'value'),
               Input('sample-size', 'value'),
               Input('parameter1', 'value'),
               Input('parameter2', 'value')])
def process_sample(distribution, size, *parameters):
    """
    Create a sample of the selected distribution with specified parameters,
    plot a histogram & a violin plot, then compute descriptive statistics.
    """
    sample = get_random_sample(distribution, size, parameters)

    fig1 = px.histogram(x=sample, marginal='box', opacity=0.5,
                        color_discrete_sequence=['teal'],
                        title=f'{distribution} Sample Histogram',
                        template='plotly_dark')

    fig2 = px.violin(x=sample, box=True, color_discrete_sequence=['teal'],
                     title=f'{distribution} Sample Violin Plot',
                     template='plotly_dark')

    sample_stats = ([html.Th('Summary Statistics')]
                    + [html.Tr([html.Td(f'{name}:'), html.Td(value)])
                       for name, value in descriptive_stats(sample).items()])

    return fig1, fig2, sample_stats


if __name__ == '__main__':
    app.run_server(debug=True)
