import random
from user import User

WORDLIST_FILE = 'wordlist.txt'

with open(WORDLIST_FILE) as wordlistFile:
    wordlist = wordlistFile.read().splitlines() 
word = wordlist[random.randint(0, (len(wordlist) - 1))]

game = User("daniel", ["fairy"])
for i in range(7):
    guess = input()
    response = game.makeGuess(guess)
    if ("word correct" in response[0]) or ("game over" in response[0]):
        print(response)
        break
    print(response)

