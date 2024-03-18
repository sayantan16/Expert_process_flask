from application import app
from flask import render_template, jsonify, request, current_app
import os
import json

@app.route("/")
@app.route("/index")
@app.route("/#")
def index():
    return render_template("index.html", page_title='Choose a Problem')

@app.route("/code")
def code():
    return render_template("code.html", page_title='Coding Problem')

@app.route("/math")
def math():
    return render_template("math.html", page_title='Math Problem')

@app.route("/vis")
def vis():
    return render_template("vis.html", page_title='Visualization Problem')

@app.route('/graph-data')
def graph_data():
    path_to_file = os.path.join(current_app.root_path, 'static', 'jsonFiles', 'graphData.json')
    with open(path_to_file) as f:
        graph_data = json.load(f)
    return jsonify(graph_data)

@app.route('/explanations')
def explanations():
    # Construct the path relative to the Flask application instance
    path_to_file = os.path.join(current_app.root_path, 'static', 'jsonFiles', 'explanation.json')
    with open(path_to_file) as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/my-flowchart')
def my_flowchart():
    return render_template('myFlowchart.html')