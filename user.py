# Contains class that tracks state of player in wordle game and their score

from Format import format_colors
from status_codes import Status

class User:
    """
    A class to represent a wordle game.

    ...

    Public Attributes
    ----------
    name : str
        name of the person
    words : [str]
        list of strings that are the correct words

    Private Attributes
    ----------
    __guessNumber : int
        the nth guess the user is on for that word indexing starting at 1 (1-7)
    __score : int
        the user's current score
    __prevClose : [char]
        list of characters (for the word the user is trying to guess) that have 
        been guessed but not in the correct spot (only yellow)
    __prevRight : [int]
        list of indices (for the words the user is trying to guess) that have
        already been guessed in the correct spot (green)
    __currentWord : int
        index of the current word that the game is on, in relation to self.words
    __pastGuesses : [[{str, [int], [int]}]]
        list of lists that stores all previous guesses made by the user. The
        outer list represents the guess for each word, and the interior list is
        a list of tuples that represent the individual guess for that word. 
        Each tuple is a made up of a string that is the word guessed, a list of
        ints that is every correct (green) letter in the guess, and a list of 
        ints that is every close (yellow) letter in the guess. 
    __printGuesses: [str]
        list of strings where each string represents the output for that word.
        Each string is fully formatted so it prints the correct color for each
        word based on the guesses made. 

    Public Methods
    -------
    getWord():
        returns the word that the user is currently trying to guess
    makeGuess(guess):
        This is the main function that facilitates playing the game. It expects 
        a 5 letter string and processes the guess according to the rules of 
        wordle. Returns a tuple containing a status code based on the state of 
        the game and the formatted string based on the guesses made. 
    getScore():
        returns the user's current score
    
    Private Methods
    -------
    __resetGuessedLetters():
        If it is a user's first guess for the current word it clears the current
        contents of self.__prevClose and self.__prevRight. It returns nothing 
        but self.__prevClose and self.__prevRight are updated by reference. 
    __calculateScore():
        Updates the self.__score attribute based on the most current guess made.
        It accounts for previously guessed letters by using self.__prevClose and
        self.__prevRight and accurately updates the score.  
    """
    __guessNumber = 1
    __score = 0
    prevRight = []
    prevClose = []

    
    def __init__(self, name, words):
        '''expects the name of the user as a string and the list of words they
           must guess. Initalizes the name, words, __currentWod, __pastGuesses,
           and __printGuesses attributes.'''
        self.name = name
        self.words = words
        self.__currentWord = 0
        self.__pastGuesses = [[] for i in range(len(words))]
        self.__printGuesses = ["" for i in range(len(words))]


    def getWord(self):
        '''returns the word that the user is currently trying to guess'''
        return self.words[self.__currentWord]

    def makeGuess(self, guess):
        '''This is the main function that facilitates playing the game. It 
           expects a 5 letter string and processes the guess according to the 
           rules of wordle. It also updates their score based on the guess. It
           Returns a tuple containing a status code based on the state of the 
           game and the formatted string to print based on the guesses made.'''
        if (self.__guessNumber < 7) and (self.__currentWord < len(self.words)):
            right = []
            close = []
            word = self.words[self.__currentWord]
            self.__resetGuessedLetters()
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
                    # prevent duplcates for double letters
                    word = word.replace(modifiedGuess[i], '#', 1)

            # append to storage arrays
            self.__pastGuesses[self.__currentWord].append((guess, right, close))
            self.__print_guesses[self.__currentWord] = self.__print_guesses[self.__currentWord] + "\n" + format_colors(guess, right, close)
            self.__calculateScore()
            self.__guessNumber += 1

            # determine return state

            # game complete on correct guess
            if ((guess == self.words[self.__currentWord]) and 
                                  (self.__currentWord >= (len(self.words) -1))):
                return (Status.GAME_COMPLETE, 
                                        self.__printGuesses[self.__currentWord])
            # word complete on correct guess
            elif (guess == self.words[self.__currentWord]):
                self.__currentWord += 1
                self.__guessNumber = 1
                return (Status.CORRECT_GUESS, 
                                      self.__printGuesses[self.__currentWord-1])
            # game complete on wrong guess
            elif ((self.__guessNumber == 7) and 
                                   (self.__currentWord >= (len(self.words) -1))):
                return (Status.GAME_COMPLETE, 
                                        self.__printGuesses[self.__currentWord])
            # word complete on wrong guess
            elif (self.__guessNumber == 7):
                self.__currentWord += 1
                self.__guessNumber = 1
                return (Status.OUT_OF_GUESSES, 
                                      self.__printGuesses[self.__currentWord-1])
            # word incomplete
            else: 
                return (Status.INCORRECT_GUESS, 
                                        self.__printGuesses[self.__currentWord])
        else: # caused by making guess after game is already over
            return (Status.INVALID_GUESS,)

    def __resetGuessedLetters(self):
        '''If it is a user's first guess for the current word it clears the 
           current contents of self.__prevClose and self.__prevRight. It returns
           nothing but self.__prevClose and self.__prevRight are updated by 
           reference.'''
        if self.__guessNumber == 1:
            self.prevRight = []
            self.prevClose = []

    def getScore(self):
        '''Returns the user's current score'''
        return self.__score

    def __calculateScore(self):
        '''Updates the self.__score attribute based on the most current guess 
           made. It accounts for previously guessed letters by using 
           self.__prevClose and self.__prevRight and accurately updates the 
           score. '''
        currentGuesses = self.__pastGuesses[self.__currentWord]
        lastGuess = currentGuesses[-1]
        guessWord = lastGuess[0]
        correctLetters = lastGuess[1]
        closeLetters = lastGuess[2]

        notClose = list(self.getWord())
        for letter in self.prevClose:
            notClose.remove(letter)

        if len(correctLetters) == 5: # they guessed the word
            if len(currentGuesses) == 1:
                self.__score += 500
            if len(currentGuesses) == 2:
                self.__score += 250
            if len(currentGuesses) == 3:
                self.__score += 125 
            if len(currentGuesses) == 4:
                self.__score += 75   
            if len(currentGuesses) == 5:
                self.__score += 50

        prevLetters = []        
        for letterIndex in correctLetters: # check for new correct letters
            letter = guessWord[letterIndex]
            if ((letterIndex not in self.prevRight) and 
                                                (letter not in self.prevClose)): 
                # letter was not previously yellow or green
                self.__score += 100
                self.prevRight.append(letterIndex)
                self.prevClose.append(letter)
            elif ((letterIndex not in self.prevRight) and 
                              (letter in prevLetters) and (letter in notClose)):
                # letter was previously green but it is a duplicate, has a
                # matching duplicate in the word to guess, and was not 
                # previously yellow. 
                self.__score += 100
                self.prevRight.append(letterIndex)
                self.prevClose.append(letter)
                notClose.remove(letter)
            elif (letterIndex not in self.prevRight):
                # letter was previously yellow but not green
                self.__score += 50
                self.prevRight.append(letterIndex)
            prevLetters.append(letter)

        for letterIndex in closeLetters: # checking for new close letters
            letter = guessWord[letterIndex]
            if (letter not in self.prevClose):
                # letter was not previously yellow
                self.__score += 25
                self.prevClose.append(letter)
            elif ((letter in prevLetters) and (letter in notClose)):
                # letter was previously yellow but is a duplicate and has a 
                # matching dupliate in the word to guess
                self.__score += 25
                notClose.remove(letter)
                self.prevClose.append(letter)
            prevLetters.append(letter)
