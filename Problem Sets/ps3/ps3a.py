# 6.00 Problem Set 3A Solutions
# The 6.00 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name: Matt Graffunder
# Collaborators: None 
# Time Spent: 0:20

import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

	The score for a word is the sum of the points for letters
	in the word multiplied by the length of the word, plus 50
	points if all n letters are used on the first go.

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    score = 0

    #Add letter scores together
    for c in word:
        score += SCRABBLE_LETTER_VALUES[c]

    #Multiply by number of Letters
    score *= len(word)

    #Add 50 Points if word used all letters in hand
    if len(word) == n:
        score += 50

    return score
#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,              # print all on the same line
    print                               # print an empty line

#
# Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
	In other words, this assumes that however many times
	a letter appears in 'word', 'hand' has at least as
	many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    #Copy Hand into New Hand
    newHand = hand.copy()
    
    #Remove used letters from new hand
    for c in word:
        newHand[c] -= 1

    return newHand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """

    #Check that word is in word list
    if not word_bisection_search(word, word_list):
        return False

##    if not word_brute_force_search(word, word_list):
##        return False
    
    #Check that word can be made from letters in hand
    wordLetters = get_frequency_dict(word)  

    for letter in wordLetters:
        if letter not in hand:
            return False
        elif hand[letter] < wordLetters[letter]:
            return False

    return True

def word_bisection_search(word, word_list):
    """
    Return True if the word is in the word_list
    """

    lowGuess = 0
    highGuess = len(word_list)

    guess = (lowGuess + highGuess) / 2

    while guess != lowGuess and guess != highGuess:
        #Get word from list
        guessWord = word_list[guess]

        if guessWord == word:
            return True
        else:
            if guessWord > word:
                highGuess = guess
            else:
                lowGuess = guess

        #choose new guess
        guess = (lowGuess + highGuess) / 2

    #Return False, nothing Found
    return False

def word_brute_force_search(word, word_list):
    """
    Return True if the word is in the word_list
    """
    #Check that word is in word list
    if word in word_list:
        return True
    else:
        return False

def calculate_handlen(hand):
    handlen = 0
    for v in hand.values():
        handlen += v
    return handlen

def SolicitAndReturnWordFromUser():
    """
    Asks the user to choose a word
    Returns a word.

    Will Continue to ask user until provided a single character in A-Za-z
    Will also continue if letter has been guessed
    """

    #Loop until valid letter is choosen.
    while True:
        word = str.lower(raw_input('Enter word, or a "." to indicate that you are finished: '))

        if len(word) == 0:
            print "Please enter a word."
            print        
        else:
            #Check if letter has already been guessed
            return word

def DisplayWordIsInvalid(word):
    print word + " is invalid, please try again."

def DisplayWordResults(word, wordScore, handScore):
    print '"' + str(word) + '" earned ' + str(wordScore) + ' points.',
    DisplayHandScore(handScore)
    
def DisplayHandScore(handScore):
    print "Total: " + str(handScore) + " points."
#
# Problem #4: Playing a hand
#
def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      
    """
    #Initialize
    handScore = 0
    
    while calculate_handlen(hand) > 0:
        print
        
        #Display hand
        display_hand(hand)

        #Get Word from User
        word = SolicitAndReturnWordFromUser()

        #Check if Word is valid - Restart round if it isn't
        if word == ".":
            break
        elif not is_valid_word(word, hand, word_list):
            DisplayWordIsInvalid(word)
            continue
        else:
            wordScore = get_word_score(word, HAND_SIZE)
            handScore += wordScore
            hand = update_hand(hand, word)
            DisplayWordResults(word, wordScore, handScore)

    DisplayHandScore(handScore)

def PromptUserForGameOption():
    #Continue Prompting until a valid response
    while True:
        choice = string.lower(raw_input('n: Play new Hand\nr: Repeat Previous Hand\ne: Exit\nPlease Choose "n", "r", or "e":'))

        if len(choice) > 1 or choice not in 'nre':
                print "Please choose a valid option"
                print
        else:
            return choice

#
# Problem #5: Playing a game
# Make sure you understand how this code works!
# 
def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """

    hand = deal_hand(HAND_SIZE)

    while True:
        #Get Choice From User
        choice = PromptUserForGameOption()

        if choice == 'e':
            return #Exit Game
        elif choice == 'n':
            hand = deal_hand(HAND_SIZE)
            play_hand(hand, word_list)
        elif choice == 'r':
            play_hand(hand, word_list)
  
    
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
    #is_valid_word("asdf", {'a':1}, word_list)
