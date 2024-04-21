# from dash import Dash, html
import time
import importlib

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import utils.dash_reusable_components as drc
import utils.figures as figs

from ces import CES


app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    external_stylesheets=[dbc.themes.GRID,
                          dbc.themes.SLATE]
)

app.layout = dbc.Container(
    children=[
        # banner
        dbc.Row(
            [
                html.Div(
                    className="banner",
                    children=[
                        html.Div(
                            children=[
                                html.H2(
                                    id="banner-title",
                                    children=[
                                        html.A(
                                            "Constant Elasticity of Substitution (CES) function Explorer",
                                            href="https://github.com/Schlegen/CES-explorer",
                                            style={
                                                "textDecoration": "none",
                                                "color": "inherit",
                                            },
                                        )
                                    ],
                                ),
                            ],
                        )
                    ],
                )
            ]
        ),

        dbc.Container(
            [
                html.Span(
                    id="body",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        drc.Card(
                                            id="first-card",
                                            children=[
                                                drc.NamedSlider(
                                                    name="alpha_x",
                                                    id="slider-alpha-x",
                                                    min=0,
                                                    max=1,
                                                    marks={
                                                        i / 10: str(i / 10)
                                                        for i in range(0, 11, 2)
                                                    },
                                                    step=0.1,
                                                    value=0.2,
                                                ),
                                                drc.NamedSlider(
                                                    name="alpha_y",
                                                    id="slider-alpha-y",
                                                    min=0,
                                                    max=1,
                                                    marks={
                                                        i / 10: str(i / 10)
                                                        for i in range(0, 11, 2)
                                                    },
                                                    step=0.1,
                                                    value=0.2,
                                                ),
                                                drc.NamedSlider(
                                                    name="rho",
                                                    id="slider-rho",
                                                    min=-2,
                                                    max=5,
                                                    value=0.5
                                                )
                                            ],
                                        )
                                    ],
                                    width=2,
                                ),
                                dbc.Col(
                                    html.Span(
                                        id="central-graph",
                                        children=dcc.Graph(
                                            id="graph-ces",
                                            figure=dict(
                                                layout=dict(
                                                    plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                                )
                                            ),
                                        )
                                    ),
                                    width=6,
                                ),
                                dbc.Col(
                                    html.Span(
                                        children=[
                                            dcc.Graph(
                                                id="graph-y",
                                                figure=dict(
                                                    layout=dict(
                                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                                    )
                                                )
                                            ),
                                            dcc.Graph(
                                                id="graph-marginal1",
                                                figure=dict(
                                                    layout=dict(
                                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                                    )
                                                )
                                            ),
                                            dcc.Graph(
                                                id="graph-marginal2",
                                                figure=dict(
                                                    layout=dict(
                                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                                    )
                                                )
                                            ),
                                        ]
                                    ),
                                    width=4,
                                ),
                            ],
                            style={"display": "flex"},  # Ensure columns are displayed side by side
                        )
                    ],
                )
            ],
        style={
            "width": "100%",
            'maxWidth' : '100vw'
        }
        ),
    ],
    style={
        "width": "100%",
        'maxWidth' : '100vw'
    }
)



@app.callback(
    Output("central-graph", "children"),
    [
        # Input("slider-x", "value"),
        # Input("slider-y", "value"),
        Input("slider-alpha-x", "value"),
        Input("slider-alpha-y", "value"),
        Input("slider-rho", "value")
    ],
)
def update_central_graph(alpha_x, alpha_y, rho):

    ces_function = CES(1, 1, 1, rho)

    ces_figure = figs.serve_CES_plot(0, 0, 10, 10, ces_function)

    return [
        html.Span(
            id="central-graph",
            children=dcc.Loading(
                className="graph-wrapper",
                children=dcc.Graph(id="graph-ces", figure=ces_figure),
                style={"display": "none"},
            )
        )
    ]


if __name__ == '__main__':
    app.run(debug=True)