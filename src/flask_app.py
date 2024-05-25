import os
from flask import Flask, render_template
import jinja2# import Environment, FileSystemLoader


from ces import CES
import utils.figures as figs
from config import *

app = Flask(__name__)

# @app.route('/ces_plot')
# def ces_plot():
#     ces_graph_url = build_central_graph(0.5, 3)
#     # todo : make it more modular
#     return render_template(os.path.join(PLOTS_DIR, 'ces_graph.html'))

@app.route('/')
def home():
    ces_graph_url = build_central_graph(0.5, 3)

    # if LOCAL:
    #     ces_graph_url = "file:///" + ces_graph_url

    return render_template('index.html',
        url_ces_graph=ces_graph_url
    )


def build_central_graph(alpha1, rho):
    alpha2 = 1-alpha1
    ces_function = CES(alpha1, alpha2, rho)
    ces_figure = figs.serve_CES_plot_3d(0, 0, 10, 10, ces_function)
    # ces_figure = figs.serve_CES_plot(0, 0, 10, 10, ces_function)
    return ces_figure

if __name__ == '__main__':

    app.run(debug=True)
