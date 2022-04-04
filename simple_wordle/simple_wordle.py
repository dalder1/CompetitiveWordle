#!/usr/bin/env python3

###
### CS 21 Concurrent Programming
### Spring 2022
### Project: Wordle
### one_file.py:
###     simple Python Wordle game in one file
###

import sys
import random

WORDLIST_FILE = 'wordlist.txt'

def printGuesses(guesses):
    print('')

    print("Guesses:")
    for word in guesses:
        print(word)
    
    print('')

# main function
def main():
    """
        main function parses arguments,
        reads in filenames from stdin,
        opens the files,
        populatesthe dictionary with word frequencies of each file, and
        prints out the
    """

    with open(WORDLIST_FILE) as wordlistFile:
        wordlist = wordlistFile.read().splitlines() 
    word = wordlist[random.randint(0, (len(wordlist) - 1))]
    solved = False
    userGuesses = []
    numGuesses = 1
    while (numGuesses < 6):
        guess = input()
        if (len(guess) != 5):
            print('Guess must be 5 letters.')
        elif(guess == word):
            solved = True
            break
        else:
            numGuesses += 1
            userGuesses.append(guess)
            printGuesses(userGuesses)
    
    if solved:
        print('Great job! You guessed the word in %i guesses' % numGuesses)
    else:
        print('The word was %s.' % word)

    sys.exit(0)

if __name__ == '__main__':
  main()
