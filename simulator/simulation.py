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
        pass

    def geneticAlgorithm(self):
        pass

    def addOrganism(self):
        pass

    def deleteOrganism(self):
        pass

    def updateIteration(self):
        pass

    def updateFitnessFunction(self, newFunction):
        self.fitnessFunction = newFunction

    def updateSimulationSpeed(self, newSpeed):
        self.simulationSpeed = newSpeed

    def createOrganism(self):
        pass

    def createGenes(self):
        pass

    def validateGenes(self):
        pass

    def validateCoordinates(self, xCoordinate, yCoordinate):
        return (xCoordinate, yCoordinate) in self.coordinates

    def decodeGenes(self):
        pass

    def updateDisplay(self):
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
        self.actionGenes = acionGenes
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
        return floor(sqrt((xCoordinate-self.locationCoordinates[0])**2+(yCoordinate-self.locationCoordinates[1])**2))

    def performLocationFunc(self):
        pass

    def performHealthFunc(self):
        pass

    def performFitnessFunction(self):
        if self.fitnessFunction == "health":
            pass


class SimulationData:
    def __init__(self):
        self.data = {}

    def setIterationData(self, index, data):
        self.data[index] = data

    def getIterationData(self, index):
        return self.data[index]


simulationData = SimulationData()
simulation = Simulation(100, 100, "health", simulationData)

