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
ALLOWED_GUESSES = 6

def printGuesses(guesses):
    print('')

    print("Guesses:")
    for word in guesses:
        print(word)
    
    print('')

# main function
def main():
    """
        main function
    """

    with open(WORDLIST_FILE) as wordlistFile:
        wordlist = wordlistFile.read().splitlines()
    
    word = wordlist[random.randint(0, (len(wordlist) - 1))]
    solved = False
    userGuesses = []
    numGuesses = 1

    print('Please guess a word.')

    while(numGuesses < ALLOWED_GUESSES):
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
        print('\033[32m' + 'Great job! You guessed the word in %i guesses!' % numGuesses + '\033[0m')
    else:
        print('\033[31m' + 'The word was %s.' % word + '\033[0m')

    sys.exit(0)

if __name__ == '__main__':
  main()
