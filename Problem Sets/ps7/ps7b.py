# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name: Matt Graffunder
# Collaborators: None 
# Time Spent: 2:00

import numpy
import random
import pylab

def Roll(numDice):
	result = []
	
	for i in xrange(numDice):
		result.append(random.randrange(1,7))

	return result
	
def Trial(numDice, numRolls):
	yatzees = 0
	
	for x in xrange(numRolls):
		roll = Roll(numDice)
		
		#print "Roll", roll, 
		
		#Check that dice match
		match = True
		for die in roll:
			if die != roll[0]:
				match = False
				break
		if match:
			yatzees += 1
			#print "Yatzee"
		#else: 
			#print ""
		
			
		
			
	odds = float(yatzees) / numRolls
	return odds
	
def RunTrials():
	numDice = 5
	numTrials = 10
	numRollsPerTrial = 1000000
	
	results = []
	
	for trial in xrange(numTrials):
		results.append(Trial(numDice, numRollsPerTrial))
		
	mean = CalculateMean(results)
	stdDeviation = CalculateStandardDeviation(results)

	print "Mean Avg.: ", mean
	print "Standard Deviation: ", stdDeviation

def CalculateMean(listOfNumbers):
	total = 0
	
	for num in listOfNumbers:
		total += num
	
	return float(total) / len(listOfNumbers)
	
def CalculateStandardDeviation(listOfNumbers):
	mean = CalculateMean(listOfNumbers)
	
	intermediate = 0
	
	for num in listOfNumbers:
		intermediate += (num - mean) ** 2
	
	stdDeviation = (intermediate / len(listOfNumbers)) ** .5
	
	return stdDeviation
