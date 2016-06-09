# 6.00 Problem Set 8
# Name: Matt Graffunder
# Collaborators: None 
# Time Spent: 0:30

import numpy
import random
import pylab

#Need to copy ps7 to ps8 directory, or update the path variable
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """

        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb
        
    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        
        if drug in self.resistances:
            return self.resistances[drug]
        else:
            return False

    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """

        #Check to see if it can reproduce        
        willReproduce = self.IsResistantToAllDrugs(activeDrugs) and self.WillReproduce(popDensity)
        #print "Will Reproduce: ", willReproduce
        
        #Virus has resistance to one or more drugs, therefore it can reproduce
        if willReproduce:
            childResistances = self.GetChildResistances()
            
            return ResistantVirus(self.maxBirthProb, self.clearProb, childResistances, self.mutProb)
        else:
            raise NoChildException()
          
    def IsResistantToAtLeastOneDrug(self, activeDrugs):      
        """
        I added this because the instructions said ANY drug, 
        but I'm pretty sure they meant ALL drugs
        """
        if len(activeDrugs) == 0:
            return True # No Drugs to check resistance to
              
        for drug in activeDrugs:
            if self.isResistantTo(drug):
                return True #Resistant to One, Break
        
        return False
    
    def IsResistantToAllDrugs(self, activeDrugs):
        #Forces virus to be resistant to both
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                return False # Not Resistant to one or more
                
        return True #Resistant to All
                 
    def KeepResistance(self, mutProb):
        return random.random() < (1 - mutProb)

    def GainResistance(self, mutProb):
        return random.random() < mutProb
       
    def GetChildResistances(self):
        childResistances = {}
        
        #Determine Drug Resistances
        for drug in self.resistances:
            if self.isResistantTo(drug):
                childResistances[drug] = self.KeepResistance(self.mutProb)
            else:
                childResistances[drug] = self.GainResistance(self.mutProb)
                    
        return childResistances

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        SimplePatient.__init__(self, viruses, maxPop)
        self.prescriptions = []

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
       
        if newDrug not in self.prescriptions:
            self.prescriptions.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """
        
        return self.prescriptions
        

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
    
        #Loop through drugs, and save any viruses that are resistant
        #Return the length of the remaining viruses

        remainingViruses = self.viruses
        
        for drug in drugResist:
            resistantViruses = []
            
            for virus in remainingViruses:
                if virus.isResistantTo(drug):
                   resistantViruses.append(virus)
            
            remainingViruses = resistantViruses
            
        return len(remainingViruses)

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        # TODO

        #Get the viruses that survived
        self.viruses = self.GetSurvivingViruses()
        
        populationDensity = self.GetPopulationDensity()
        
        self.viruses = self.GetUpdatedListOfViruses(populationDensity)
        
        return self.getTotalPop()
    
    def GetUpdatedListOfViruses(self, density):
        updatedViruses = []
        
        for virus in self.viruses:
            #Add Virus back to updated
            updatedViruses.append(virus)
            
            #Check if virus reproduced
            try:
                #print "Try: ",
                #print "Density: ", density,
                #print "Prescriptions: ", self.getPrescriptions(),
                updatedViruses.append(virus.reproduce(density, self.getPrescriptions()))
                #~ print " Sucess"
            except:
                #~ print " Failed"
                pass
                
        return updatedViruses

#
# PROBLEM 2
#

def GetStartingViruses(startingNumberOfViruses, maxBirthProb, clearProb, mutProb, drugsToAdminister):
    viruses = []
    
    #Build Resistance Dictionary
    resistances = {}
    
    for drug in drugsToAdminister:
        resistances[drug] = False
            
    for i in xrange(startingNumberOfViruses):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
            
    return viruses

def BuildFinalResults(listOfDataLists, simulationSteps):
    """
    Takes a list of simulation result sets, and returns a list of values of the mean at each step
    """
    finalResults = []
    for step in xrange(simulationSteps):
        currentValue = 0
        for sim in listOfDataLists:
            currentValue += sim[step]
            
        finalResults.append(currentValue/len(listOfDataLists))
    
    return finalResults

def RunSimulation(patient, numberOfStepsToSimulate, drugsToAdminister, stepToAdministerDrugs ):
    """
    Runs Simulation on the patient, and returns the results from each step.
    """
    
    simResultsTotalVirus = []
    simResultsResistantViruses = []
    
    simResultsIndividualResistantViruses = {}
    for drug in drugsToAdminister:
        simResultsIndividualResistantViruses[drug] = []
    
    #Run Simulation
    for i in xrange(numberOfStepsToSimulate):
        #Check if we should add a drug
        if i in stepToAdministerDrugs:
            for drug in stepToAdministerDrugs[i]:
                patient.addPrescription(drug)
        
        totalPop = patient.update()            
        resistantPop = patient.getResistPop(drugsToAdminister)
        
        simResultsTotalVirus.append(totalPop)
        simResultsResistantViruses.append(resistantPop)
        
        for drug in drugsToAdminister:
            simResultsIndividualResistantViruses[drug].append(patient.getResistPop([drug]))
        
    return (simResultsTotalVirus, simResultsResistantViruses, simResultsIndividualResistantViruses)

def simulationWithDrug():
    """
    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """

    #Simulation Parameters
    startingNumberOfViruses = 100
    maxNumberOfViruses = 1000

    maxBirthProb = 0.1
    clearProb = 0.05
    mutProb = .005

    numberOfTimesToRunSimulation = 25
    numberOfStepsToSimulate = 300
    
    #Dictionary of Drugs to Administer
    #Key is step number to administer Drug
    #Value is list of drugs to administer
    drugsToAdminister = ["guttagonal"]
    stepToAdministerDrugs = {150 : ["guttagonal"]}
    	
    #Run Simulations
    allSimulationResultsTotalViruses = []
    allSimulationResultsResistantViruses = []        
    
    for sim in xrange(numberOfTimesToRunSimulation):            
        #Setup Simulation        
        startViruses = GetStartingViruses(startingNumberOfViruses, maxBirthProb, clearProb, mutProb, drugsToAdminister)
        patient = Patient(startViruses,maxNumberOfViruses)
        
        simResults = RunSimulation(patient, numberOfStepsToSimulate, drugsToAdminister, stepToAdministerDrugs)
         
        allSimulationResultsTotalViruses.append(simResults[0])
        allSimulationResultsResistantViruses.append(simResults[1])
    
    #Build Final Results sets
    finalResultsTotalViruses = BuildFinalResults(allSimulationResultsTotalViruses, numberOfStepsToSimulate)
    finalResultsResistantViruses = BuildFinalResults(allSimulationResultsResistantViruses, numberOfStepsToSimulate)
     
    pylab.plot(finalResultsTotalViruses)
    pylab.plot(finalResultsResistantViruses)
    pylab.title('Mean Number of Viruses in patient at each step for ' + str(numberOfTimesToRunSimulation) + ' trials')
    pylab.xlabel('Step Number')
    pylab.ylabel('Number of Viruses')
    pylab.ylim(0, maxNumberOfViruses)
    pylab.show()

#simulationWithDrug()

#
# PROBLEM 3
#        

def PrintProgressBar(totalSteps, currentStep):
    size = 20
    print "[" + "-" * 20 + "]"

def simulationDelayedTreatment():

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """

    #Simulation Parameters
    startingNumberOfViruses = 100
    maxNumberOfViruses = 1000

    maxBirthProb = 0.1
    clearProb = 0.05
    mutProb = .005

    drugsToAdminister = ["guttagonal"]

    numberOfTimesToRunSimulation = 1000
    numberOfStepsToSimulateAfterDelay = 150
    
    #Dictionary of Drugs to Administer
    #Key is step number to administer Drug
    #Value is list of drugs to administer    
    #~ stepToAdministerDrugs = {150 : ["guttagonal"]}
    
    simulationsToRun = [(300, {300 : ["guttagonal"]}), (150, {150 : ["guttagonal"]}),(75, {75 : ["guttagonal"]}),(0, {0 : ["guttagonal"]})]
    
    delayResults = {}
    
    print "Total Patients to Simulate: " + str(numberOfTimesToRunSimulation)
    print ""
    
    #Run Simulations
    for simulation in simulationsToRun:   
        patientResults = []
        
        delay = simulation[0]
        totalStepsToRun = delay + numberOfStepsToSimulateAfterDelay
             	
        print "Running Simulations for Delay: " + str(delay)
        
        for sim in xrange(numberOfTimesToRunSimulation):     
            
            if sim % (numberOfTimesToRunSimulation /10) == 0:
                print str(sim / (numberOfTimesToRunSimulation /10)*10 + 10) + "%"
                   
            #Setup Simulation        
            startViruses = GetStartingViruses(startingNumberOfViruses, maxBirthProb, clearProb, mutProb, drugsToAdminister)
            patient = Patient(startViruses,maxNumberOfViruses)
                        
            RunSimulation(patient, totalStepsToRun, drugsToAdminister, simulation[1])
             
            patientResults.append(patient.getTotalPop())
        
        delayResults[delay] = patientResults
        
    #DisplayResults
    for delay in delayResults:
        pylab.hist(delayResults[delay], 20, (0,1000))
        pylab.title('Number of viruses remaining in patient after a ' + str(delay) + ' delay')
        pylab.xlabel('Remaining Viruses')
        pylab.ylabel('Number of Patients')
        pylab.show()

#
# PROBLEM 4
#

#simulationDelayedTreatment()

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    #Simulation Parameters
    startingNumberOfViruses = 100
    maxNumberOfViruses = 1000

    maxBirthProb = 0.1
    clearProb = 0.05
    mutProb = .005

    drugsToAdminister = ["guttagonal", "grimpex"]

    numberOfTimesToRunSimulation = 1000
    numberOfStepsToSimulateBeforeFirstDrug = 150
    numberOfStepsToSimulateAfterDelay = 150
    
    
    #Dictionary of Drugs to Administer
    #Key is step number to administer Drug
    #Value is list of drugs to administer    
    #~ stepToAdministerDrugs = {150 : ["guttagonal"]}
    
    simulationsToRun = [
    (300, {numberOfStepsToSimulateBeforeFirstDrug : ["guttagonal"], 450: ['grimpex']}), 
    (150, {numberOfStepsToSimulateBeforeFirstDrug : ["guttagonal"], 300: ['grimpex']}),
    (75, {numberOfStepsToSimulateBeforeFirstDrug : ["guttagonal"], 225: ['grimpex']}),
    (0, {numberOfStepsToSimulateBeforeFirstDrug : ["guttagonal", 'grimpex']})]
    
    delayResults = {}
    
    print "Total Patients to Simulate: " + str(numberOfTimesToRunSimulation)
    print ""
    
    #Run Simulations
    for simulation in simulationsToRun:   
        patientResults = []
        
        delay = simulation[0]
        totalStepsToRun = numberOfStepsToSimulateBeforeFirstDrug + delay + numberOfStepsToSimulateAfterDelay
             	
        print "Running Simulations for Delay: " + str(delay)
        
        for sim in xrange(numberOfTimesToRunSimulation):     
            
            if sim % (numberOfTimesToRunSimulation /10) == 0:
                print str(sim / (numberOfTimesToRunSimulation /10)*10 + 10) + "%"
                   
            #Setup Simulation        
            startViruses = GetStartingViruses(startingNumberOfViruses, maxBirthProb, clearProb, mutProb, drugsToAdminister)
            patient = Patient(startViruses,maxNumberOfViruses)
                        
            RunSimulation(patient, totalStepsToRun, drugsToAdminister, simulation[1])
             
            patientResults.append(patient.getTotalPop())
        
        delayResults[delay] = patientResults
        
    #DisplayResults
    for delay in delayResults:
        pylab.hist(delayResults[delay], 20, (0,1000))
        pylab.title('Number of viruses remaining in patient after a ' + str(delay) + ' delay')
        pylab.xlabel('Remaining Viruses')
        pylab.ylabel('Number of Patients')
        pylab.show()

#simulationTwoDrugsDelayedTreatment()

#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    #Simulation Parameters
    startingNumberOfViruses = 100
    maxNumberOfViruses = 1000

    maxBirthProb = 0.1
    clearProb = 0.05
    mutProb = .005

    numberOfTimesToRunSimulation = 25
        
    #Dictionary of Drugs to Administer
    #Key is step number to administer Drug
    #Value is list of drugs to administer
    drugsToAdminister = ["guttagonal", "grimpex"]
    
    #Trial 1 with No Delay
    numberOfStepsToSimulate = 300
    stepToAdministerDrugs = {150 : ["guttagonal", "grimpex"]}
    
    #Trial 2 with 150 Step Delay
    #numberOfStepsToSimulate = 450
    #stepToAdministerDrugs = {150 : ["guttagonal"], 300 : ["grimpex"]}
    	
    #Run Simulations
    allSimulationResultsTotalViruses = []
    allSimulationResultsResistantViruses = []    
    allSimResultsIndividualResistantViruses = {}
    
    
    for drug in drugsToAdminister:
        allSimResultsIndividualResistantViruses[drug] = []
    
    for sim in xrange(numberOfTimesToRunSimulation):            
        #Setup Simulation        
        startViruses = GetStartingViruses(startingNumberOfViruses, maxBirthProb, clearProb, mutProb, drugsToAdminister)
        patient = Patient(startViruses,maxNumberOfViruses)
        
        simResults = RunSimulation(patient, numberOfStepsToSimulate, drugsToAdminister, stepToAdministerDrugs)
         
        allSimulationResultsTotalViruses.append(simResults[0])
        allSimulationResultsResistantViruses.append(simResults[1])
        
        for drug in drugsToAdminister:
            allSimResultsIndividualResistantViruses[drug].append(simResults[2][drug])
    
    #Build Final Results sets
    finalResultsTotalViruses = BuildFinalResults(allSimulationResultsTotalViruses, numberOfStepsToSimulate)
    finalResultsResistantViruses = BuildFinalResults(allSimulationResultsResistantViruses, numberOfStepsToSimulate)
    finalResultsIndividualResistantViruses = {}
    
    for drug in drugsToAdminister:
        finalResultsIndividualResistantViruses[drug] = BuildFinalResults(allSimResultsIndividualResistantViruses[drug], numberOfStepsToSimulate)
        
    pylab.plot(finalResultsTotalViruses)
    pylab.plot(finalResultsResistantViruses)
    
    for drug in drugsToAdminister:
        pylab.plot(finalResultsIndividualResistantViruses[drug])
    
    pylab.title('Mean Number of Viruses in patient at each step for ' + str(numberOfTimesToRunSimulation) + ' trials')
    pylab.xlabel('Step Number')
    pylab.ylabel('Number of Viruses')
    pylab.ylim(0, maxNumberOfViruses)
    pylab.show()

#simulationTwoDrugsVirusPopulations()

