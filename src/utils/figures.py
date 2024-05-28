import os

import colorlover as cl
import plotly.graph_objs as go
import plotly.io as pio
import plotly
# import plotly.graph_objects as go
import numpy as np

from config import *

def serve_CES_plot_3d(xmin, ymin, xmax, ymax, ces_function, control_problem=None):
    # Colorscale
    bright_cscale = [[1, "#ff3700"], [0, "#0b8bff"]]
    cscale = [
        [0.0000000, "#20e6ff"],
        [0.1428571, "#9af8ff"],
        [0.2857143, "#c8feff"],
        [0.4285714, "#e5fcff"],
        [0.5714286, "#ffe7dc"],
        [0.7142857, "#ffc0a8"],
        [0.8571429, "#ff916d"],
        [1.0000000, "#ff744c"],
    ]

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
        font={"color": "#a5b1cd"}
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
                colorscale=cscale
            ),
            go.Scatter3d(
                y=control_problem.x2,
                x=control_problem.x1,
                z=control_problem.y,
                # mode='markers',
                marker=dict(
                    size=3,
                    color=control_problem.t,                # set color to an array/list of desired values
                    colorscale='Viridis',   # choose a colorscale
                    opacity=0.8
                )
            )],
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

def serve_CES_plot(xmin, ymin, xmax, ymax, ces_function):
    # Colorscale
    bright_cscale = [[1, "#ff3700"], [0, "#0b8bff"]]
    cscale = [
        [0.0000000, "#20e6ff"],
        [0.1428571, "#9af8ff"],
        [0.2857143, "#c8feff"],
        [0.4285714, "#e5fcff"],
        [0.5714286, "#ffe7dc"],
        [0.7142857, "#ffc0a8"],
        [0.8571429, "#ff916d"],
        [1.0000000, "#ff744c"],
    ]

    # Create the plot
    x_grid = np.arange(xmin, xmax, 0.1)
    y_grid = np.arange(ymin, ymax, 0.1)
    z_grid = ces_function.eval_rectangle(x_grid, y_grid)
    
    trace0 = go.Contour(
        x=x_grid,
        y=y_grid,
        z=z_grid,
        zmin=0,
        zmax=10,
        colorscale=cscale,
        opacity=0.9,
    )

    layout = go.Layout(
        hovermode="closest",
        legend=dict(x=0, y=-0.01, orientation="h"),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd"},
    )

    data = [trace0]#, trace1, trace2, trace3]
    figure = go.Figure(data=data, layout=layout)

    return figure

def serve_CES_marginal_plot(xmin, ymin, xmax, ymax, ces_function):
    # Colorscale
    bright_cscale = [[1, "#ff3700"], [0, "#0b8bff"]]
    cscale = [
        [0.0000000, "#20e6ff"],
        [0.1428571, "#9af8ff"],
        [0.2857143, "#c8feff"],
        [0.4285714, "#e5fcff"],
        [0.5714286, "#ffe7dc"],
        [0.7142857, "#ffc0a8"],
        [0.8571429, "#ff916d"],
        [1.0000000, "#ff744c"],
    ]
    # Create the plot
    # Plot the prediction contour of the SVM
    x_grid = np.arange(xmin, xmax, 0.1)
    y_grid = np.arange(ymin, ymax, 0.1)
    z_grid1, z_grid2 = ces_function.eval_derivatives_rectangle(x_grid, y_grid)
    
    trace1 = go.Contour(
        x=x_grid,
        y=y_grid,
        z=z_grid1,
        # zmin=0,
        # zmax=10,
        colorscale=cscale,
        opacity=0.9,
    )

    trace2 = go.Contour(
        x=x_grid,
        y=y_grid,
        z=z_grid2,
        # zmin=0,
        # zmax=10,
        colorscale=cscale,
        opacity=0.9,
    )

    layout = go.Layout(
        # xaxis=dict(ticks="", showticklabels=False, showgrid=False, zeroline=False),
        # yaxis=dict(ticks="", showticklabels=False, showgrid=False, zeroline=False),
        hovermode="closest",
        legend=dict(x=0, y=-0.01, orientation="h"),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd"},
    )

    data1 = [trace1]#, trace1, trace2, trace3]
    figure1 = go.Figure(data=data1, layout=layout)
    data2 = [trace2]
    figure2 = go.Figure(data=data2, layout=layout)

    return figure1, figure2

def serve_CES_cheaper_plot(xmin, ymin, xmax, ymax, ces_function, ratio_prices):
    # Colorscale
    # bright_cscale = [[1, "#ff3700"], [0, "#0b8bff"]]

    cscale = [
        [0.0000000, "#20e6ff"],
        [0.1428571, "#9af8ff"],
        [0.2857143, "#c8feff"],
        [0.4285714, "#e5fcff"],
        [0.5714286, "#ffe7dc"],
        [0.7142857, "#ffc0a8"],
        [0.8571429, "#ff916d"],
        [1.0000000, "#ff744c"],
    ]
    # Create the plot
    # Plot the prediction contour of the SVM
    x_grid = np.arange(xmin, xmax, 0.1)
    y_grid = np.arange(ymin, ymax, 0.1)
    z_grid = ces_function.eval_cheaper_rectangle(x_grid, y_grid, ratio_prices)
    
    trace = go.Contour(
        x=x_grid,
        y=y_grid,
        z=z_grid.astype(int),
        # zmin=0,
        # zmax=10,
        colorscale=cscale,
        opacity=0.9,
    )

    layout = go.Layout(
        # xaxis=dict(ticks="", showticklabels=False, showgrid=False, zeroline=False),
        # yaxis=dict(ticks="", showticklabels=False, showgrid=False, zeroline=False),
        hovermode="closest",
        legend=dict(x=0, y=-0.01, orientation="h"),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd"},
    )

    data = [trace]
    figure = go.Figure(data=data, layout=layout)

    return figure