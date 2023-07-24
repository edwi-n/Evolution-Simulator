# Change grid size to 1000 x 1000

# If it is not a new simulation, the parameters cannot change


import math
from random import randint
from random import shuffle
import os
import time


class Simulation:
    def __init__(self, populationSize, numberOfIterations, fitnessFunction, dataObject):
        self.globalID = 0
        self.populationSize = populationSize
        self.numberOfIterations = numberOfIterations
        self.fitnessFunction = fitnessFunction
        self.organisms = []
        self.currentIterationNumber = 1
        self.currentIterationData = ""
        self.simulationData = dataObject
        self.simulationSpeed = 1.0
        self.coordinates = {}
        self.gridSize = 100
        self.dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        self.dy = [-1, 0, 1, 1, 1, 0, -1, -1]

    def displayInfo(self):
        print(
            f"Population Size: {self.populationSize}\nTotal Iterations: {self.numberOfIterations}\nFitness Function: {self.fitnessFunction}")

    def displaySimulation(self):
        grid = ["."*self.gridSize]*self.gridSize
        for i in self.organisms:
            currRow = list(grid[i.xCoordinate])
            currRow[i.yCoordinate] = "x"
            grid[i.xCoordinate] = "".join(currRow)
        print("\n".join(grid))

    def geneticAlgorithm(self):
        selectionProcess = []

        # Fitness Function
        for i in self.organisms:
            selectionProcess.append(
                [self.fitnessFunction.performFitnessFunction(i), i.id])

        # Selection
        selectionProcess = sorted(selectionProcess)

        # Reproduction
        newOrganisms = []
        ind = 0
        while ind+1 < self.populationSize:
            newProbability = self.combineGenes(
                self.organisms[ind].genome.actionGenes, self.organisms[ind+1].genome.actionGenes)
            newGenome = Genome(newProbability, [])
            newCoord = self.generateCoordinates()
            self.coordinates[(newCoord)] = True
            newOrganism = Organism(
                self.globalID, newCoord[0], newCoord[1], newGenome)
            self.globalID += 1
            self.organisms.append(newOrganism)
            ind += 2

        for i in range(math.ceil(self.populationSize/2), self.populationSize):
            self.deleteOrganism(selectionProcess[i][1])

    def deleteOrganism(self, id):
        for i in range(len(self.organisms)):
            if (self.organisms[i].id == id):
                del self.organisms[i]
                return True
        return False

    def move(self):
        for i in self.organisms:
            new_probability = self.adjustGenes(i)
            cumulative_probability = [0, 0, 0, 0, 0, 0, 0, 0]
            total_probability = 0

            for j in range(8):
                total_probability += new_probability[j]
                cumulative_probability[j] = total_probability

            moveProbability = randint(0, total_probability)
            for j in range(8):
                if (moveProbability < cumulative_probability[j]):
                    self.coordinates.pop((i.xCoordinate, i.yCoordinate))
                    i.updateCoordinate(
                        i.xCoordinate + self.dx[j], i.yCoordinate + self.dy[j])
                    self.coordinates[(i.xCoordinate, i.yCoordinate)] = True
                    break
                else:
                    continue

    def updateIteration(self, iterationNumber):
        simulation.displaySimulation()
        for i in range(self.gridSize):
            os.system("cls")
            simulation.move()
            print(iterationNumber+1)
            simulation.displaySimulation()
            time.sleep(0.05)

        self.geneticAlgorithm()

        self.coordinates = {}

        for i in self.organisms:
            newCoord = self.generateCoordinates()

            self.coordinates[newCoord] = True
            i.updateCoordinate(newCoord[0], newCoord[1])

    def updateFitnessFunction(self, newFunction):
        self.fitnessFunction = newFunction

    def updateSimulationSpeed(self, newSpeed):
        self.simulationSpeed = newSpeed

    def createOrganism(self, type=-1, xCoordinate=-1, yCoordinate=-1, genomeObject=-1):
        if (type == -1):
            newCoord = self.generateCoordinates()

            self.coordinates[newCoord] = True

            newGenome = Genome(self.createGenes(), [])

            self.globalID += 1
            self.organisms.append(
                Organism(self.globalID-1, newCoord[0], newCoord[1], newGenome))
        else:
            self.coordinates[(xCoordinate, yCoordinate)] = True
            self.globalID += 1

            self.organisms.append(
                Organism(self.globalID-1, xCoordinate, yCoordinate, genomeObject))

    def createGenes(self):
        total_remaining = 100
        initial_probability = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            initial_probability[i] = randint(0, total_remaining)
            total_remaining -= initial_probability[i]

        shuffle(initial_probability)
        return initial_probability

    def adjustGenes(self, organism):
        total_probability = 0

        new_probability = [0, 0, 0, 0, 0, 0, 0, 0]

        for i in range(8):
            newX = organism.xCoordinate + self.dx[i]
            newY = organism.yCoordinate + self.dy[i]

            if (newX < 0 or newX >= self.gridSize or newY < 0 or newY >= self.gridSize):
                continue

            if ((newX, newY) in self.coordinates):
                continue

            new_probability[i] = organism.genome.actionGenes[i]
            total_probability += organism.genome.actionGenes[i]

        return new_probability

    def combineGenes(self, gene1, gene2):
        newGene = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            newGene[i] = math.floor((gene1[i]+gene2[i])/2)
        return newGene

    def validateGenes(self):
        pass

    def generateCoordinates(self):
        newCoord = (randint(0, self.gridSize-1),
                    randint(0, self.gridSize-1))

        while newCoord in self.coordinates:
            newCoord = (randint(0, self.gridSize-1),
                        randint(0, self.gridSize-1))

        return newCoord

    def validateCoordinates(self, xCoordinate, yCoordinate):
        return (xCoordinate, yCoordinate) in self.coordinates

    def decodeGenes(self):
        pass

    def updateDisplay(self):
        # Get available cells, then generate new probability, then randomly generate number and move. Use pseudocode in page 38.
        pass


class Organism:
    def __init__(self, ID, xCoordinate, yCoordinate, genomeObject):
        self.id = ID
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.startCoord = [xCoordinate, yCoordinate]
        self.genome = genomeObject
        self.children = []

    def updateCoordinate(self, xCoordinate, yCoordinate):
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate

    def addChild(self, childObject):
        self.children.append(childObject)

    def getCoordinate(self):
        return (self.xCoordinate, self.yCoordinate)

    def performAction(self):
        pass


class Genome:
    def __init__(self, actionGenes, sensoryGenes):
        self.actionGenes = actionGenes
        self.sensoryGenes = sensoryGenes

    def setActionGenes(self, actionGenes):
        self.actionGenes = actionGenes

    def setSensoryGenes(self, sensoryGenes):
        self.sensoryGenes = sensoryGenes

    def getActionGenes(self):
        return self.actionGenes

    def getSensoryGenes(self):
        return self.sensoryGenes

    def mutateGenes(self):
        pass


class FitnessFunction:
    def __init__(self, fitnessType):
        self.fitnessFunction = fitnessType
        self.locationCoordinates = []

    def setLocation(self, xCoordinate, yCoordinate):
        self.locationCoordinates = [xCoordinate, yCoordinate]

    def getDistanceFromLocation(self, xCoordinate, yCoordinate):
        return math.floor(math.sqrt((xCoordinate-self.locationCoordinates[0])**2+(yCoordinate-self.locationCoordinates[1])**2))

    def performHealthFunc(self, organism):
        pass

    def performFitnessFunction(self, organism):
        if self.fitnessFunction == "health":
            return self.performHealthFunc()
        else:
            return self.getDistanceFromLocation(organism.xCoordinate, organism.yCoordinate)


class SimulationData:
    def __init__(self):
        self.__data = {}

    def setIterationData(self, index, data):
        self.__data[index] = data

    def getIterationData(self, index):
        return self.__data[index]

    def initOrganisms(self, organisms):
        self.__data["organisms"] = organisms

    def getOrganisms(self):
        return self.__data["organisms"]


newSimulation = False
simulationData = SimulationData()

if (newSimulation):
    population_size = int(input("Enter population size: "))
    total_iterations = int(input("Enter the number of iterations: "))
    fitness_function = input("Fitness function: ").lower()

    if fitness_function == "location":
        locationX = int(input("Enter location x coordinate: "))
        locationY = int(input("Enter location y coordinate: "))


else:
    # Get existing simulation data
    population_size = 1000
    total_iterations = 100
    fitness_function = "location"

    if fitness_function == "location":
        locationX = 50
        locationY = 50

    # Update simulationData

fitnessFunction = FitnessFunction(fitness_function)

if (fitness_function == "location"):
    fitnessFunction.setLocation(locationX, locationY)

simulation = Simulation(population_size, total_iterations,
                        fitnessFunction, simulationData)


# if newSimulation:
#     for i in range(population_size):
#         simulation.createOrganism(-1)
# else:
#     allOrganisms = simulationData.getOrganisms()
#     for i in range(population_size):
#         actionGene = allOrganisms[i][3]
#         sensoryGene = allOrganisms[i][4]
#         newGenome = Genome(actionGene, sensoryGene)
#         simulation.createOrganism(1, allOrganisms[i][0], allOrganisms[i][1], allOrganisms[i][2], newGenome)

for i in range(population_size):
    simulation.createOrganism(-1)

for i in range(total_iterations):
    simulation.updateIteration(i)
    time.sleep(1)

# simulation.displayInfo()

# print(simulation.organisms)


# print(simulation.deleteOrganism(2))
