import os
from flask import Flask, render_template, jsonify, request
import jinja2# import Environment, FileSystemLoader
import numpy as np

from ces import CES, ControlProblem
import utils.figures as figs
from config import *

app = Flask(__name__)


@app.route('/')
def home():
    ces_graph_url = build_ces_graph(0.5, 3)

    ces_graph_url2 = build_ces_graph(0.7, -2)

    return render_template('index.html',
        url_ces_graph=ces_graph_url,
        url_ces_graph_dynamics=ces_graph_url2
    )

@app.route('/update-plot-ces', methods=['POST'])
def update_plot_ces():
    alpha1 = float(request.form['alpha'])
    rho = float(request.form['rho'])

    # Create an updated Plotly graph
    ces_graph_url = build_ces_graph(alpha1, rho)

    # Convert the Plotly graph to HTML
    return jsonify({'url_ces_graph': ces_graph_url})

@app.route('/update-plot-cesdyn', methods=['POST'])
def update_plot_cesdyn():
    alpha1 = float(request.form['alpha'])
    rho = float(request.form['rho'])

    # Create an updated Plotly graph
    cesdyn_graph_url = build_cesdyn_graph(alpha1, rho)

    # Convert the Plotly graph to HTML
    return jsonify({'url_ces_graph_dynamics': cesdyn_graph_url})


def build_ces_graph(alpha1, rho):
    alpha2 = 1-alpha1
    ces_function = CES(alpha1, alpha2, rho)
    ces_figure = figs.serve_CES_plot_3d(0, 0, 10, 10, ces_function)
    return ces_figure

def build_cesdyn_graph(alpha1, rho):
    pb = ControlProblem(rho=rho, 
                        q0=np.array([1.,1.]),
                        p=np.array([1.,1.]), 
                        I=1., Tf=10)

    pb.solve()

    ces_figure = figs.serve_CES_plot_3d(0, 0, 10, 10, pb.ces, pb)
    return ces_figure

if __name__ == '__main__':

    app.run(debug=True)
