# user.py
# Contains class that tracks state of player in wordle game

from Format import format_colors
from status_codes import Status

class User:
    __guessNumber = 1

    
    # expects unique name for user
    def __init__(self, name, words):
        self.name = name
        self.words = words
        self.__currentWord = 0
        self.__pastGuesses = [[] for i in range(len(words))]
        self.__print_guesses = ["" for i in range(len(words))]


    def makeGuess(self, guess):
        if (self.__guessNumber < 7) and (self.__currentWord < len(self.words)):
            right = []
            close = []
            word = self.words[self.__currentWord]
            modifiedGuess = guess
            for i in range(5): # find all correct letter
                if(modifiedGuess[i] == word[i]):
                    right.append(i)
                    # prevent duplicates for double letters
                    wordList = list(word)
                    wordList[i] = '#'
                    word = ''.join(wordList)
                    # prevent letter from being both correct and close
                    guessList = list(modifiedGuess)
                    guessList[i]= '*'
                    modifiedGuess = ''.join(guessList)
            for i in range(5): # find all close letters
                if(modifiedGuess[i] in word):
                    close.append(i)
                    #prevent duplcates for double letters
                    word = word.replace(modifiedGuess[i], '#', 1)

            # append to storage arrays
            self.__pastGuesses[self.__currentWord].append((guess, right, close))
            self.__print_guesses[self.__currentWord] = self.__print_guesses[self.__currentWord] + "\n" + format_colors(guess, right, close)
            self.__guessNumber += 1

            # determine return state

            # game complete on correct guess
            if ((guess == self.words[self.__currentWord]) and 
                                   (self.__currentWord >= (len(self.words) -1))):
                return (Status.GAME_COMPLETE, self.__print_guesses[self.__currentWord])
            # word complete on correct guess
            elif (guess == self.words[self.__currentWord]):
                self.__currentWord += 1
                self.__guessNumber = 1
                return (Status.CORRECT_GUESS, self.__print_guesses[self.__currentWord-1])
            # game complete on wrong guess
            elif ((self.__guessNumber == 7) and 
                                   (self.__currentWord >= (len(self.words) -1))):
                return (Status.GAME_COMPLETE, self.__print_guesses[self.__currentWord])
            # word complete on wrong guess
            elif (self.__guessNumber == 7):
                self.__currentWord += 1
                self.__guessNumber = 1
                return (Status.OUT_OF_GUESSES, self.__print_guesses[self.__currentWord-1])
            # word incomplete
            else: 
                return (Status.INCORRECT_GUESS, self.__print_guesses[self.__currentWord])
        else: # caused by making guess after game is already over
            return (Status.INVALID_GUESS,)

    def getScore(self):
        return self.__calculateScore(self.__pastGuesses)

    def __calculateScore(self, pastGuesses):
        return 100