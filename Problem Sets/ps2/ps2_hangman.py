# 6.00 Problem Set 2 - Hangman
# Name: Matt Graffunder
# Collaborators: None 
# Time Spent: 1:00


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()

# your code begins here!

def hangman():
    """
    Play Hangman
    """

    #Initialize game
    numberOfGuesses = 8
    letterTracker = {} #Dictionary: Key: letter, Value: bool (has  been guessed)
    wordGuessed = False
    
    for c in string.ascii_lowercase:
        letterTracker[c] = False

    #Select Word
    word = choose_word(wordlist)

    #Display Welcome statement
    PrintWelcomeStatement(len(word))

    #Main game loop, exit if word is guessed or guesses are exhusted
    while not wordGuessed and numberOfGuesses > 0:
        #Print Separators
        PrintRoundSeparator()

        #Print the visible parts of the word
        PrintGuessedPartOfWord(word, letterTracker)
        
        #Display Number of Guesses
        PrintRemainingGuesses(numberOfGuesses) 
        
        #Display Remaining Letters
        PrintRemainingLetters(letterTracker)
        
        #Ask user for guess
        guess = SolicitAndReturnGuessFromUser(letterTracker)
        letterTracker[guess] = True
        
        #Display if guess is correct or not
        if guess in word:
            PrintLetterIsInWord()            
            wordGuessed = CheckIfWordHasBeenGuessed(word, letterTracker)
        else:
            PrintLetterIsNotInWord()
            numberOfGuesses -= 1 #If guess is incorrect decrement the number of guesses

    #Print Separators
    PrintRoundSeparator()
    
    if wordGuessed:
        PrintGuessedPartOfWord(word, letterTracker)
        PrintGameWin() #If user guesses all letters, Display victory statement
    else:
        PrintWord(word)
        PrintGameLose() #If user fails to guess all letter before guesses run out, display defeat statement
       
    return

#Display Helper Functions

def PrintWelcomeStatement(lengthOfWord):
    print "Welcome to the game, Hangman!"
    print "I am thinking of a word that is " + str(lengthOfWord) + " letters long."

def PrintRemainingGuesses(numberOfGuessesRemaining):
    print "You have " + str(numberOfGuessesRemaining) + " guesses left."

def PrintGuessedPartOfWord(word, letterTracker):
    print "Word: ",

    display = []

    for c in word:
        if letterTracker[c]:
            display.append(c)            
        else:
            display.append("_ ")
            
    print "".join(display) # Print Empty string to terminate inline prints

def PrintRoundSeparator():
    print "-" * 10
    print ""    

def SolicitAndReturnGuessFromUser(letterTracker):
    """
    Asks the user to pick a letter
    Returns a single lowercase letter.

    Will Continue to ask user until provided a single character in A-Za-z
    Will also continue if letter has been guessed
    """

    valid = False
    letter = ""    

    #Loop until valid letter is choosen.
    while True:
        letter = str.lower(raw_input("Please guess a letter: "))

        if len(letter) > 1:
            print "Please Choose a SINGLE letter."
            print
        elif letter not in string.lowercase:
            print "Please Choose a LETTER, not a number or special character."
            print
        else:
            #Check if letter has already been guessed
            if letterTracker[letter]:
                print "Letter: " + letter + " has already been chosen, pick again"
                print
            else:
                return letter

def PrintRemainingLetters(letterDict):
    print "Available letters: ",

    display = []
    
    for c in string.ascii_lowercase:
        if letterDict[c]:
            display.append("_")
        else:
            display.append(c)

    print "".join(display) # Print Empty string to terminate inline prints
        
def PrintLetterIsInWord():
    print "Good Guess!"

def PrintLetterIsNotInWord():
    print "Oops, that isn't correct."

def CheckIfWordHasBeenGuessed(word, letterTracker):
    """
    Returns True if all letters in the word have been guessed.
    """
    guessed = True
    
    for c in word:
        guessed = guessed and letterTracker[c]

    return guessed

def PrintGameWin():
    print "Congratulations, you won!"
    
def PrintGameLose():
    print "Sorry, you lost.  Try Again!"

def PrintWord(word):
    print "Word: " + word
