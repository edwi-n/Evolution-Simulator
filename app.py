#!/usr/bin/env python3

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    print(request.method)
    if request.method == 'POST':
        if request.form['submit'] == 'Open Simulation':
            return app.redirect("/open")
        elif request.form['submit'] == 'Create Simulation':
            return app.redirect("/start")
    elif request.method == 'GET':
        return render_template('index.html')

@app.route("/test")
def reroute():
    return app.redirect("/")

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
