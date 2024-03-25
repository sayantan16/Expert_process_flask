from application import app
from flask import render_template, jsonify, request, current_app
import os
import json
from openai import OpenAI

def make_knowledge_graph_prompt(codeinfo, model):
    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a JSON object creator, who creates relevant topics in the form of knowledge graph based on a problem given by the user.\n\nThe JSON object must have 2 things only:\nA nodes key which has a value of array of different topics and another key called edges which has the source and target between nodes in the form of array.\n\nThe nodes or the topics based on the problem should be like this:\nThe main topic should be based on the most common and high level topic which can branch out to different use cases of the code.\nThe topics should range from programming concepts to uses of the code like this example:\n\nQuestion was based on Linear Regression program written in python, for which the knowledge graph could be:\n\n{\n  \"nodes\": [\n    { \"id\": \"n1\", \"label\": \"Linear Regression\" },\n    { \"id\": \"n2\", \"label\": \"Programming Basics\" },\n    { \"id\": \"n3\", \"label\": \"Machine Learning Basics\" },\n    { \"id\": \"n4\", \"label\": \"Python Syntax\" },\n    { \"id\": \"n5\", \"label\": \"Data Structure\" },\n    { \"id\": \"n6\", \"label\": \"Variables\" },\n    { \"id\": \"n7\", \"label\": \"Functions\" },\n    { \"id\": \"n8\", \"label\": \"Modules\" },\n    { \"id\": \"n9\", \"label\": \"Loops\" },\n    { \"id\": \"n10\", \"label\": \"Testing\" },\n    { \"id\": \"n11\", \"label\": \"Lists\" },\n    { \"id\": \"n12\", \"label\": \"Tuples\" },\n    { \"id\": \"n13\", \"label\": \"Dictionaries\" },\n    { \"id\": \"n14\", \"label\": \"Sets\" },\n    { \"id\": \"n15\", \"label\": \"Dataframes\" },\n    { \"id\": \"n16\", \"label\": \"Model Evaluation\" },\n    { \"id\": \"n17\", \"label\": \"Data Processing\" },\n    { \"id\": \"n18\", \"label\": \"Supervised Learning\" },\n    { \"id\": \"n19\", \"label\": \"Unsupervised Learning\" },\n    { \"id\": \"n20\", \"label\": \"Model Optimization\" }\n  ],\n  \"edges\": [\n    { \"source\": \"n1\", \"target\": \"n2\" },\n    { \"source\": \"n1\", \"target\": \"n3\" },\n    { \"source\": \"n2\", \"target\": \"n4\" },\n    { \"source\": \"n2\", \"target\": \"n5\" },\n    { \"source\": \"n4\", \"target\": \"n6\" },\n    { \"source\": \"n4\", \"target\": \"n7\" },\n    { \"source\": \"n4\", \"target\": \"n8\" },\n    { \"source\": \"n4\", \"target\": \"n9\" },\n    { \"source\": \"n4\", \"target\": \"n10\" },\n    { \"source\": \"n5\", \"target\": \"n11\" },\n    { \"source\": \"n5\", \"target\": \"n12\" },\n    { \"source\": \"n5\", \"target\": \"n13\" },\n    { \"source\": \"n5\", \"target\": \"n14\" },\n    { \"source\": \"n5\", \"target\": \"n15\" },\n    { \"source\": \"n3\", \"target\": \"n16\" },\n    { \"source\": \"n3\", \"target\": \"n17\" },\n    { \"source\": \"n3\", \"target\": \"n18\" },\n    { \"source\": \"n3\", \"target\": \"n19\" },\n    { \"source\": \"n3\", \"target\": \"n20\" }\n  ]\n}\n\nAs you can see that this is the graph json object generated for question from user. Now, for any code question given by the user, generate the same formatted JSON object with nodes and edges."
            },
            {
                "role": "user",
                "content": codeinfo
            }
        ],
        temperature=0,
        max_tokens=900,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content

def make_selected_text_prompt(selected_text, model):
    client = OpenAI()

    response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a detailed explanation generator.\nPlease give a detailed explanation on the user input code snippet.\n\nUnderstand the language of the code and then give as much information in detailed and concise way as you can."
                },
                {
                    "role": "user",
                    "content": selected_text
                }
            ],
            temperature=1,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    explanation = response.choices[0].message.content if response.choices else "No explanation found."
    return explanation

def make_topic_text_prompt(topic, model):
    client = OpenAI()

    response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a detailed explanation generator.\nPlease give a detailed explanation on the user input topic.\n\nGive a detailed explanation on the topic give, the explanation should contain general idea as well as its use-case. How the topic can be used and implemented.\n\nGive a very detailed explanation to the user for gaining expertise on the topic."
                },
                {
                    "role": "user",
                    "content": topic
                }
            ],
            temperature=1,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    explanation = response.choices[0].message.content if response.choices else "No explanation found."
    return explanation

@app.route("/")
@app.route("/index")
@app.route("/#")
def index():
    return render_template("index.html", page_title='Choose a Problem')

@app.route("/code", methods=['GET', 'POST'])
def code():
    if request.method == 'POST':
        text_data = request.form['text']
        response = make_knowledge_graph_prompt(text_data, "gpt-3.5-turbo-0125")
        #print(os.getcwd())
        with open('application/static/jsonFiles/graphData.json', 'w', encoding='utf-8') as json_file:
            json.dump(json.loads(response), json_file)
        return render_template("code.html", text_data=text_data)
    # If it's a GET request, just render the original code page
    return render_template("code.html", page_title='Coding Problem')

@app.route('/graph-data')
def graph_data():
    path_to_file = os.path.join(current_app.root_path, 'static', 'jsonFiles', 'graphData.json')
    with open(path_to_file) as f:
        graph_data = json.load(f)
    return jsonify(graph_data)

@app.route('/explanations', methods=['POST'])
def explanations():
    data = request.get_json()
    topic = data.get('topic')

    try:
        explanation = make_topic_text_prompt(topic, "gpt-3.5-turbo-0125")
    except Exception as e:
        explanation = str(e)

    return jsonify(explanation=explanation)

@app.route('/my-flowchart')
def my_flowchart():
    return render_template('myFlowchart.html')

@app.route('/get_explanation', methods=['POST'])
def get_explanation():
    data = request.get_json()
    selected_text = data.get('selectedText')

    try:
        explanation = make_selected_text_prompt(selected_text, "gpt-3.5-turbo-0125")
    except Exception as e:
        explanation = str(e)

    return jsonify(explanation=explanation)