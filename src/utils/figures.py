import os

import colorlover as cl
import plotly.graph_objs as go
import plotly.io as pio
import plotly
# import plotly.graph_objects as go
import numpy as np



from config import *

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






def serve_CES_plot_3d(xmin, ymin, xmax, ymax, ces_function):
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


    fig = go.Figure(
        go.Surface(
            contours = {
                # "x": {"show": True, "start": 1.5, "end": 2, "size": 0.04, "color":"white"},
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












def serve_prediction_plot(model, X_train, X_test, y_train, y_test, Z, xx, yy, mesh_step, threshold):
    # Get train and test score from model
    y_pred_train = (model.decision_function(X_train) > threshold).astype(int)
    y_pred_test = (model.decision_function(X_test) > threshold).astype(int)
    train_score = metrics.accuracy_score(y_true=y_train, y_pred=y_pred_train)
    test_score = metrics.accuracy_score(y_true=y_test, y_pred=y_pred_test)

    # Compute threshold
    scaled_threshold = threshold * (Z.max() - Z.min()) + Z.min()
    range = max(abs(scaled_threshold - Z.min()), abs(scaled_threshold - Z.max()))

    # Colorscale
    bright_cscale = [[0, "#ff3700"], [1, "#0b8bff"]]
    cscale = [
        [0.0000000, "#ff744c"],
        [0.1428571, "#ff916d"],
        [0.2857143, "#ffc0a8"],
        [0.4285714, "#ffe7dc"],
        [0.5714286, "#e5fcff"],
        [0.7142857, "#c8feff"],
        [0.8571429, "#9af8ff"],
        [1.0000000, "#20e6ff"],
    ]

    # Create the plot
    # Plot the prediction contour of the SVM
    trace0 = go.Contour(
        x=np.arange(xx.min(), xx.max(), mesh_step),
        y=np.arange(yy.min(), yy.max(), mesh_step),
        z=Z.reshape(xx.shape),
        zmin=scaled_threshold - range,
        zmax=scaled_threshold + range,
        hoverinfo="none",
        showscale=False,
        contours=dict(showlines=False),
        colorscale=cscale,
        opacity=0.9,
    )

    # Plot the threshold
    trace1 = go.Contour(
        x=np.arange(xx.min(), xx.max(), mesh_step),
        y=np.arange(yy.min(), yy.max(), mesh_step),
        z=Z.reshape(xx.shape),
        showscale=False,
        hoverinfo="none",
        contours=dict(
            showlines=False, type="constraint", operation="=", value=scaled_threshold
        ),
        name=f"Threshold ({scaled_threshold:.3f})",
        line=dict(color="#708090"),
    )

    # Plot Training Data
    trace2 = go.Scatter(
        x=X_train[:, 0],
        y=X_train[:, 1],
        mode="markers",
        name=f"Training Data (accuracy={train_score:.3f})",
        marker=dict(size=10, color=y_train, colorscale=bright_cscale),
    )

    # Plot Test Data
    trace3 = go.Scatter(
        x=X_test[:, 0],
        y=X_test[:, 1],
        mode="markers",
        name=f"Test Data (accuracy={test_score:.3f})",
        marker=dict(
            size=10, symbol="triangle-up", color=y_test, colorscale=bright_cscale
        ),
    )

    layout = go.Layout(
        xaxis=dict(ticks="", showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(ticks="", showticklabels=False, showgrid=False, zeroline=False),
        hovermode="closest",
        legend=dict(x=0, y=-0.01, orientation="h"),
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd"},
    )

    data = [trace0, trace1, trace2, trace3]
    figure = go.Figure(data=data, layout=layout)

    return figure


def serve_roc_curve(model, X_test, y_test):
    decision_test = model.decision_function(X_test)
    fpr, tpr, threshold = metrics.roc_curve(y_test, decision_test)

    # AUC Score
    auc_score = metrics.roc_auc_score(y_true=y_test, y_score=decision_test)

    trace0 = go.Scatter(
        x=fpr, y=tpr, mode="lines", name="Test Data", marker={"color": "#13c6e9"}
    )

    layout = go.Layout(
        title=f"ROC Curve (AUC = {auc_score:.3f})",
        xaxis=dict(title="False Positive Rate", gridcolor="#2f3445"),
        yaxis=dict(title="True Positive Rate", gridcolor="#2f3445"),
        legend=dict(x=0, y=1.05, orientation="h"),
        margin=dict(l=100, r=10, t=25, b=40),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd"},
    )

    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure


def serve_pie_confusion_matrix(model, X_test, y_test, Z, threshold):
    # Compute threshold
    scaled_threshold = threshold * (Z.max() - Z.min()) + Z.min()
    y_pred_test = (model.decision_function(X_test) > scaled_threshold).astype(int)

    matrix = metrics.confusion_matrix(y_true=y_test, y_pred=y_pred_test)
    tn, fp, fn, tp = matrix.ravel()

    values = [tp, fn, fp, tn]
    label_text = ["True Positive", "False Negative", "False Positive", "True Negative"]
    labels = ["TP", "FN", "FP", "TN"]
    blue = cl.flipper()["seq"]["9"]["Blues"]
    red = cl.flipper()["seq"]["9"]["Reds"]
    colors = ["#13c6e9", blue[1], "#ff916d", "#ff744c"]

    trace0 = go.Pie(
        labels=label_text,
        values=values,
        hoverinfo="label+value+percent",
        textinfo="text+value",
        text=labels,
        sort=False,
        marker=dict(colors=colors),
        insidetextfont={"color": "white"},
        rotation=90,
    )

    layout = go.Layout(
        title="Confusion Matrix",
        margin=dict(l=50, r=50, t=100, b=10),
        legend=dict(bgcolor="#282b38", font={"color": "#a5b1cd"}, orientation="h"),
        plot_bgcolor="#282b38",
        paper_bgcolor="#282b38",
        font={"color": "#a5b1cd"},
    )

    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure