from flask import Blueprint, render_template, jsonify
import json


diff_visualizer_bp = Blueprint('diff-visualizer', __name__)

@diff_visualizer_bp.route('/diff-visualizer')
def show_diff():
    results = json.load(open('data/ifft_results.json'))
    return render_template('diff_visualizer.html', results_dict=results)

