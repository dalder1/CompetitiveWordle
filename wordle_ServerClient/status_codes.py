from enum import IntEnum, unique

@unique
class Status(IntEnum):
    INCORRECT_GUESS = 0
    CORRECT_GUESS   = 1
    OUT_OF_GUESSES  = 2
    INVALID_GUESS   = 3
    GAME_COMPLETE   = 10
    SCORE_UPDATE    = 11
    TERMINATE       = 20

    GUESS_MADE      = -1
    CLIENT_QUIT     = -2
    CLIENT_NAME     = -3