from flask import Flask, render_template, jsonify
from modules.diff_visualizer import diff_visualizer_bp 
import os
import json


app = Flask(__name__)
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')

app.register_blueprint(diff_visualizer_bp)

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
    Serve graph-compatible data based on the IFFT results.
    """
    try:
        with open(os.path.join(DATA_PATH, "ifft_results.json"), "r") as f:
            results = json.load(f)

        nodes = []
        edges = []

        for file, blocks in results.items():
            nodes.append({"id": file, "label": file, "color": "#1f78b4"})

            for block in blocks:
                block_label = block["associated_file_label"]
                associated_file = block["associated_file_name"]

                nodes.append({"id": block_label, "label": block_label, "color": "#33a02c"})
                edges.append({"from": file, "to": block_label, "label": "contains"})
                nodes.append({"id": associated_file, "label": associated_file, "color": "#1f78b4"})
                edges.append({"from": block_label, "to": associated_file, "label": "depends on"})

        return jsonify({"nodes": nodes, "edges": edges})
    except FileNotFoundError:
        return jsonify({"error": "Results file not found."}), 404

@app.route('/')
def dashboard():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
