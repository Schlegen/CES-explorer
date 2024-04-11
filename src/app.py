# from dash import Dash, html
import time
import importlib

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import utils.dash_reusable_components as drc
import utils.figures as figs

from ces import CES

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        # .container class is fixed, .container.scalable is scalable
        # banner
        html.Div(
            className="banner",
            children=[
                # Change App Name here
                html.Div(
                    className="container scalable",
                    children=[
                        # Change App Name here
                        html.H2(
                            id="banner-title",
                            children=[
                                html.A(
                                    "Constant Elasticity of Substitution (CES) function Explorer",
                                    href="https://github.com/Schlegen/CES-explorer",
                                    style={
                                        "text-decoration": "none",
                                        "color": "inherit",
                                    },
                                )
                            ],
                        ),
                        html.A(
                            id="banner-logo",
                            children=[
                                html.Img(src=app.get_asset_url("images/logo-eiee.png"))
                            ],
                            href="https://plot.ly/products/dash/",
                        ),
                    ],
                )
            ],
        ),

        html.Div(
            id="body",
            className="container scalable",
            children=[
                html.Div(
                    id="app-container",
                    # className="row",
                    children=[
                        html.Div(
                            # className="three columns",
                            id="left-column",
                            children=[
                                drc.Card(
                                    id="first-card",
                                    children=[
                                        drc.NamedSlider(
                                            name="X",
                                            id="slider-x",
                                            min=0,
                                            max=1,
                                            marks={
                                                i / 10: str(i / 10)
                                                for i in range(0, 11, 2)
                                            },
                                            step=0.1,
                                            value=1,
                                        ),
                                        drc.NamedSlider(
                                            name="Y",
                                            id="slider-y",
                                            min=0,
                                            max=1,
                                            marks={
                                                i / 10: str(i / 10)
                                                for i in range(0, 11, 2)
                                            },
                                            step=0.1,
                                            value=0.2,
                                        ),
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            id="div-graphs",
                            children=dcc.Graph(
                                id="graph-ces",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                    )
                                ),
                            ),
                        ),
                    ],
                )
            ],
        ),
    ]
)

@app.callback(
    Output("div-graphs", "children"),
    [
        Input("slider-x", "value"),
        Input("slider-y", "value"),
    ],
)
def update_svm_graph(x, y):

    return [
        html.Div(
            id="svm-graph-container",
            children=dcc.Loading(
                className="graph-wrapper",
                children=dcc.Graph(id="graph-ces", figure=prediction_figure),
                style={"display": "none"},
            ),
        )
        # html.Div(
        #     id="graphs-container",
        #     children=[
        #         dcc.Loading(
        #             className="graph-wrapper",
        #             children=dcc.Graph(id="graph-line-roc-curve", figure=roc_figure),
        #         ),
        #         dcc.Loading(
        #             className="graph-wrapper",
        #             children=dcc.Graph(
        #                 id="graph-pie-confusion-matrix", figure=confusion_figure
        #             ),
        #         ),
        #     ],
        # ),
    ]

if __name__ == '__main__':
    app.run(debug=True)