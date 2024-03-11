from application import app
from flask import render_template, jsonify, request


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
    graph_data = {
    "nodes": [
        {"id": "n1", "label": "Employee Satisfaction"},
        {"id": "n2", "label": "Customer Satisfaction"},
        {"id": "n3", "label": "Innovation and Development"},
        {"id": "n4", "label": "Operational Efficiency"},
        {"id": "n5", "label": "Market Position"},
        {"id": "n6", "label": "Financial Health"},
        {"id": "n7", "label": "Corporate Social Responsibility"}
    ],
    "edges": [
        {"source": "n1", "target": "n2", "label": "Impact on Customer Satisfaction"},
        {"source": "n2", "target": "n5", "label": "Influences Market Position"},
        {"source": "n3", "target": "n4", "label": "Drives Operational Efficiency"},
        {"source": "n4", "target": "n6", "label": "Affects Financial Health"},
        # {"source": "n6", "target": "n1", "label": "Feedback to Employee Satisfaction"},
        {"source": "n7", "target": "n3", "label": "Supports Innovation"},
        {"source": "n5", "target": "n3", "label": "Necessitates Innovation"}
        # The edges here are hypothetical relationships between topics for illustrative purposes.
    ]
}
   

    return jsonify(graph_data)

@app.route('/node-click', methods=['POST'])
def node_click():
    data = request.json
    # Process the node click event here, for example:
    response_text = f"Received click from {data['label']}"
    return jsonify({"text": response_text})

@app.route('/my-flowchart')
def my_flowchart():
    return render_template('myFlowchart.html')