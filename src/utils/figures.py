import os

import colorlover as cl
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.io as pio
import plotly
# import plotly.graph_objects as go
import numpy as np
from config import *




def serve_CES_plot_3d(ces_function, control_problem=None):
    # Colorscale
    cscale = [
        [0.0000000, "#20e6ff"],
        [0.1428571, "#9af8ff"],
        [0.2857143, "#c8feff"],
        [0.4285714, "#e5fcff"],
        [0.5714286, "#ffe7dc"],
        [0.7142857, "#ffc0a8"],
        [0.8571429, "#ff916d"],
        [1.0000000, "#ff744c"]
    ]

    if control_problem:
        xmin = min(min(control_problem.x1), min(control_problem.x2)) - 1
        ymin = xmin
        xmax = max(max(control_problem.x1), max(control_problem.x2)) + 1
        ymax = xmax

    else :
        xmin, ymin, xmax, ymax = 0, 0, 10, 10

    # Create the plot
    x_grid = np.arange(xmin, xmax, 0.2)
    y_grid = np.arange(ymin, ymax, 0.2)
    z_grid = ces_function.eval_rectangle(x_grid, y_grid)

    layout = go.Layout(
        hovermode="closest",
        # legend=dict(x=0, y=-0.01, orientation="h"),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd"},
        width=600,
    )

    if control_problem:

        fig = go.Figure(
            [
            go.Surface(
                contours = {
                    "z": {"show": True, "start": 0.1, "end": 10, "size": 0.5}
                },
                x=x_grid,
                y=y_grid,
                z=z_grid,
                colorscale=cscale,
                opacity=0.8,
                showlegend=False
            ),
            go.Scatter3d(
                y=control_problem.x2,
                x=control_problem.x1,
                z=control_problem.y,
                line=dict(
                    color='darkblue',
                    width=8
                ),
                mode='lines',
                showlegend=False
            ),
            go.Scatter3d( # start point
                y=[control_problem.x2[0]],
                x=[control_problem.x1[0]],
                z=[control_problem.y[0]],
                text=['start'],
                mode='markers+text',
                marker=dict(
                    size=8,
                    color='darkgreen',
                    symbol='cross'
                ),
                textfont=dict(
                    size=18,
                    color="darkgreen"
                ),
                showlegend=False
            ),
            go.Scatter3d( # end point
                y=[control_problem.x2[-1]],
                x=[control_problem.x1[-1]],
                z=[control_problem.y[-1]],
                text=['end'],
                mode='markers+text',
                marker=dict(
                    size=8,
                    color='darkred',
                    symbol='cross'
                ),
                textfont=dict(
                    size=18,
                    color='darkred'
                ),
                showlegend=False
            )
            ],
            layout=layout
        )

    else :
        fig = go.Figure(
            go.Surface(
                contours = {
                    "z": {"show": True, "start": 0.1, "end": 10, "size": 0.5}
                },
                x=x_grid,
                y=y_grid,
                z=z_grid,
                colorscale=cscale
            ),
            layout=layout
        )

    fig.update_layout(
        scene = {
            "xaxis": {"nticks": 20, "title":"x1"},
            "yaxis": {"nticks": 20, "title":"x2"},
            "zaxis": {"nticks": 15, "title":"y"},
            'camera_eye': {"x": -1.2, "y": -1.2, "z": 1.6},
            "aspectratio": {"x": 1, "y": 1, "z": 0.7},
        },
    )

    return pio.to_html(fig, full_html=False)

def serve_CES_quantities_plot(control_problem):

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
    )

    fig.append_trace(go.Scatter(
        x=control_problem.t,
        y=control_problem.x1,
        name='x1'
    ), row=1, col=1)

    fig.append_trace(go.Scatter(
        x=control_problem.t,
        y=control_problem.x2,
        name='x2'
    ), row=1, col=1)

    fig.append_trace(go.Scatter(
        x=control_problem.t,
        y=control_problem.y,
        name='y'
    ), row=1, col=1)

    fig.append_trace(go.Scatter(
        x=control_problem.t,
        y=control_problem.x1 * control_problem.p[0],
        name = 'x1'
    ), row=2, col=1)

    fig.append_trace(go.Scatter(
        x=control_problem.t,
        y=control_problem.x2 * control_problem.p[1],
        name='x2'
    ), row=2, col=1)


    fig.update_xaxes(title_text="t", row=1, col=1)
    fig.update_yaxes(title_text="Quantities", row=1, col=1)
    fig.update_xaxes(title_text="t", row=2, col=1)
    fig.update_yaxes(title_text="Total investments", row=2, col=1)

    fig.update_layout(
        hovermode="closest",
        width=800,
        # legend=dict(x=0, y=-0.01, orientation="h"),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd"})
    

    return pio.to_html(fig, full_html=False)