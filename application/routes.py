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