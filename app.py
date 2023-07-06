#!/usr/bin/env python3

from flask import Flask, render_template, request
import sys
# sys.path.insert(1, '~/Computer-Science-NEA/simulator')
# import simulation.py
from simulator import simulation

app = Flask(__name__)


size = -1
numberOfIterations = -1
fitnessFunction = ""

@app.route("/", methods=["GET", "POST"])
def index():
    print(request.method)
    if request.method == 'POST':
        if request.form['submit'] == 'Open Simulation':
            return app.redirect("/open")
        elif request.form['submit'] == 'New Simulation':
            return app.redirect("/start")
    elif request.method == 'GET':
        return render_template('index.html')

@app.route("/test")
def reroute():
    return app.redirect("/")

@app.route("/start", methods=["GET", "POST"])
def start():
    if(request.method == "POST"):
       global size, numberOfIterations, fitnessFunction
       size = request.form["size"]
       numberOfIterations = request.form["iteration"]
       fitnessFunction = request.form["fitness"]
       return app.redirect("/simulation")

    return render_template("start.html")

@app.route("/open")
def open():
    return render_template("open.html")

@app.route("/simulation")
def simulate():
    # return str(size)+"\n"+str(numberOfIterations)+"\n"+fitnessFunction
    if str(numberOfIterations) == "" or str(size) == "" or fitnessFunction == "":
        return app.redirect("/init-simulation-error")
    return render_template("simulation.html")

@app.route("/init-simulation-error")
def init_simulation_error():
    error = ""
    if str(numberOfIterations) == "" or numberOfIterations < 1 or numberOfIterations > 1000:
        error += "Number of Iterations have to be > 0 and < 1000\n"
    if str(size) == "" or size < 1 or size > 10000:
        error += "Population Size has to be > 0 and < 10000\n"

    return error


@app.route("/end")
def end():
    return render_template("end.html")

if(__name__ == "__main__"):
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
