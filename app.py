#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Evolution Simulator"

@app.route("/start")
def start():
    return "Start Simulation\nOpen Simulation"

if(__name__ == "__main__"):
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
