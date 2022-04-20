# user.py
# Contains class that tracks state of player in wordle game

from Format import format_colors
from status_codes import Status

class User:
    __guessNumber = 1
    __score = 0
    __notClose = []
    __notRight = []

    
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
            self.__resetGuessedLetters(word)
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
            self.__print_guesses[self.__currentWord] = self.__print_guesses[self.__currentWord] + format_colors(guess, right, close) + "\n"
            self.__calculateScore()
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

    def __resetGuessedLetters(self, word):
        if self.__guessNumber == 1:
            self.__notClose = list(word)
            self.__notRight = list(word)

    def getScore(self):
        return self.__score

    def __calculateScore(self):
        currentGuesses = self.__pastGuesses[self.__currentWord]
        lastGuess = currentGuesses[-1]
        print(lastGuess)
        guess = lastGuess[0]
        correctLetters = lastGuess[1]
        closeLetters = lastGuess[2]
        improvedScore = 0  

        if len(correctLetters) == 5: #they guessed the word
            if len(currentGuesses == 1):
                improvedScore += 500
            if len(currentGuesses == 2):
                improvedScore += 250
            if len(currentGuesses == 3):
                improvedScore += 125 
            if len(currentGuesses == 4):
                improvedScore += 75   
            if len(currentGuesses == 5):
                improvedScore += 50

        for letterIndex in correctLetters: # new correct letters
            letter = guess[letterIndex]
            if ((letter in self.__notRight) and (letter in self.__notClose)):
                improvedScore += 100
                self.__notClose.remove(letter)
                self.__notRight.remove(letter)
            elif (letter in self.__notRight):
                improvedScore += 50
                self.__notRight.remove(letter)

        for letterIndex in closeLetters: # new close letters
            letter = guess[letterIndex]
            if (letter in self.__notClose):
                improvedScore += 25
                self.__notClose.remove(letter)

        self.__score += improvedScore