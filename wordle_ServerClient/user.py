# user.py
# Contains class that tracks state of player in wordle game


from contextlib import nullcontext
from logging import NullHandler


class User:
    __score = 0
    __pastGuesses = []
    __guessNumber = 1
    __guessLimit = None
    words = []

    
    # expects unique name for user
    def __init__(self, name, words):
        self.name = name
        self.words = words
        print(type(self.words))
        print()
        self.__guessLimit = (len(words) * 6) + 1
        self.__currentWord = 0

    def makeGuess(self, guess):
        if (self.__guessNumber < self.__guessLimit) and (self.__currentWord < len(self.words)):
            right = []
            close = []
            for i in range(5):
                if(guess[i] == (self.words[self.__currentWord][i])):
                    right.append(i)
                elif(guess[i] in self.words[self.__currentWord]):
                    close.append(i)
            self.__pastGuesses.append((guess, right, close))
            if (guess == self.words[self.__currentWord]):
                self.__guessNumber += 1
                self.__currentWord += 1
                return ("word correct", self.__pastGuesses)    
            self.__guessNumber += 1
            return ("game continue", self.__pastGuesses)

        else: 
            return ("game over, you lost", self.__pastGuesses)

    def getScore(self):
        return "notdone"

    def __calculateScore(self, pastGuesses):
        return 100