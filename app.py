#!/usr/bin/env python3

from flask import send_file
from flask import Flask, render_template, request, redirect
from simulator import simulation
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

app = Flask(__name__)

simulations = {}
simulationDataClasses = {}
entireSimulationData = {}
database = simulation.Database()
uniqueId = 1


@app.route("/", methods=["GET"])
def index():
    """
    Handle the index route of the application.
    The request method can only be GET.
    Render the index.html template.
    """
    return render_template('index.html')


@app.route("/start", methods=["GET", "POST"])
def start():
    """
    Handles the route to start a new simulation.
    If the request method is POST, process the form data and create a new simulation.
    If the request method is GET, render the start.html template with empty data.

    Returns:
        If the request method is POST and the form data is valid, redirect to the simulation page.
        If the request method is POST and the form data is invalid, render the start.html template with error messages.
        If the request method is GET, render the start.html template with empty data.
    """
    if (request.method == "POST"):
        global uniqueId, simulations, simulationDataClasses

        # Try to convert the form data to integers, if not possible, set the values to -1
        try:
            size = int(request.form["size"])
        except ValueError:
            size = -1
        try:
            numberOfIterations = int(request.form["iteration"])
        except ValueError:
            numberOfIterations = -1
        locationType = request.form["locationtype"]
        try:
            mutationRate = int(request.form["mutation"])
        except ValueError:
            mutationRate = -1

        error = ""

        # Checks if the data is in the correct range, otherwise update the error message.
        # If the conversion failed previously, the value will be -1, which is not in the range.
        if numberOfIterations < 1 or numberOfIterations > 100:
            numberOfIterations = -1
            error += "Number of Iterations has to be an integer between 1 and 100. "

        if size < 1 or size > 1000:
            size = -1
            error += "Population Size has to be an integer between 1 and 1000. "

        if (mutationRate < 0 or mutationRate > 100):
            mutationRate = -1
            error += "Mutation Probability has to be an integer between 0% and 100%. "

        # If there are any errors, render the start.html template with the error messages
        if (error != ""):
            return render_template("start.html", data={"size": size, "iterationCount": numberOfIterations, "location": locationType, "mutationRate": mutationRate, "error": error})

        # Determine the coordinates based on the selected location type
        locationCoord = {"north": (0, 50), "east": (
            50, 99), "south": (99, 50), "west": (50, 0), "sw": (99, 0), "se": (99, 99), "ne": (0, 99), "nw": (0, 0)}[locationType]

        # Create the fitness function and simulation data objects
        fitnessFunction = simulation.FitnessFunction()
        fitnessFunction.setLocation(locationCoord[0], locationCoord[1])
        simulationData = simulation.SimulationData(
            int(numberOfIterations), int(size), locationCoord)

        # Create a new simulation object
        newSimulation = simulation.Simulation(
            int(size), mutationRate, fitnessFunction, simulationData)

        # Store the simulation and simulation data objects in dictionaries using a unique ID,
        # this is so that the Simulation and SimulationData objects can be retrieved later using its unique id.
        simulations[uniqueId] = newSimulation
        simulationDataClasses[uniqueId] = simulationData
        # Increment the unique ID for the next simulation
        uniqueId += 1

        # Redirect to the simulation page
        return redirect(f"/simulation/{uniqueId-1}")

    # Render the start.html template with empty data
    return render_template("start.html", data={})


@app.route("/open", methods=["GET"])
def open_file():
    """
    Handles the route to open an existing simulation.
    The request method can only be GET.
    Render the open.html template.

    Returns:
        The rendered open.html template.
    """
    return render_template("open.html", data={})


@app.route('/oldSimulation', methods=['POST'])
def uploadSimulation():
    """
    Handles the route to open an existing simulation as a file.
    Uploads a simulation file, validates it and then renders the simulation page.
    The request method can only be POST.

    Returns:
        A rendered template for the simulation page if the file is valid.
        Otherwise, a rendered template for the open.html page.
    """
    if request.method == 'POST':
        global uniqueId, simulationDataClasses

        # Save the uploaded file as "newSimulation.json"
        f = request.files['file']
        f.save("newSimulation.json")

        # Load the data from the saved file and convert the json to a dictionary
        with open("newSimulation.json", "r") as openfile:
            data = json.load(openfile)

        try:
            # Create a SimulationData object using the loaded data
            # Checks if all the required keys are present in the dictionary
            simulationData = simulation.SimulationData(
                int(data["iterationCount"]), int(data["populationSize"]), (data["location"][0], data["location"][1]))
        except KeyError:
            # Return an error message if the file is invalid
            return render_template("open.html", data={"error": "Invalid File. Please try again."})

        # Upload the data to the SimulationData object
        if not simulationData.uploadData(data):
            # Return an error message if simulation.uploadData() returns False
            return render_template("open.html", data={"error": "Invalid File. Please try again."})

        # Store the SimulationData object in a dictionary with a unique ID
        simulationDataClasses[uniqueId] = simulationData

        # Update the data dictionary with simulation type and ID
        data["simulationType"] = 0
        data["id"] = uniqueId

        # Increment the unique ID for the next simulation
        uniqueId += 1

        # Render the simulation template with the updated data
        return render_template("simulation.html", data=data)


@app.route("/oldSimulationDB", methods=['POST'])
def dbSimulation():
    """
    Handles the route to open an existing simulation from the database.
    Retrieves simulation data from the database and renders the simulation page.
    The request method can only be POST.

    Returns:
        If the simulation data is found in the database, returns the rendered 'simulation.html' template.
        Otherwise, returns a string indicating the failure to open the simulation.
    """
    global uniqueId

    if request.method == 'POST':
        name = request.form["name"]

        # Check if the simulation exists in the database
        if (database.checkForSimulation(name)):
            # Retrieve the simulation data from the database
            data = database.getSimulation(name)

            # Create a SimulationData object and upload the retrieved data
            simulationData = simulation.SimulationData(
                int(data["iterationCount"]), int(data["populationSize"]))
            simulationData.uploadData(data)

            # Store the SimulationData object in a dictionary with a unique ID
            simulationDataClasses[uniqueId] = simulationData

            # The simulation type is 0 because it is an existing simulation
            data["simulationType"] = 0
            data["id"] = uniqueId

            # Increment the unique ID for the next simulation
            uniqueId += 1

            # Render the 'simulation.html' template and pass the data dictionary
            return render_template("simulation.html", data=data)

    # Return a failure message if the simulation data is not found
    return "Failed to open simulation"


@app.route("/simulation/<id>", methods=["GET"])
def simulate(id):
    """
    Starts a simulation with the given ID and renders the simulation page if the ID is valid.
    The request method can only be GET.

    Parameters:
        id (int): The unique ID of the simulation to be simulated.

    Returns:
        render_template: The rendered template for the simulation.
    """

    global simulations

    # Convert the ID to an integer
    try:
        id = int(id)
    except ValueError:
        # If the ID is not an integer, render the 404 page
        return render_template("404.html"), 404

    # Check if the ID exists in the simulations dictionary
    try:
        newSimulation = simulations[id]
    except KeyError:
        # If the ID does not exist, render the 404 page
        return render_template("404.html"), 404

    # Start the simulation and retrieve the data
    data = newSimulation.start()

    # SimulationType 1 indicates that the simulation is a new simulation.
    data["simulationType"] = 1
    data["id"] = id

    # Render the simulation page and pass the data dictionary
    return render_template("simulation.html", data=data)


@app.route("/get/<id>", methods=["GET"])
def getNextIteration(id):
    """
    Retrieves the next iteration data for a given simulation ID.
    The request method can only be GET.

    Args:
        id (int): The ID of the simulation.

    Returns:
        str: The data for the next iteration.
    """
    global simulations, simulationDataClasses

    # Convert the ID to an integer
    try:
        uniqueId = int(id)
    except ValueError:
        return render_template("404.html"), 404

    # Check if the ID exists in the simulations dictionary and simulationDataClasses dictionary
    try:
        newSimulation = simulations[int(uniqueId)]
        simulationData = simulationDataClasses[int(uniqueId)]
    except KeyError:
        return render_template("404.html"), 404

    # Clear the current data in the simulationData object
    # This is so that the data from the previous iterations is not included in the response
    simulationData.clearMovement()
    simulationData.clearOrganisms()
    # Perform the next iteration
    newSimulation.updateIteration()
    # Retrieve the data for the next iteration
    data = simulationData.getData()
    # Return the data as a dictionary
    return data


@app.route("/summary/<id>", methods=["GET"])
def viewSummary(id):
    """
    Renders a summary page for a given ID.

    Args:
        id (str): The ID of the summary to be viewed.

    Returns:
        render_template: The rendered summary page.
    """
    # Convert the ID to an integer
    try:
        id = int(id)
    except ValueError:
        return render_template("404.html"), 404
    global simulationDataClasses, entireSimulationData
    # Check if the ID exists in the simulationDataClasses dictionary
    try:
        data = entireSimulationData[id]
        iterationNumber = []
        varianceData = []

        # Calculate variance for each iteration
        for i in range(data["iterationCount"]):
            # A list of genomes for each organism in the iteration
            variance = []
            for j in data["organismsInIteration"][i]:
                variance.append(data["organisms"][j][1])
            iterationNumber.append(i+1)
            # Calculate the variance for all the genomes in the iteration
            varianceData.append(np.sum(np.var(variance, axis=0)))

        fitnessData = []
        # Retrieve the location coordinates
        location_x = data["location"][0]
        location_y = data["location"][1]

        # Calculate fitness score for each iteration
        for i in range(data["iterationCount"]):
            # data[iterations][i] is in the format [[organismID, [x, y]], [organismID, [x, y]], ..., ...]
            iterationData = data["iterations"][i]
            # Calculates the total number of moves in the iteration
            totalSteps = len(iterationData)
            # The score sum is the total distance from the fitness location to all the organisms in the iteration
            scoreSum = 0
            # Calculate the distance from the fitness location to each organism in the iteration
            for j in range(data["populationSize"]):
                # iterationData[j] is in the format [organismID, [x, y]]
                coordinates = iterationData[totalSteps-j-1][1]
                # Calculate the distance using the distance formula.
                distance = (coordinates[0]-location_x)**2 + \
                    (coordinates[1]-location_y)**2
                # Add the distance to the total score
                scoreSum += distance
            # Append the average score (total score/number of organisms) to the fitnessData list
            fitnessData.append(scoreSum/data["populationSize"])

    except KeyError:
        # If the ID does not exist, render the 404 page
        return render_template("404.html"), 404

    # Plot the variance graph
    # Sets the y-axis ticks to be between 0 and 1
    plt.ylim(0, 1)
    if (len(iterationNumber) == 1):
        # If there is only one iteration, plot a single point
        plt.plot(iterationNumber, varianceData, "o")
    else:
        # Plot the graph with iterationNumber as the x-axis and varianceData as the y-axis
        plt.plot(iterationNumber, varianceData)
    # Set the x-axis label to "Iteration"
    plt.xlabel("Iteration")
    # Set the y-axis label to "Variance"
    plt.ylabel("Variance")
    # Save the plot as a png file in the static folder with the name "summary.png"
    plt.savefig("static/summary.png")

    # Plot the fitness score graph
    # Clears the current plot
    plt.clf()
    if (len(iterationNumber) == 1):
        # Plot a single point if there is only one iteration
        plt.plot(iterationNumber, fitnessData, "o")
    else:
        # Plot the graph with iterationNumber as the x-axis and fitnessData as the y-axis
        plt.plot(iterationNumber, fitnessData)
    # Label the x-axis as "Iteration"
    plt.xlabel("Iteration")
    # Label the y-axis as "Fitness Score"
    plt.ylabel("Fitness Score")
    # Save the plot as a png file in the static folder with the name "summary2.png"
    plt.savefig("static/summary2.png")
    plt.clf()
    # Render the summary.html template and pass in the id
    return render_template("summary.html", data={"id": id})


@app.route("/savesimulation/<id>", methods=["GET"])
def saveSimulation(id):
    """
    Renders the 'savesimulation.html' template with the provided simulation ID.

    Args:
        id (int): The ID of the simulation.

    Returns:
        str: The rendered HTML template.
    """
    # Convert the ID to an integer
    try:
        id = int(id)
    except ValueError:
        return render_template("404.html"), 404
    # Render the 'savesimulation.html' template with the ID
    return render_template("savesimulation.html", data={"id": id})


@app.route("/database/<id>")
def saveInDatabase(id):
    """
    This function saves the given ID in the database and renders the 'database.html' template.

    Parameters:
        id (str): The ID to be saved in the database.

    Returns:
        str: The rendered 'database.html' template with the data dictionary.

    """
    # Convert the ID to an integer
    try:
        id = int(id)
    except ValueError:
        return render_template("404.html"), 404
    # Render the 'database.html' template with the ID
    return render_template("database.html", data={"id": id})


@app.route("/downloadSimulation/<id>", methods=["GET"])
def downloadSimulation(id):
    global entireSimulationData
    # Convert the ID to an integer
    try:
        id = int(id)
    except ValueError:
        return render_template("404.html"), 404
    with open("simulation.json", "w") as outfile:
        # Check if the ID exists in the entireSimulationData dictionary
        try:
            # Convert the dictionary into a json file named "simulation.json"
            json.dump(entireSimulationData[id], outfile)
        except KeyError:
            return render_template("404.html"), 404

    # Downloads the file "simulation.json"
    return send_file(os.getcwd()+"\\simulation.json", as_attachment=True)


@app.route("/checkSimulation/<name>", methods=['GET'])
def checkIfSimulationExists(name):
    # Check if the simulation exists in the database
    # database.checkForSimulation() returns True if the simulation exists, otherwise False
    result = database.checkForSimulation(name)
    return {"valid": result}


@app.route("/verifyPassword", methods=['POST'])
def verifyDatabasePassword():
    # databaseInfo is a dictionary containing the simulation name and password
    databaseInfo = request.json
    simulationName = databaseInfo["name"]
    simulationPassword = databaseInfo["password"]
    # database.verifyPassword() returns True if the password is correct, otherwise False
    result = database.verifyPassword(simulationName, simulationPassword)
    return {"valid": result}


@app.route("/checkPublic/<name>", methods=['GET'])
def checkSimulationPublic(name):
    # database.isPublic() returns True if the simulation is public, otherwise False
    result = database.isPublic(name)
    return {"valid": result}


@app.route("/dbsave", methods=['POST'])
def dbSave():
    global entireSimulationData
    # Parse the data from the request
    databaseInfo = request.json
    simulationName = databaseInfo["name"]
    simulationPassword = databaseInfo["password"]
    isPrivate = databaseInfo["isPrivate"]
    id = databaseInfo["uniqueId"]
    # Check if the ID exists in the entireSimulationData dictionary
    try:
        entireSimulationData[id]
    except KeyError:
        return {"valid": False}

    # Check if the simulation exists in the database
    if (database.checkForSimulation(simulationName)):
        # Simulation exists, so remove the old simulation from the database
        database.removeSimulation(simulationName)

    # Inserts the current simulation into the database
    database.insertSimulation(
        simulationName, simulationPassword, isPrivate, entireSimulationData[id])

    # Successfully saved the simulation
    return {"valid": True}


@app.route("/updateEntireData/<id>", methods=['POST'])
def updateEntireData(id):
    global entireSimulationData
    # Convert the ID to an integer
    try:
        id = int(id)
    except ValueError:
        return render_template("404.html"), 404
    # Store all of the simulation data in the entireSimulationData dictionary
    entireSimulationData[id] = json.loads(request.json)
    return {"valid": True}


@app.route("/end/<id>", methods=['GET'])
def end(id):
    # Convert the ID to an integer
    try:
        id = int(id)
    except ValueError:
        return render_template("404.html"), 404
    # Render the 'end.html' template with the ID
    return render_template("end.html", data={"id": id})


@app.errorhandler(404)
def pageNotFound(error):
    # Render the 404.html template
    return render_template("404.html"), 404


# Run the server
if (__name__ == "__main__"):
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
