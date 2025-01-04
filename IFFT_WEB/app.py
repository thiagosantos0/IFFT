from flask import Flask, render_template
from modules.diff_visualizer import diff_visualizer_bp 


app = Flask(__name__)
app.register_blueprint(diff_visualizer_bp)

@app.route('/')
def dashboard():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
