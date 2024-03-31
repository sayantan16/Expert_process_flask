from application import app
from flask import render_template, jsonify, request, current_app
import os
import json
from openai import OpenAI

CodeSnippet=""

def make_knowledge_graph_prompt(codeinfo, model):
    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        response_format={ "type": "json_object" },
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

def make_topic_text_prompt(topic_name, code_snippet, knldg_graph, model):
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        response_format={ "type": "json_object" },
        messages=[
            {
                "role": "system",
                "content": "Please generate a JSON response detailing a topic related to the user's provided code. The response should follow this structure:\n\nUser input will have:\n1. Topic Name\n2. Input Code Snippet\n3. Knowledge Graph\n\n{\n  \"Topic Name\": \"Specify the topic chosen by the user.\",\n  \"General Concept\": \"Provide a succinct overview of the topic, using minimum 500 words.\",\n  \"Relevant Lines\": {\n    \"line number\": \"Explain how the topic relates to this specific line of code.\"\n  },\n  \"Graph Hyperlinks\": [\"Related topic 1\", \"Related topic 2\"],\n  \"Wider Topics Hyperlinks\": [\"Extended topic 1\", \"Extended topic 2\", \"Extended topic 3\"]\n}\n\nGuidelines for each section:\n\n- Topic Name: Enter the topic selected by the user.\n- General Concept: Offer a brief and clear description of the concept.\n- Relevant Lines: Create a dictionary with line numbers and their corresponding explanations, focusing on the topic's relevance to the code.\n- Graph Hyperlinks: Include 2-3 topics closely related to the main topic, as found in the knowledge graph.\n- Wider Topics Hyperlinks: Suggest 3-4 additional topics not in the knowledge graph but relevant for broader understanding or further exploration.\n\nRemember to tailor the response to the user's input, following the JSON format provided."
            },
            {
                "role": "user",
                "content": f"1. Topic Name - {topic_name}\n2. Input Code Snippet - {code_snippet}\n3. Knowledge Graph - {knldg_graph}"
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    explanation = response.choices[0].message.content if response.choices else "No explanation found."
    return explanation

def update_knowledge_graph(topic, model):
    client = OpenAI()
    with open('application/static/jsonFiles/graphData.json', 'r', encoding='utf-8') as json_file:
        currentGraph = json.dumps(json.load(json_file))
    response = client.chat.completions.create(
    model=model,
    messages=[
        {
        "role": "system",
        "content": f"Take the JSON formatted knowledge graph inputted by the user and add more nodes related to this topic: {topic}, include edges to other relevant topics. Return the updated json in the same format"
        },
        {
            "role": "user",
            "content": currentGraph
        }
    ],
    temperature=1,
    max_tokens=800,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    #print(response)
    explanation = response.choices[0].message.content if response.choices else "No explanation found."
    #print('updated graph',explanation)
    with open('application/static/jsonFiles/graphData.json', 'w', encoding='utf-8') as json_file:
            json.dump(json.loads(explanation), json_file)
    return explanation

@app.route("/")
@app.route("/index")
@app.route("/#")
def index():
    return render_template("index.html", page_title='Choose a Problem')

@app.route("/code", methods=['GET', 'POST'])
def code():
    global CodeSnippet
    if request.method == 'POST':
        text_data = request.form['text']
        CodeSnippet = text_data
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
    topic_name = data.get('topic')

    global CodeSnippet
    code_snippet = CodeSnippet

    path_to_file = os.path.join(current_app.root_path, 'static', 'jsonFiles', 'graphData.json')
    with open(path_to_file) as f:
        graph_data = json.load(f)  # This loads the graph data into a dictionary
    # Convert the dictionary back to a JSON-formatted string
    knldg_graph = json.dumps(graph_data)

    try:
        explanation = make_topic_text_prompt(topic_name, code_snippet, knldg_graph, "gpt-3.5-turbo-0125")
        # update_knowledge_graph(topic, "gpt-3.5-turbo-0125")
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

@app.route('/update_and_explain', methods=['POST'])
def update_and_explain():
    data = request.get_json()
    topic_name = data.get('topic')

    try:
        # Assuming update_knowledge_graph now also returns the updated graph data
        updated_graph = update_knowledge_graph(topic_name, "gpt-3.5-turbo-0125")
        explanation = make_topic_text_prompt(topic_name, CodeSnippet, updated_graph, "gpt-3.5-turbo-0125")
        return jsonify(explanation=explanation, graph=updated_graph)
    except Exception as e:
        return jsonify(error=str(e)), 500
