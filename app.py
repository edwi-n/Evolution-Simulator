#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify
import sys
# sys.path.insert(1, '~/Computer-Science-NEA/simulator')
# import simulation.py
from simulator import simulation
import json
import time
import multiprocessing

app = Flask(__name__)


newSimulation = True
size = -1
numberOfIterations = -1
fitness_function = ""
locationType = ""
simulationData = None
fitnessFunction = None
sim = None
totalCount = 0


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


@app.route("/start", methods=["GET", "POST"])
def start():
    if (request.method == "POST"):
        global size, numberOfIterations, fitness_function, locationType
        size = int(request.form["size"])
        numberOfIterations = int(request.form["iteration"])
        fitness_function = request.form["fitness"]
        locationType = request.form["locationtype"]
        return app.redirect("/simulation")

    return render_template("start.html")


@app.route("/open")
def open():
    # check database or file for simulation data
    global newSimulation, simulationData
    newSimulation = False
    simulationData = None
    return render_template("open.html")


@app.route("/simulation")
def simulate():
    # return str(size)+"\n"+str(numberOfIterations)+"\n"+fitnessFunction
    global newSimultion, numberOfIterations, size, fitness_function, fitnessFunction, simulationData, sim
    if str(numberOfIterations) == "" or str(size) == "" or fitness_function == "":
        return app.redirect("/init-simulation-error")
    if fitness_function == "location" and locationType == "":
        return app.redirect("/init-simulation-error")

    # global newSimulation, size, numberOfIterations, fitness_function, locationType
    if (newSimulation):
        locationCoord = {"north": (0, 50), "east": (
            50, 99), "south": (99, 50), "west": (50, 0)}[locationType]
        fitnessFunction = simulation.FitnessFunction(fitness_function)
        if (fitness_function == "location"):
            fitnessFunction.setLocation(locationCoord[0], locationCoord[1])
        simulationData = simulation.SimulationData(
            int(numberOfIterations), fitness_function)
        sim = simulation.Simulation(
            int(size), int(numberOfIterations), fitnessFunction, simulationData)
        # sim.updateIteration(int(numberOfIterations))
        # data = simulationData.getData()
        data = sim.start()
        # for i in range(numberOfIterations):
        #     data = sim.updateIteration(i+1)
        # print(data)

        # while (int(numberOfIterations) > 0):
        #     numberOfIterations -= 1
        #     sim.updateIteration(numberOfIterations)

        # data = getData()
        # while (data != -1):
        #     # print(data)
        #     data = getData()

        # start = time.time()
        # processes = []
        # for _ in range(numberOfIterations):
        #     p = multiprocessing.Process(
        #         target=sim.updateIteration(numberOfIterations))
        #     p.start()
        #     processes.append(p)

        # for process in processes:
        #     process.join()

        # end = time.time()
        # print(end-start)
        # data = simulationData.getData()
    else:
        data = simulationData.getData()

    return render_template("simulation.html", data=data)


@app.route("/test")
def test():
    data = {'test': 10, 'two': 2, "three": [2, 3]}
    return render_template("test.html", data=data)


@app.route("/get", methods=["GET"])
def getNextIteration():
    global numberOfIterations, sim, simulationData, totalCount
    # print(sim.organisms[size-1].id)
    simulationData.clearMovement()
    simulationData.clearOrganisms()
    if (request.method == "GET"):
        sim.updateIteration(totalCount)
        totalCount += 1
        data = simulationData.getData()
        # print(data)
        return data


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


if (__name__ == "__main__"):
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
