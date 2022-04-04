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
    print('\n')

    for word in guesses:
        print(word)
    
    print('\n')

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
    
    print('wordlist', wordlist)

    word = wordlist[random.randint(0, len(wordlist))]
    print(word)
    solved = False
    numGuesses = 0
    userGuesses = []
    while(numGuesses < 6):
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
        print('Great job! You guessed the word in %i guesses' % numGuesses)
    else:
        print('The word was %s.' % word)

    sys.exit(0)

if __name__ == '__main__':
  main()
