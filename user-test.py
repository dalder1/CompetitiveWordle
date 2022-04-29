#!/usr/bin/env python3

###
### Daniel Alderman, Ann Marie Burke, Ethan Schreiber
### CS 21 Concurrent Programming
### Spring 2022
### Project: Wordle with Friends
### user-test.py:
###     Tests the User class
###

import random
from user import User
from status_codes import Status

WORDLIST_FILE = 'wordlist.txt'

# starts a game for one player with 5 words to guess. Allows for testing user
# class without client or server. 
with open(WORDLIST_FILE) as wordlistFile:
    wordlist = wordlistFile.read().splitlines() 
words = [wordlist[random.randint(0, (len(wordlist) - 1))] for i in range (5)]
game = User("daniel", words)
for i in range(len(words) * 6):
    guess = input()
    correctWord = game.getWord()
    response = game.makeGuess(guess)
    status = response[0]
    prev_print = response[1]
    score = game.getScore()
    if status == Status.INCORRECT_GUESS:
        print(prev_print)
        print("Score: " + str(score))
    elif status == Status.CORRECT_GUESS:
        print(prev_print)
        print("You guessed this word!")
        prev_print = "" # reset for new word
        print("Score: " + str(score))
    elif status == Status.OUT_OF_GUESSES:
        print("You're out of guesses on this word.")
        print(correctWord)
        prev_print = "" # reset for new word
        print("Score: " + str(score))
    elif status == Status.GAME_COMPLETE:
        print("You've finished guessing every word!")
        print("Your final score: " + str(score))
        break
    elif status == Status.INVALID_GUESS:
        print("Sorry, that's not in our word list.")
    print()

