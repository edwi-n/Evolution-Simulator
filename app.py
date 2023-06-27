#!/usr/bin/env python3

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    if "open" in request.form:
        app.route("/open")
    elif "close" in request.form:
        return start()
    return render_template("index.html")

@app.route("/start")
def start():
    return render_template("start.html")

@app.route("/open")
def open():
    return render_template("open.html")

@app.route("/simulation")
def simulate():
    return render_template("simulation.html")

@app.route("/end")
def end():
    return render_template("end.html")

if(__name__ == "__main__"):
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
