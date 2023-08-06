
import numpy as np

from pathlib import Path
from typing import List
import os
from dash.dependencies import Output, Input
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from flask import Flask, Blueprint
import logging 
import plotly.graph_objs as go


DEVEL_MODE = bool(os.getenv("DEVEL_MODE", False))
if not DEVEL_MODE:
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

base_pathname = '/'
print('url_base_pathname', base_pathname)

server = Flask(__name__)
app = dash.Dash(__name__,
                server=server,
                url_base_pathname=base_pathname
                )

bp = Blueprint('myBlueprint', __name__)

osparc_style = {
    'color': '#bfbfbf',
    'backgroundColor': '#202020',
    'gridColor': '#444444',
}

# The Interval component and call make runs every 5 seconds, reload input data and plots them
app.layout = html.Div(style=osparc_style,
    children=[
    dcc.Graph(id='graph-1'),
    dcc.Graph(id='graph-2'),
    dcc.Graph(id='graph-3'),
            dcc.Interval(
            id='interval-component',
            interval=1*20000, # in milliseconds
            n_intervals=0
        )
]
)

@app.callback(
    [
        Output('graph-1', 'figure'),
        Output('graph-2', 'figure'),
        Output('graph-3', 'figure')
    ],
    [
    Input('interval-component', 'n_intervals')
    ]
)
def plot_graphs(n) -> List[go.Figure]:
    if len(check_inputs()) == 4:

        figs = [
            plot_top_middle_graph(check_inputs()[0]),
            plot_top_middle_graph(check_inputs()[1]),
            plot_bottom_graph(check_inputs()[2])
            ]
  
    else:
        print("Some of the inputs were not found, showing empty graph", flush=DEVEL_MODE)
        figs = [get_empty_graph() for i in range(3)]
    return figs

@bp.route("/")
def serve_index():
    plot_graphs(1)
    return app.layout


#---------------------------------------------------------#
# Check if expected inputs are in the input ports, get and process them

IN_PARENT_DIR = Path(os.environ["DY_SIDECAR_PATH_INPUTS"])

def check_inputs() -> list:
    INPUT_1 = list(Path(os.environ["DY_SIDECAR_PATH_INPUTS"]).joinpath("input_1/").glob("*txt"))
    INPUT_2 = list(Path(os.environ["DY_SIDECAR_PATH_INPUTS"]).joinpath("input_2/").glob("*txt"))
    INPUT_3 = list(Path(os.environ["DY_SIDECAR_PATH_INPUTS"]).joinpath("input_3/").glob("*txt"))
    if len(INPUT_1) == 1 and len(INPUT_2) == 1 and len(INPUT_3) == 1:
        return [INPUT_1[0], INPUT_2[0], INPUT_3[0]]
    else:
        return []

def get_input_df(input_path: Path) -> pd.DataFrame:
    return pd.read_csv(input_path)


#---------------------------------------------------------#
# Plot data 

def plot_top_middle_graph(data_path) -> go.Figure:
    data = get_input_df(data_path)
    xlab, ylab = data.columns
    name, unit = ylab.split("(")

    fig = get_empty_graph("", "", legend=False)
    fig.update_layout = go.Layout(fig['layout'])
    fig.add_trace(go.Scatter(x=data[xlab], y=data[ylab], name=unit[:-1]))
    fig.update_yaxes(title_text="<br>".join([name,"("+unit]))
    return fig



def plot_bottom_graph(data_path) -> go.Figure:
    data = get_input_df(data_path)
    xlab, ylab = data.columns
    name, unit = ylab.split("(")
    fig = get_empty_graph("", "", legend=False)
    fig.update_layout = go.Layout(fig['layout'])
    fig.add_trace(go.Scatter(x=data[xlab], y=data[ylab], name=unit[:-1]))
    fig.update_yaxes(title_text="<br>".join([name,"("+unit]))
    fig.update_traces(selector=0, patch = {"line": {"shape": 'hv'}})
    fig.update_xaxes(title_text="Time (s)", row=3)
    return fig
 

#---------------------------------------------------------#
# Styling

# app.css.append_css({
#     "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
# })


def give_fig_osparc_style(fig, xLabels=['x'], yLabels=['y'], legend=False):
    for idx, xLabel in enumerate(xLabels):
        suffix = str(idx)
        if idx == 0:
            suffix = ''
        fig['layout']['xaxis'+suffix].update(
            title=xLabel,
            gridcolor=osparc_style['gridColor']
        )
    for idx, yLabel in enumerate(yLabels):
        suffix = str(idx)
        if idx == 0:
            suffix = ''
        fig['layout']['yaxis'+suffix].update(
            title=yLabel,
            gridcolor=osparc_style['gridColor']
        )
    fig = give_fig_osparc_style2(fig, legend=legend)
    return fig

def give_fig_osparc_style2(fig, legend=False):
    margin = 10
    y_label_padding = 50
    x_label_padding = 30
    fig['layout']['margin'].update(
        l=margin+y_label_padding,
        r=margin,
        b=margin+x_label_padding,
        t=margin,
    )

    fig['layout'].update(
        autosize=True,
        height=400,
        showlegend=legend,
        plot_bgcolor=osparc_style['backgroundColor'],
        paper_bgcolor=osparc_style['backgroundColor'],
        font=dict(
            color=osparc_style['color']
        )
    )
    return fig

def get_empty_graph(xLabel='x', yLabel='y', legend=False):
    fig = go.Figure(data=[], layout={})
    fig = give_fig_osparc_style(fig, [xLabel], [yLabel], legend=legend)
    return fig


if __name__ == "__main__":
    server.register_blueprint(bp, url_prefix=base_pathname)
    print(f"Devel mode is: {DEVEL_MODE}")
    app.run_server(debug=DEVEL_MODE, port=8888, host="0.0.0.0")