from flask import Blueprint, render_template, jsonify
import networkx as nx
import plotly.graph_objects as go
import json
import plotly

graph_bp = Blueprint('graph', __name__)

@graph_bp.route('/graph')
def show_graph():
    
    results = json.load(open('data/ifft_results.json'))
    return render_template('graph.html', results_dict=results)


