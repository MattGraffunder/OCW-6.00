from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """

    #perms = get_perms(hand, HAND_SIZE)

    bestWord = None
    bestWordPoints = 0

    size = len(hand)

    for n in range(1, size +1):
        perms = get_perms(hand, n)
        for word in perms:
            #Need to optimize this.  It's doing a full loop for each permutation
            #Pre sort Word list,
            #Then Implement a bisection search on the sorted list
            if is_valid_word(word, hand, word_list):
                wordScore = get_word_score(word, HAND_SIZE)

                if wordScore > bestWordPoints:
                    bestWord = word
                    bestWordPoints = wordScore

    return bestWord

#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    
    #Initialize
    handScore = 0
    
    while calculate_handlen(hand) > 0:
        print
        
        #Display hand
        display_hand(hand)

        #Get Word from User
        word = comp_choose_word(hand, word_list)

        #Check if Word is valid - Restart round if it isn't
        if word == None:
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

def PromptUserForPlayerOption():
    #Continue Prompting until a valid response
    while True:
        choice = string.lower(raw_input('u: Player plays Hand\nc: Computer Plays Hand\nPlease Choose "u" or "c":'))

        if len(choice) > 1 or choice not in 'uc':
                print "Please choose a valid option"
                print
        else:
            return choice

#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    hand = deal_hand(HAND_SIZE)

    while True:
        #Get Choice From User
        gameChoice = PromptUserForGameOption()

        if gameChoice == 'e':
            return #Exit Game
        elif gameChoice == 'n':
            hand = deal_hand(HAND_SIZE)            
        elif gameChoice == 'r':
            hand = hand
            # Do nothing since we already have the hand we want
        else:
            continue

        playerChoice = PromptUserForPlayerOption()

        if playerChoice == 'u':
            play_hand(hand, word_list)
        elif playerChoice == 'c':
            comp_play_hand(hand, word_list)
        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

    
