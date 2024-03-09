from application import app
from flask import render_template


@app.route("/")
@app.route("/index")
@app.route("/#")
def index():
    return render_template("index.html")

@app.route("/code")
def code():
    return render_template("code.html")

@app.route("/math")
def math():
    return render_template("math.html")

@app.route("/vis")
def vis():
    return render_template("vis.html")