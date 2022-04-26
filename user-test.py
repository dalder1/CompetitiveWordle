import random
from user import User

WORDLIST_FILE = 'wordlist.txt'

with open(WORDLIST_FILE) as wordlistFile:
    wordlist = wordlistFile.read().splitlines() 
# word = wordlist[random.randint(0, (len(wordlist) - 1))]
words = ["fairy", "memor", "large", "apple"]
game = User("daniel", words)
for i in range(len(words) * 6):
    guess = input()
    response = game.makeGuess(guess)
    if ("game over" in response[0]):
        print(response)
        break
    print(response)

