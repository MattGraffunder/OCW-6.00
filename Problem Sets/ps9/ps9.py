# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name: Matt Graffunder
# Collaborators: None 
# Time Spent: 2:00
#

import itertools

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    subjectDict = {}

    # The following sample code reads lines from the specified file and prints
    # each one.
    inputFile = open(filename)
    for line in inputFile:
        subjectParts = line.split(',')
        #print subjectParts
        #Add to Dictionary
        subjectDict[subjectParts[0]] = (int(subjectParts[1]), int(subjectParts[2]))

    return subjectDict

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    
    return subInfo1[0] > subInfo2[0]

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    return subInfo1[1] < subInfo2[1]

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    return (float(subInfo1[0])/subInfo1[1]) > (float(subInfo2[0])/subInfo2[1])

#This homeworks isn't easy to do the way it was designed.
#The Comparator function is deprecated, and almost scrubed from the internet it seems
#Plus Prof. Guttag uses key functions instead, so I will too.

def keyValue(course):
    return course.getValue()

def keyWork(course):
    #print subjectTuple[1]
    #return 1.0/subjectTuple[1]
    return 1.0 / course.getWork()

def keyRatio(course):
    #return float(subjectTuple[0])/subjectTuple[1]
    return float(course.getValue())/course.getWork()

def greedyAdvisor(subjects, maxWork, keyFn):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    results = {}
    totalWork = 0

    #This dictionary is stupid, and hard to sort.  Let's make a class and use that
    courses = BuildCourseList(subjects)         
    
    #Get list of subjects sorted by key function
    courses = sorted(courses, key=keyFn, reverse = True)
    
    #select from list using dictionary
    for course in courses:
        name = course.getCourseName()
        
        #check if subject exceeds max work        
        if totalWork + course.getWork() <= maxWork:
            results[name] = subjects[name]
            totalWork += course.getWork()

    return results

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    
    results = {}
    bestResult = []
    bestResultValue = 0    

    #This dictionary is stupid, and hard to sort.  Let's make a class and use that
    courses = BuildCourseList(subjects)         

    #Iterate over the powerset
    for courseListSize in xrange(len(courses)+1):
        for courseList in itertools.combinations(courses, courseListSize):
            courseListValue = sum(course.getValue() for course in courseList)
            courseListWork = sum(course.getWork() for course in courseList)

            if courseListWork <= maxWork and courseListValue > bestResultValue:
                bestResultValue = courseListValue
                bestResult = courseList

    for course in bestResult:
        results[course.getCourseName()] = (course.getValue(), course.getWork())

    return results

class Course(object):
    def __init__(self, courseName, value, work):
        self.courseName = courseName
        self.value = value
        self.work = work

    def getCourseName(self):
        return self.courseName

    def getValue(self):
        return self.value

    def getWork(self):
        return self.work

    def __str__(self):
        return "Name: " + self.courseName + ", Value: " + str(self.value) + ", Work: " + str(self.work)

def BuildCourseList(subjects):
    #This dictionary is stupid, and hard to sort.  Let's make a class and use that
    courses = []
    for subject in subjects:
        courses.append(Course(subject, subjects[subject][0], subjects[subject][1]))

    return courses
