class Simulation:
    def __init__(self, populationSize, numberOfIterations, fitnessFunction):
        self.globalID = 0
        self.populationSize = populationSize
        self.numberOfIterations = numberOfIterations
        self.fitnessFunction = fitnessFunction
        self.organisms = []
        self.currentIterationNumber
        self.currentIterationData = ""
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
    pass


class Genome:
    pass


class FitnessFunction:
    pass


class SimulationData:
    pass
