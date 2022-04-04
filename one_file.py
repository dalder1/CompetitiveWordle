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
    print('\n')

    for word in guesses:
        print(word)
    
    print('\n')

# main function
def main():
    """
        main function
    """

    with open(WORDLIST_FILE) as wordlistFile:
        wordlist = wordlistFile.read().splitlines() 
    
    print('wordlist', wordlist)

    word = wordlist[random.randint(0, len(wordlist))]
    print(word)
    solved = False
    numGuesses = 0
    userGuesses = []
    while(numGuesses < ALLOWED_GUESSES):
        guess = input()
        if (len(guess) != 5):
            print('Guess must be 5 letters.')
        elif(guess not in wordlist):
            print('Word not found in dictionary.')
        elif(guess == word):
            numGuesses += 1
            solved = True
            break
        else:
            userGuesses.append(guess)
            numGuesses += 1
            printGuesses(userGuesses)
    
    if solved:
        print('\033[32m' + 'Great job! You guessed the word in %i guesses!' % numGuesses + '\033[0m')
    else:
        print('\033[31m' + 'The word was %s.' % word + '\033[0m')

    sys.exit(0)

if __name__ == '__main__':
  main()
