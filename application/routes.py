from application import app
from flask import render_template, jsonify, request, current_app
import os
import json
import openai as OpenAI

def make_prompt(codeinfo, model):
    from openai import OpenAI
    
    client = OpenAI(api_key="")

    response = client.chat.completions.create(
    model=model,
    messages=[
        {
        "role": "system",
        "content": "Create a JSON knowledge graph containing programming topics that are related to the code snippet given by the user. Create nodes for each relevant programming topic you can identify, also create nodes for programming topics related to other nodes, use this format for the knowledge graph and return your answer in a JSON format:\n{\n  \"nodes\": [\n    { \"id\": \"n1\", \"label\": \"Linear Regression\" },\n    { \"id\": \"n2\", \"label\": \"Programming Basics\" },\n    { \"id\": \"n3\", \"label\": \"Machine Learning Basics\" },\n    { \"id\": \"n4\", \"label\": \"Python Syntax\" },\n    { \"id\": \"n5\", \"label\": \"Data Structure\" }\n  ],\n  \"edges\": [\n    { \"source\": \"n1\", \"target\": \"n2\" },\n    { \"source\": \"n1\", \"target\": \"n3\" },\n    { \"source\": \"n2\", \"target\": \"n4\" },\n    { \"source\": \"n2\", \"target\": \"n5\" }\n  ]\n}\n\n"
        },
        {
        "role": "user",
        "content": codeinfo
        }
    ],
    temperature=1,
    max_tokens=724,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response.choices[0].message.content


@app.route("/")
@app.route("/index")
@app.route("/#")
def index():
    return render_template("index.html", page_title='Choose a Problem')

@app.route("/code", methods=['GET', 'POST'])
def code():
    if request.method == 'POST':
        
        text_data = request.form['text']
        response = make_prompt(text_data, "gpt-3.5-turbo-0125")
        #print(os.getcwd())
        with open('application/static/jsonFiles/graphData.json', 'w', encoding='utf-8') as json_file:
                json.dump(json.loads(response), json_file)
        return render_template("code.html", text_data=text_data)
    # If it's a GET request, just render the original code page
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