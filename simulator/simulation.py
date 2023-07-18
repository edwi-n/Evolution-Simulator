# Change grid size to 1000 x 1000

# If it is not a new simulation, the parameters cannot change


import math
from random import randint

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

    def displayInfo(self):
        print(f"Population Size: {self.populationSize}\nTotal Iterations: {self.numberOfIterations}\nFitness Function: {self.fitnessFunction}")

    def displaySimulation(self):
        grid = ["."*100]*100
        for i in self.organisms:
            currRow = list(grid[i.xCoordinate])
            currRow[i.yCoordinate] = "x"
            grid[i.xCoordinate] = "".join(currRow)
        print("\n".join(grid))

    def geneticAlgorithm(self):
        pass

    def deleteOrganism(self, id):
        for i in range(len(self.organisms)):
            if(self.organisms[i].id == id):
                del self.organisms[i]
                return True
        return False

    def updateIteration(self):
        pass

    def updateFitnessFunction(self, newFunction):
        self.fitnessFunction = newFunction

    def updateSimulationSpeed(self, newSpeed):
        self.simulationSpeed = newSpeed

    def createOrganism(self, type = -1, xCoordinate = -1, yCoordinate = -1, genomeObject = -1):
        if(type == -1):
            newCoord = (randint(0, 99), randint(0, 99))

            while newCoord in self.coordinates:
                newCoord = (randint(0, 99), randint(0, 99))

            self.coordinates[newCoord] = True
            newGenome = Genome(self.createGenes(), [])
            self.globalID += 1
            self.organisms.append(Organism(self.globalID-1, newCoord[0], newCoord[1], newGenome))
        else:
            self.coordinates[(xCoordinate, yCoordinate)] = True
            self.globalID += 1

            self.organisms.append(Organism(self.globalID-1, xCoordinate, yCoordinate, genomeObject))

    def createGenes(self):
        total_remaining = 100
        initial_probability = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            initial_probability[i] = randint(0, total_remaining)
            total_remaining -= initial_probability[i]
        return initial_probability

    def validateGenes(self):
        pass

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

    def performLocationFunc(self):
        pass

    def performHealthFunc(self):
        pass

    def performFitnessFunction(self):
        if self.fitnessFunction == "health":
            pass


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

if(newSimulation):
    population_size = int(input("Enter population size: "))
    total_iterations = int(input("Enter the number of iterations: "))
    fitness_function = input("Fitness function: ").lower()
else:
    # Get existing simulation data
    population_size = 1000
    total_iterations = 100
    fitness_function = "health"

    # Update simulationData

simulation = Simulation(population_size, total_iterations, fitness_function, simulationData)

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


# simulation.displayInfo()

# print(simulation.organisms)
simulation.displaySimulation()

# print(simulation.deleteOrganism(2))


