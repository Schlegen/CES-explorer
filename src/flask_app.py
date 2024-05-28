import os
from flask import Flask, render_template, jsonify, request, url_for
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
    x10 = float(request.form['x10'])
    x20 = float(request.form['x20'])
    p1 = float(request.form['p1'])
    p2 = float(request.form['p2'])
    rho = float(request.form['rho'])
    calib_mode = request.form['calib_mode']

    # Create an updated Plotly graph
    cesdyn_graph_url, quantities_graph = build_cesdyn_graph(x10, x20, p1, p2, rho, calib_mode)

    # Convert the Plotly graph to HTML
    return jsonify({'url_ces_graph_dynamics': cesdyn_graph_url,
                    'url_quantities_graph_dynamics' : quantities_graph})

def build_ces_graph(alpha1, rho):
    alpha2 = 1-alpha1
    ces_function = CES.from_alphas(alpha1, alpha2, rho)
    ces_figure = figs.serve_CES_plot_3d(ces_function)
    return ces_figure

def build_cesdyn_graph(x10, x20, p1, p2, rho, calib_mode):

    pb = ControlProblem(rho=rho, 
                        q0=np.array([x10, x20]),
                        p=np.array([p1, p2]), 
                        calib_mode=calib_mode,
                        I=1., Tf=10)
    pb.solve()

    ces_figure = figs.serve_CES_plot_3d(pb.ces, pb)

    quantities_graph = figs.serve_CES_quantities_plot(pb)

    return ces_figure, quantities_graph

if __name__ == '__main__':
    app.run(debug=True)
    # app.add_url_rule('/favicon.ico',
    #              redirect_to=url_for('static', filename='images/favicon.ico'))