from flask import Blueprint, render_template, jsonify
import json


output_bp = Blueprint('output', __name__)

@output_bp.route('/output')
def show_output():
    results = json.load(open('data/ifft_results.json'))
    return render_template('output.html', results_dict=results)

