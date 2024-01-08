from random import randint
from random import uniform
import sqlite3
from sqlite3 import Error
import numpy as np


class Simulation:
    """
    A class representing a simulation.

    Attributes:
    - globalID (int): A counter for organism id.
    - populationSize (int): The size of the population in the simulation.
    - mutationRate (float): The probability of mutation after creating children.
    - fitnessFunction (object): The fitness function object used in the genetic algorithm.
    - organisms (list): The list of alive organisms in the simulation.
    - simulationData (object): The object used to store simulation data.
    - coordinates (dict): The dictionary storing the coordinates of alive organisms.
    - gridSize (int): The size of the grid in the simulation.
    - dx (list): The list of x-directions for movement.
    - dy (list): The list of y-directions for movement.
    """

    def __init__(self, populationSize, mutationRate, fitnessFunction, dataObject):
        """
        Initializes a Simulation object.
        """
        self.globalID = 0
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.fitnessFunction = fitnessFunction
        self.organisms = []
        self.simulationData = dataObject
        self.coordinates = {}
        self.gridSize = 100
        self.dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        self.dy = [-1, 0, 1, 1, 1, 0, -1, -1]

    def start(self):
        """
        Creates the initial population for the simulation.

        Returns:
        - data (dict): The starting data for the simulation (population size, iteration count,
                       organism data and location)
        """
        for i in range(self.populationSize):
            self.createOrganism()

        return self.simulationData.getData()

    def getOrganismById(self, id):
        """
        Retrieves an organism from the organisms list using an ID.

        Parameters:
        - id (int): The ID of the organism.

        Returns:
        - organism (object): The organism object with the provided ID, or -1 if not found.
        """

        # linear search on the list of organisms
        for i in self.organisms:
            # check if the id of the organism matches the id provided
            if (i.id == id):
                return i
        return -1

    def geneticAlgorithm(self):
        """
        Performs the genetic algorithm for reproduction and selection of organisms.

        The genetic algorithm works as follows:
        - The fitness function is performed for each organism.
        - The organisms are sorted based on their fitness function score.
        - The top 50% of organisms are used to reproduce and create children with similar genes. 
        - Mutations are then applied to the children's genomes.
        - The children are then added to the simulation and the parents are removed.

        """
        selectionProcess = []

        # Fitness Function
        for i in self.organisms:
            selectionProcess.append(
                [self.fitnessFunction.performFitnessFunction(i), i.id])

        # Selection
        selectionProcess = sorted(selectionProcess)

        # Reproduction
        newOrganisms = []

        """
        check if the population size is 1 as it is a special case because 
        two parents are required to create a child
        """
        if (self.populationSize == 1):
            organism = self.getOrganismById(selectionProcess[0][1])
            self.createChild(organism, organism)

        elif (self.populationSize < 4):
            parent1 = self.getOrganismById(selectionProcess[0][1])
            parent2 = self.getOrganismById(selectionProcess[1][1])
            # two children are created from the first two parents
            self.createChild(parent1, parent2)
            self.createChild(parent1, parent2)
            if (self.populationSize == 3):
                # another child is created from the first two parents if the population size is 3
                self.createChild(parent1, parent2)

        else:
            # the top 50% of organisms selected and then every adjacent pair is used to create 4 children
            for ind in range(0, self.populationSize//2-1, 2):
                parent1 = self.getOrganismById(selectionProcess[ind][1])
                parent2 = self.getOrganismById(selectionProcess[ind+1][1])
                # 4 children are created because the 2 parents from the top half and bottom half are deleted
                self.createChild(parent1, parent2)
                self.createChild(parent1, parent2)
                self.createChild(parent1, parent2)
                self.createChild(parent1, parent2)

            parent1 = self.getOrganismById(selectionProcess[0][1])
            parent2 = self.getOrganismById(selectionProcess[1][1])

            """
            if the population size is odd, it means that there is one parent left over from the top half
            so the top two parents are used to create another child
            """
            if (self.populationSize % 2 != 0):
                self.createChild(parent1, parent2)

            """
            If the population size is even and not divisible by 4, this means that there
            are 2 parents left over. One from the top half and one from the bottom
            If the population size is odd and the even number below is not divisible by 4,
            then there is 1 parent left over from the top half and two from the bottom half.
            """
            if ((self.populationSize-self.populationSize % 2) % 4 != 0):
                self.createChild(parent1, parent2)
                self.createChild(parent1, parent2)

        # All the parents are deleted
        for i in range(len(selectionProcess)):
            self.deleteOrganism(selectionProcess[i][1])

    def deleteOrganism(self, id):
        """
        Deletes an organism from the simulation based on its ID.

        Parameters:
        - id (int): The ID of the organism to delete.

        Returns:
        - success (bool): True if the organism was successfully deleted, False otherwise.
        """
        # linear search on the list of organisms
        for i in range(len(self.organisms)):
            # check if the id of the organism matches the id provided
            if (self.organisms[i].id == id):
                # remove the organism from the list of organisms if it is found
                del self.organisms[i]
                return True
        return False

    def move(self):
        """
        Moves the organisms in the simulation.
        """
        # Iterates through every alive organism in the simulation
        for i in self.organisms:
            # Calculates the bias of the organism based on its current position.
            bias = self.calculateBias(i)

            # Get the weights of the organism (genes)
            organism_weights = i.genome.genes

            # Activation function
            def af(x): return np.tanh(x)

            maxWeight = 0
            direction = [0, 0]

            # The genes have a length of 8, so iterate through each gene
            for j in range(8):
                # Calculate the weight of the gene
                weight = af(bias[j] * organism_weights[j])

                if (abs(weight) > maxWeight):
                    maxWeight = weight
                    direction = [self.dx[j], self.dy[j]]

            # Remove the current coordinates of the organism from the dictionary
            self.coordinates.pop((i.xCoordinate, i.yCoordinate))

            # Update the coordinates of the organism using the direction values calculated above
            i.updateCoordinate(
                i.xCoordinate + direction[0], i.yCoordinate + direction[1])

            # Add the new coordinates of the organism to the dictionary
            self.coordinates[(i.xCoordinate, i.yCoordinate)] = True

            # Update the movement data for the organism in the simulation data object
            self.simulationData.updateMovement(
                i.id, i.xCoordinate, i.yCoordinate)

    def updateIteration(self):
        """
        Updates the simulation for a new iteration.
        """
        # This is pushed so that the programs knows it is a new iteration
        self.simulationData.updateMovement(-1, -1, -1)

        # The list of coordinates is cleared at the start of every iteration
        self.coordinates = {}

        for i in self.organisms:
            # New coordinates are generated for each organism
            newCoord = self.generateCoordinates()

            self.coordinates[newCoord] = True
            i.updateCoordinate(newCoord[0], newCoord[1])

            # The movement data is updated for each organism
            self.simulationData.updateMovement(i.id, newCoord[0], newCoord[1])

        # The organisms move for 100 iterations (this can change by changing the grid size)
        for i in range(2*self.gridSize):
            self.move()

        # The genetic algorithm is performed after all the organisms have moved
        self.geneticAlgorithm()

    def createOrganism(self):
        """
        Creates a new organism and adds it to the simulation.
        """
        # Generates a random available coordinate for the organism
        coordinates = self.generateCoordinates()
        xCoordinate = coordinates[0]
        yCoordinate = coordinates[1]
        # Creates a random set of genes for the organism
        genomeObject = Genome(self.createGenes(), self.mutationRate)
        # Adds the coordinates to the dictionary to prevent it from being used again
        self.coordinates[(xCoordinate, yCoordinate)] = True
        self.globalID += 1
        # Instantiates a new organism object and adds it to the list of organisms and simulation data object
        newOrganism = Organism(
            self.globalID-1, xCoordinate, yCoordinate, genomeObject)
        self.organisms.append(newOrganism)
        self.simulationData.addOrganism(newOrganism)

    def createChild(self, parent1, parent2):
        """
        Creates a child organism from two parent organisms and adds it to the simulation.

        Parameters:
        - parent1 (object): The first parent organism.
        - parent2 (object): The second parent organism.
        """
        # Generates a random available coordinate for the organism
        coordinates = self.generateCoordinates()
        xCoordinate = coordinates[0]
        yCoordinate = coordinates[1]
        # Adds the coordinates to the dictionary to prevent it from being used again
        self.coordinates[(xCoordinate, yCoordinate)] = True
        self.globalID += 1
        # Instantiates a new child object and adds it to the list of organisms and simulation data object
        newOrganism = ChildOrganism(
            self.globalID-1, xCoordinate, yCoordinate, parent1, parent2, self.mutationRate)
        self.organisms.append(newOrganism)
        self.simulationData.addOrganism(newOrganism)

    def createGenes(self):
        """
        Creates a set of genes for an organism.

        Returns:
        - genes (list): The list of genes.
        """
        # Genes have a length of 8 that represents each direction (N, NE, E, SE, S, SW, W, NW)
        weights = []
        for i in range(8):
            # Each weight is a float between 0 and 1
            weights.append(uniform(0, 1))
        return weights

    def calculateBias(self, organism):
        """
        Calculates the bias of an organism in each direction

        Parameters:
        - organism (object): The organism object whose bias is calculated.

        Returns:
        - bias (list): The bias for each direction.
        """
        bias = [0, 0, 0, 0, 0, 0, 0, 0]

        # The organism's current coordinates
        x_coordinate = organism.xCoordinate
        y_coordinate = organism.yCoordinate

        # Iterate through each direction (N, NE, E, SE, S, SW, W, NW)
        # The directions are stored in the dx and dy lists
        for i in range(8):
            distance = 0
            for j in range(1, 100):
                # Calculate the new coordinates for the organism
                newX = x_coordinate + self.dx[i]*j
                newY = y_coordinate + self.dy[i]*j
                # Check if the new coordinates are out of bounds
                if (newX < 0 or newX >= self.gridSize or newY < 0 or newY >= self.gridSize):
                    break
                # Check if the new coordinates are occupied by another organism
                if ((newX,  newY) in self.coordinates):
                    break

                # There is no organism in the new coordinates, so the distance is incremented
                distance += 1

            bias[i] = distance

        return bias

    def generateCoordinates(self):
        """
        Generates random coordinates for an organism.

        Returns:
        - coordinates (tuple): The generated coordinates.
        """
        # Use randint function to generate two random numbers
        newCoord = (randint(0, self.gridSize-1),
                    randint(0, self.gridSize-1))

        # Repeat until the coordinates are not occupied by another organism
        while newCoord in self.coordinates:
            newCoord = (randint(0, self.gridSize-1),
                        randint(0, self.gridSize-1))

        return newCoord


class Organism:
    """
    Represents the first generation organisms in the simulation.

    Attributes:
        id (int): The ID of the organism.
        xCoordinate (int): The x-coordinate of the organism's location.
        yCoordinate (int): The y-coordinate of the organism's location.
        genome (object): The genome object of the organism.
    """

    def __init__(self, ID, xCoordinate, yCoordinate, genomeObject):
        """
        Initializes a new instance of the Organism class.

        Args:
            ID (int): The ID of the organism.
            xCoordinate (int): The x-coordinate of the organism's location.
            yCoordinate (int): The y-coordinate of the organism's location.
            genomeObject (object): The genome object of the organism.
        """
        self.id = ID
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.genome = genomeObject

    def updateCoordinate(self, xCoordinate, yCoordinate):
        """
        Updates the coordinates of the organism.

        Args:
            xCoordinate (int): The new x-coordinate of the organism's location.
            yCoordinate (int): The new y-coordinate of the organism's location.
        """
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate

    def getParents(self):
        """
        Gets the parents of the organism.
        Since the organisms are the first generation, they do not have parents so it returns [-1, -1]
        """
        return [-1, -1]


class ChildOrganism(Organism):
    """
    Represents a child organism inheriting genes from two parent organisms.
    This class inherits the attributes and methods from the Organism class.

    Attributes:
        ID (int): The unique identifier of the child organism.
        xCoordinate (float): The x-coordinate of the child organism's position.
        yCoordinate (float): The y-coordinate of the child organism's position.
        parent1 (Organism): The first parent organism.
        parent2 (Organism): The second parent organism.
        mutationRate (float): The rate at which the child organism's genes mutate.
    """

    def __init__(self, ID, xCoordinate, yCoordinate, parent1, parent2, mutationRate):
        """
        Initializes a ChildOrganism object and inherits the attributes and methods from the Organism class.
        """
        self.parents = [parent1, parent2]
        parent1_genome = parent1.genome.genes
        parent2_genome = parent2.genome.genes
        # Combine the genes of the two parent organisms to create a new genome
        newProbability = ChildOrganism.combineGenes(
            parent1_genome, parent2_genome)
        newGenome = Genome(newProbability, mutationRate)
        # Mutate the genes of the new genome based on the mutation rate
        newGenome.mutateGenes()
        # Call the constructor of the Organism class
        super().__init__(ID, xCoordinate, yCoordinate, newGenome)

    def combineGenes(parent1_genome, parent2_genome):
        """
        Combines the genes of two parent organisms to create a new probability.

        Args:
            parent1_genome (list): The gene probabilities of the first parent organism.
            parent2_genome (list): The gene probabilities of the second parent organism.

        Returns:
            list: The combined gene probabilities of the two parent organisms.
        """
        newProbability = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            # The gene at every even index is taken from the first parent and
            # the gene at every odd index is taken from the second parent
            if (i % 2 == 0):
                newProbability[i] = parent1_genome[i]
            else:
                newProbability[i] = parent2_genome[i]

        return newProbability

    # Overrides the getParents method from the Organism class
    def getParents(self):
        """
        Gets the IDs of the parent organisms.

        Returns:
            list: The IDs of the parent organisms.
        """
        return [self.parents[0].id, self.parents[1].id]


class Genome:
    """
    Represents the genome of an organism.

    Attributes:
        genes (list): A list of genes.
        mutationRate (float): The mutation rate.
    """

    def __init__(self, genes, mutationRate):
        """
        Initializes a Genome object.

        Args:
            genes (list): A list of genes.
            mutationRate (float): The mutation rate.

        Attributes:
            genes (list): A list of genes.
            mutationRate (float): The mutation rate.
        """
        self.genes = genes
        self.mutationRate = mutationRate

    def mutateGenes(self):
        """
        Mutates the genes of the Genome object.
        """
        # Iterate through each gene
        for i in range(8):
            # Check if the gene should be mutated based on the mutation rate
            if (randint(1, 100) <= self.mutationRate):
                # Mutate the gene by replacing it with a random float between 0 and 1
                self.genes[i] = uniform(0, 1)


class FitnessFunction:
    """
    A class that represents a fitness function.

    Attributes:
        __locationCoordinates (list): The location coordinates.
    """

    def __init__(self):
        self.__locationCoordinates = []

    def setLocation(self, xCoordinate, yCoordinate):
        """
        Set the location coordinates.

        Args:
            xCoordinate (float): The x-coordinate of the location.
            yCoordinate (float): The y-coordinate of the location.
        """
        self.__locationCoordinates = [xCoordinate, yCoordinate]

    def performFitnessFunction(self, organism):
        """
        Perform the fitness function calculation for the given organism.

        Args:
            organism (Organism): The organism for which to calculate the fitness function.

        Returns:
            float: The fitness function value for the organism.
        """
        # Calculate the distance^2 using the distance formula (x2-x1)^2 + (y2-y1)^2.
        distance = (organism.xCoordinate - self.__locationCoordinates[0]) ** 2 + (
            organism.yCoordinate - self.__locationCoordinates[1]) ** 2
        return distance


class SimulationData:
    """
    A class that represents simulation data.

    Attributes:
        __data (dict): A dictionary that stores the simulation data.
    """

    def __init__(self, iterationCount, populationSize, location):
        """
        Initializes the SimulationData object.

        Args:
            iterationCount (int): The number of iterations in the simulation.
            populationSize (int): The size of the population in the simulation.
            location (tuple): The location of the simulation.

        Returns:
            None
        """
        self.__data = {}
        self.__data["iterationCount"] = iterationCount
        self.__data["populationSize"] = populationSize
        # A list of (id, (xCoordinate, yCoordinate))
        self.__data["movement"] = []
        # A list of (id, genes, parents)
        self.__data["organisms"] = []
        self.__data["location"] = [location[0], location[1]]

    def getData(self):
        """
        Returns the simulation data.

        Args:
            None

        Returns:
            dict: The simulation data.
        """
        return self.__data

    def uploadData(self, data):
        """
        Uploads new data to the simulation.

        Args:
            data (dict): The new data to be uploaded.

        Returns:
            bool: True if the data is successfully uploaded, False otherwise.
        """
        self.__data = data
        # Check if the data is in a valid format
        try:
            hasOrganism = {}
            # Check if the data has the required keys
            iterationCount = data["iterationCount"]
            populationSize = data["populationSize"]
            simulationType = data["simulationType"]
            uniqueId = data["id"]

            # Checks if all the organisms in the valid format (id, genes, parents)
            for i in range(len(data["organisms"])):
                currentOrganism = data["organisms"][i]
                # Checks if it has id, genes and parents
                if (len(currentOrganism) != 3):
                    return False
                hasOrganism[currentOrganism[0]] = True
                # Checks that the genes are of length 8
                if (len(currentOrganism[1]) != 8):
                    return False
                # Checks that the parents are of length 2
                if (len(currentOrganism[2]) != 2):
                    return False

            for i in range(iterationCount):
                # Checks if all the organisms in each iteration is in the data dictionary
                for organism in data["organismsInIteration"][i]:
                    if (not hasOrganism[organism]):
                        return False

        except KeyError:
            return False

        return True

    def addOrganism(self, organism):
        """
        Adds a new organism to the simulation.

        Args:
            organism (Organism): The organism to be added.
        """
        self.__data["organisms"].append(
            [organism.id, organism.genome.genes, organism.getParents()])

    def updateMovement(self, id, xCoordinate, yCoordinate):
        """
        Updates the movement of an organism.

        Args:
            id (int): The ID of the organism.
            xCoordinate (float): The new x-coordinate of the organism.
            yCoordinate (float): The new y-coordinate of the organism.
        """
        self.__data["movement"].append((id, (xCoordinate, yCoordinate)))

    def clearMovement(self):
        """
        Clears the movement data.
        """
        self.__data["movement"] = []

    def clearOrganisms(self):
        """
        Clears the organisms data.
        """
        self.__data["organisms"] = []


class Database:
    """
    A class that handles the database operations for the simulation.
    """

    def __init__(self):
        """
        Initializes the Database object and creates the simulation table if it doesn't exist.
        """
        try:
            connection = sqlite3.connect("simulation.db")
            connection.execute('''CREATE TABLE IF NOT EXISTS simulation(
                   name text PRIMARY KEY,
                   password text,
                   public bool,
                   iterations integer,
                   population integer,
                   location_x integer,
                   location_y integer)''')
            connection.commit()
            connection.close()
        except Error as e:
            print(f"The error '{e}' occurred")

    def checkForSimulation(self, name):
        """
        Checks if a simulation with the given name exists in the database.

        Parameters:
        - name: The name of the simulation to check.

        Returns:
        - True if the simulation exists, False otherwise.
        """
        connection = sqlite3.connect("simulation.db")
        row = connection.execute(f"""
                            SELECT * FROM simulation
                            WHERE name='{name}'""")

        # Checks if the row is empty
        for value in row:
            # Row is not empty, so the simulation exists
            connection.close()
            return True
        connection.close()
        return False

    def isPublic(self, name):
        """
        Checks if a simulation with the given name is public.

        Parameters:
        - name: The name of the simulation to check.

        Returns:
        - True if the simulation is public, False otherwise.
        """
        # Checks if the simulation exists
        if (Database.checkForSimulation(self, name) == False):
            return False
        connection = sqlite3.connect("simulation.db")
        row = connection.execute(f"""
                                SELECT public FROM simulation
                                WHERE name='{name}'                              """)

        for value in row:
            data = value[0]
        connection.close()
        return data == 0

    def verifyPassword(self, name, password):
        """
        Verifies the password for a simulation with the given name.

        Parameters:
        - name: The name of the simulation.
        - password: The password to verify.

        Returns:
        - True if the password is correct, False otherwise.
        """
        # Checks if the simulation exists
        if (Database.checkForSimulation(self, name) == False):
            return False
        connection = sqlite3.connect("simulation.db")
        row = connection.execute(
            f"SELECT password FROM simulation WHERE name='{name}'")
        for value in row:
            simulationPassword = value[0]

        # Hashes the password and compares it with the hashed password in the database
        return simulationPassword == str(Database.hashPassword(self, password))

    def hashPassword(self, password):
        """
        Hashes the given password using a custom hashing algorithm.

        Parameters:
        - password: The password to hash.

        Returns:
        - The hashed password.
        """
        modulo = 10**9 + 9  # prime number
        power = 127  # prime number that is roughly equal to no of characters
        hash_value = 0
        for i in password:
            # Get the current ASCII value of the character and multiply it by the power
            # and add the remainder of the modulo to the hash value
            hash_value = (hash_value + ord(i)*power) % modulo
            # Multiply the power by 127 and take the remainder of the modulo
            power = (power*127) % modulo
        return hash_value

    def insertSimulation(self, name, password, public, data):
        """
        Inserts a new simulation into the database.

        Parameters:
        - name: The name of the simulation.
        - password: The password for the simulation.
        - public: Whether the simulation is public or not (default is 1).
        - data: The data for the simulation (optional).
        """
        connection = sqlite3.connect("simulation.db")
        # Hashes the password
        hashedPassword = Database.hashPassword(self, password)
        iterationCount = data['iterationCount']
        size = data['populationSize']
        location_x = data['location'][0]
        location_y = data['location'][1]

        connection.execute(
            f"INSERT INTO simulation VALUES ('{name}', '{hashedPassword}', {public}, {iterationCount}, {size}, {location_x}, {location_y})")

        # Creates a table for the genome
        connection.execute(f"""CREATE TABLE IF NOT EXISTS genome_{name}(
                            id integer PRIMARY KEY,
                            genome text,
                            parent1 integer,
                            parent2 integer)
                           """)
        for organism in data["organisms"]:
            values = str(organism[0])+",'"
            for i in range(8):
                values += str(organism[1][i])+","
            values += "'," + str(organism[2][0])+","+str(organism[2][1])
            try:
                connection.execute(
                    f"INSERT INTO genome_{name} VALUES({values})")
            except:
                continue

        # Creates a table for the iteration data
        connection.execute(f"""CREATE TABLE IF NOT EXISTS iteration_{name}(
                            id integer PRIMARY KEY,
                            data text)
                           """)

        index = 0
        done = False
        # Iterates through each iteration
        for i in range(data["iterationCount"]):
            # Checks if the iteration is empty
            if (data["iterations"][i] == []):
                continue
            # Converts each iteration into a string in the format: id, xCoordinate, yCoordinate;id, xCordinate, yCoordinate;...
            # So each move is separated by a semicolon and each value is separated by a comma
            iterationData = ""
            for iteration in data["iterations"][i]:
                iterationData += f"{iteration[0]},{iteration[1][0]},{iteration[1][1]};"

            connection.execute(
                f"INSERT INTO iteration_{name} VALUES({i}, '{iterationData}')")
            iterationData = ""
        connection.commit()
        connection.close()

    def removeSimulation(self, name):
        """
        Removes a simulation from the database.

        Parameters:
        - name: The name of the simulation to remove.
        """
        connection = sqlite3.connect("simulation.db")
        connection.execute(f"DELETE FROM simulation WHERE name='{name}'")
        connection.execute(f"DROP TABLE genome_{name}")
        connection.execute(f"DROP TABLE iteration_{name}")
        connection.commit()
        connection.close()

    def getSimulation(self, name):
        """
        Retrieves the data for a simulation from the database.

        Parameters:
        - name: The name of the simulation to retrieve.

        Returns:
        - A dictionary containing the simulation data.
        """
        connection = sqlite3.connect("simulation.db")
        if (Database.checkForSimulation(self, name) == False):
            return {}

        data = {}
        row = connection.execute(
            f"SELECT * FROM simulation WHERE name='{name}'")
        # value is in the format (name, password, public, iterationCount, populationSize)
        for value in row:
            data["iterationCount"] = value[3]
            data["populationSize"] = value[4]
            data["location"] = [value[5], value[6]]
        rows = connection.execute(f"SELECT * FROM genome_{name}")
        data["organisms"] = []
        # value is in the format (id, genome, parent1, parent2)
        for value in rows:
            genes = value[1].split(',')
            genome = []
            for i in range(8):
                genome.append(float(genes[i]))
            parents = [value[2], value[3]]
            # appends the organism in the format (id, genes, parents)
            data["organisms"].append([value[0], genome, parents])
        rows = connection.execute(f"SELECT * FROM iteration_{name}")
        data["iterations"] = []
        # value is in the format (id, data)
        for value in rows:
            # data is in the format id, xCoordinate, yCoordinate;id, xCordinate, yCoordinate;...
            # so splitting it would give a list in the format ["id, xCoordinate, yCoordinate", ...]
            movements = value[1].split(';')
            # iterationData needs to be in the format [[id, [xCoordinate, yCoordinate]], ...]
            iterationData = []
            # move is in the format "id, xCoordinate, yCoordinate"
            for move in movements:
                if (move == ""):
                    continue
                # splits the move into a list in the format ["id", "xCoordinate", "yCoordinate"]
                splitted = move.split(',')
                iterationData.append(
                    [int(splitted[0]), [int(splitted[1]), int(splitted[2])]])
            data["iterations"].append(iterationData)
        return data
