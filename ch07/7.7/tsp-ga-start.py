"""
Project 7.7

A baseline genetic algorithm for the TSP.

Discovering Computer Science, Second Edition
Jessen Havill
"""

import math, turtle, random

def distance(p, q):
	"""Return the distance between points p and q."""
	
	pass
	
def tourLength(tour):
	"""Return the total length of a tour."""
	
	pass
	
def readPoints(filename):
	"""Read points from a file and return a list of tuples."""
	
	inputFile = open(filename, 'r')
	points = []
	for line in inputFile:
		values = line.split()
		points.append((float(values[0]), float(values[1])))
	return points
	
def drawTour(tour):
	"""Draw a tour expressed as a list of (x,y) coordinates."""
	
	pass
	
# ********************* GENETIC ALGORITHM FOR TSP ***********************

GENERATIONS = 100000     # number of generations to evolve
SIZE = 50                # size of the population
CROSSOVER_RATE = 0.90    # probability that a crossover happens
MUTATION_RATE = 0.20     # probability that a mutation happens
MATING_FRACTION = 0.5    # top fraction of population that mates
	
def makePopulation(cities):
	"""Create a population consisting of random permutations of the cities."""
	
	population = []
	for i in range(SIZE):
		population.append(cities[:])       # add a copy of cities to population
		random.shuffle(population[i])      # shuffle the new list randomly
	return population
		
def crossover(mom, pop):
	"""Perform a single point crossover operation."""
	
	mid = random.randrange(0, len(mom) - 1)       # randomly choose crossover point
	
	# Make child1 a copy of mom but with cities in the second "half" of pop removed.
	child1 = [city for city in mom if city not in pop[mid:]]
			
	# Add the second half of pop to the end of child1.
	child1.extend(pop[mid:])
	
	# Make child2 a copy of pop but with cities in the second "half" of mom removed.
	child2 = [city for city in pop if city not in mom[mid:]]
	
	# Add the second half of mom to the end of child1.
	child2.extend(mom[mid:])
	
	return (child1, child2)
	
def swap(L, i, j):
	"""Swap two elements in a list (used by mutate)."""
	
	temp = L[i]
	L[i] = L[j]
	L[j] = temp

def mutate(individual):
	"""Mutate an individual by randomly swapping two cities."""
	
	if random.random() < MUTATION_RATE:
		i = random.randrange(0, len(individual))
		j = random.randrange(0, len(individual))
		swap(individual, i, j)
		
def newGeneration(population):
	"""Crossover two individuals, mutate them, and replace the two least fit individuals."""
	
	mate1 = random.choice(population[:int(SIZE * MATING_FRACTION)])     # randomly choose a tour to crossover
	if random.random() < CROSSOVER_RATE:                                # crossover with pobability CROSSOVER_RATE
		mate2 = random.choice(population[:int(SIZE * MATING_FRACTION)])  # randomly choose a second tour
		(child1, child2) = crossover(mate1, mate2)                       # cross the two tours
		mutate(child1)                                                   # mutate the children
		mutate(child2)                                                   
		population[SIZE - 2] = child1                                    # replace the two least fit
		population[SIZE - 1] = child2
	else:
		mutate(population[random.randrange(SIZE)])                       # otherwise just mutate a random tour
	
def histogram(population):
	"""Print a frequency chart of the current population diversity."""
	
	pass
	
def report(population, generation, minLength):
	"""Periodically display information about the current population."""
	
	if generation % 100 == 0:                      # display the generation number every 100
		print("GENERATION", generation)
			
	if generation % 1000 == 0:                     # display population diversity every 1000
		histogram(population)
		
	currentBest = tourLength(population[0])        # get the best tour length in this population
	if currentBest < minLength:                    # if it is the best so far, then print it
		print(currentBest)
		minLength = currentBest
		
	return minLength                               # return the best tour length so far
	
def tspGA(filename):
	"""Genetic algorithm for TSP."""
	
	# Get the city coordinates from a file.
	points = readPoints(filename)
	
	# Create an initial population of random tours.
	population = makePopulation(points) 
	
	# Sort the initial population by tour length using the TourLength function.
	population.sort(key = tourLength)
	
	# Initialize the shortest tour length.
	bestSoFar = tourLength(population[0])            
	
	# Evolve over GENERATIONS generations.
	for g in range(GENERATIONS):
	
		# Print stats on the current population and update the shorest tour length.
		bestSoFar = report(population, g, bestSoFar)  
		
		# Update the population via crossover and mutation.
		newGeneration(population)                     
		
		# Sort the population by tour length using the TourLength function.
		population.sort(key = tourLength)               
	
	tour = population[0]              # the best tour in the final generation
	
	drawTour(tour)                    # draw the tour
	
	return tourLength(tour)           # return the tour's length
	
def main():
	tspGA('africa.tsp')
	
main()
