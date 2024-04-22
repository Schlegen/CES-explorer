# from dash import Dash, html
import time
import importlib

import dash
from dash import dcc
from dash import html
from dash import callback_context

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
                          dbc.themes.DARKLY]
)
app.title = 'CES-explorer'


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
                                            "CES-Explorer",
                                            href="https://github.com/Schlegen/CES-explorer",
                                            style={
                                                "textDecoration": "none",
                                                "color": "inherit",
                                                "fontFamily": "Arial, sans-serif",
                                                "fontSize": "28px",
                                                "fontWeight": "bold",
                                            },
                                        )
                                    ],
                                ),
                                html.P(
                                    "Explore the Constant Elasticity of Substitution function with interactive sliders",
                                    style={
                                        "fontSize": "16px",
                                        "marginTop": "5px",
                                        "color": "#777",
                                    },
                                ),
                            ],
                        )
                    ],
                )
            ],
            style={"backgroundColor": "rgb(50, 50, 50)", "padding": "10px"},
            className="mb-4",
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
                                                    name="alpha1",
                                                    id="slider-alpha1",
                                                    min=0,
                                                    max=1,
                                                    marks={
                                                        i / 10: str(i / 10)
                                                        for i in range(0, 11, 2)
                                                    },
                                                    step=0.1,
                                                    value=0.5,
                                                ),
                                                drc.NamedSlider(
                                                    name="alpha2",
                                                    id="slider-alpha2",
                                                    min=0,
                                                    max=1,
                                                    marks={
                                                        i / 10: str(i / 10)
                                                        for i in range(0, 11, 2)
                                                    },
                                                    step=0.1,
                                                    value=0.5,
                                                ),
                                                drc.NamedSlider(
                                                    name="rho",
                                                    id="slider-rho",
                                                    min=-10,
                                                    max=10,
                                                    value=2
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
        Input("slider-alpha1", "value"),
        Input("slider-alpha2", "value"),
        Input("slider-rho", "value")
    ],
)
def update_central_graph(alpha1, alpha2, rho):

    ces_function = CES(alpha1, alpha2, rho)
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



@app.callback(
    Output("slider-alpha1", "value"),
    [Input("slider-alpha2", "value")]
)
def update_slider_alpha1(alpha2):
    # Check if the callback was triggered by slider-alpha2
    ctx = callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"]
        if prop_id == "slider-alpha2.value":
            return 1 - alpha2
    # If not triggered by slider-alpha2, return None to prevent circular reference
    return dash.no_update

@app.callback(
    Output("slider-alpha2", "value"),
    [Input("slider-alpha1", "value")]
)
def update_slider_alpha2(alpha1):
    # Check if the callback was triggered by slider-alpha1
    ctx = callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"]
        if prop_id == "slider-alpha1.value":
            return 1 - alpha1
    # If not triggered by slider-alpha1, return None to prevent circular reference
    return dash.no_update


if __name__ == '__main__':
    app.run(debug=True)
