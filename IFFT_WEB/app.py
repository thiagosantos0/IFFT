from flask import Flask, render_template, jsonify
from modules.diff_visualizer import diff_visualizer_bp 
from modules.output import output_bp
from modules.graph import graph_bp
import os
import json
import networkx as nx
import logging
import time


app = Flask(__name__)
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
DATA_FILE = os.path.join(DATA_PATH, 'ifft_results.json')

app.register_blueprint(diff_visualizer_bp)
app.register_blueprint(output_bp)
app.register_blueprint(graph_bp)

@app.route('/welcome')
def welcome():
    # Fetch recent activity timestamp from `ifft_results.json`
    try:
        if os.path.exists(DATA_FILE):
            last_modified = time.ctime(os.path.getmtime(DATA_FILE))
        else:
            last_modified = "No recent activity."
    except Exception as e:
        logging.error(f"Error fetching recent activity: {e}")
        last_modified = "Error fetching recent activity."

    return render_template('welcome.html', last_modified=last_modified)

@app.route('/output-data', methods=['GET'])
def output_data():
    """
    Serve the IFFT results as JSON for the Output visualizer
    """
    try:
        with open(os.path.join(DATA_PATH, 'ifft_results.json'), 'r') as f:
            data = json.load(f)
        return jsonify(data)
    
    except FileNotFoundError:
        return jsonify({"error": "Results file not found"}), 404


@app.route('/graph-data', methods=['GET'])
def graph_data():
    """
        Generate graph data for file dependecies using stored data.
    """
    if not os.path.exists(DATA_FILE):
        print(f"[ERROR] No results file found. Please run IFFT analysis first.")
        return jsonify({"error": "No results file found. Please run IFFT analysis first."}), 404
        
    # Load results from JSON file
    with open(DATA_FILE, "r") as f:
        results = json.load(f)

    print(f"[DEBUG] Results: {results}")

    # Create graph data for nodes and edges
    nodes = set()
    edges = []

    for main_file, blocks in results.items():
        nodes.add(main_file)
        for block in blocks:
            print(f"[DEBUG] Block: {block}")
            associated_file = block.get("associated_file_name")
            if associated_file:
                nodes.add(associated_file)
                edges.append({
                    "from": main_file,
                    "to": associated_file,
                    "label": "Depends on",
                    "font": {
                        'color': '#343a40',
                        'size': 10
                    },
                })

    # Format nodes for Vis.js
    nodes_list = [
    {
        "id": node,
        "label": f"File: {node}" if node.endswith(".py") else f"Block: {node}",
        "color": "#1f78b4" if node.endswith(".py") else "#33a02c",
        "title": f"Python file: {node}" if node.endswith(".py") else f"Dependency block: {node}"
    }
    for node in nodes
]


    return jsonify({"nodes": nodes_list, "edges": edges})


@app.route('/')
def dashboard():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
