###
### Daniel Alderman, Ann Marie Burke, Ethan Schreiber
### CS 21 Concurrent Programming
### Spring 2022
### Project: Wordle with Friends
### status_codes.py:
###     Contains status codes for messages sent between our server and client
### 

from enum import IntEnum, unique

@unique
class Status(IntEnum):
    INCORRECT_GUESS    = 0
    CORRECT_GUESS      = 1
    OUT_OF_GUESSES     = 2
    INVALID_GUESS      = 3
    GAME_COMPLETE      = 9
    FULL_GAME_COMPLETE = 10
    SCORE_UPDATE       = 11
    GAME_UPDATE        = 12
    TERMINATE          = 20

    GUESS_MADE         = -1
    CLIENT_QUIT        = -2
    CLIENT_NAME        = -3