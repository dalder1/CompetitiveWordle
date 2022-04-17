#!/usr/bin/env python3

###
### CS 21 Concurrent Programming
### Spring 2022
### Project: Wordle with Friends
### format.py:
###     Format class to format strings for printing
###     by printing correct letters (correct letter, correct position) green,
###     semi-correct letters (correct letter, incorrect position) yellow,
###     and all other letters (wrong) black
### 

class Format:
    def __init__(self):
        self.CORRECT_COLOR = 'green'
        self.SEMI_CORRECT_COLOR = 'yellow'
        self.RESET_COLOR = 'reset'
        self._colors = {
            'reset': '\033[0m',
            'red': '\033[31m',
            'yellow': '\033[93m',
            'green': '\033[32m'
        }

    def format_string(self, word, correct, semi_correct):
        """
            takes in a word, an array of correct indices,
            and an array of semi-correct indices
            returns an ansi string formatted to print colors

            raises exception if number of correct or semi-correct letters,
            is more than the length of the word

            raises error if index out of bounds of words

            input expectations:
            - assumes that if an index is in `correct`, it is NOT in `semi_correct`
        """

        if (len(correct) > len(word) or len(semi_correct) > len(word)):
            raise ValueError("Error: Incorrect number of correct or semi-correct letters.")
        
        # string to array to store info for each letter
        print_arr = list(word)

        # format letter if correct
        for i in correct:
            print_arr[i] = self._colors[self.CORRECT_COLOR] + print_arr[i] + self._colors[self.RESET_COLOR]
        
        # format letter if semi-correct
        for i in semi_correct:
            print_arr[i] = self._colors[self.SEMI_CORRECT_COLOR] + print_arr[i] + self._colors[self.RESET_COLOR]

        # array to string to return string
        print_string = ''.join(map(str, print_arr))

        return print_string
