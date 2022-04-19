# user.py
# Contains class that tracks state of player in wordle game


class User:
    __guessNumber = 1

    
    # expects unique name for user
    def __init__(self, name, words):
        self.name = name
        self.words = words
        print(type(self.words))
        print()
        self.__currentWord = 0
        self.__pastGuesses = [None] * len(words)


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

            if (self.__pastGuesses[self.__currentWord] == None):
                self.__pastGuesses[self.__currentWord] = [(guess, right, close)]
            else: 
                self.__pastGuesses[self.__currentWord].append((guess, right, close))
            self.__guessNumber += 1
            if ((guess == self.words[self.__currentWord]) and 
                                   (self.__currentWord >= (len(self.words) -1))):
                return ("game over, you won", self.__pastGuesses)
            elif (guess == self.words[self.__currentWord]):
                self.__currentWord += 1
                self.__guessNumber = 1
                return ("word correct", self.__pastGuesses)
            elif ((self.__guessNumber == 7) and 
                                   (self.__currentWord >= (len(self.words) -1))):
                return ("game over, you lost", self.__pastGuesses)
            elif (self.__guessNumber == 7):
                self.__currentWord += 1
                self.__guessNumber = 1
                return ("you didnt get this word, good luck on next one", self.__pastGuesses)
            else: 
                return ("game continue", self.__pastGuesses)
        else: # caused by making guess after game is already over
            return ("error: game is already over",)

    def getScore(self):
        return self.__calculateScore(self.__pastGuesses)

    def __calculateScore(self, pastGuesses):
        return 100