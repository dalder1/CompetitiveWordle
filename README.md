# Wordles_with_Friends presents...Competitive Wordle!

## What is Wordle?
[Wordle](https://www.nytimes.com/games/wordle/index.html) is a game created by
Josh Wardle. It's like 
[Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game))
but instead of guessing an opponent's colors, the single player guesses a five
letter word. Green etters are correct (correct letter and correct position), and
yellow letters are semi-correct (correct letter but incorrect position).

## Our Project
Our project is a competitive multiplayer Wordle game where users compete against
each other to solve the most Wordles with the best efficiency. The best
efficiency means in fewer guesses than opponents and with more
correct/semi-correct letters in previous guesses.

## Start a game
To run the game all players must be on the same computer. To start a game, first
run `python3 wordle_server.py`. This starts the server for the game. It will ask
you how many players will be playing, and how many words you want to guess for 
the game. Then in separate terminal windows each player can join the game by 
running `python3 wordle_client.py`. It will prompt you to enter your name, and 
then you can start guessing words. Each user will see their own previous 
guesses, and they'll also receive updates when other users guess words. The game
ends when all users have gone through all the words (either guessing them
correctly or running out of guesses), or if all users quit the game. A user can
quit by typing “quit” or “q”. 


## Overview of Files

`README.md`
- This file.
- Contains information about the project and instructions on how to run it.

`wordle_server.py`
- This contains the code for the game server. It starts the game, runs the game,
and then ends the game when all players are finished guessing.
- The server interacts with the `User` class to update the user object according
to messages sent from the client.

`wordle_client.py`
- This contains the code for the game's clients. It allows the user to guess
words, prints out the user's progress (previous guesses), and also prints out
other users' progress.
- The client uses the `workQueue` class. The producer thread of the client
queues messages received from the server and the consumer pops the messages off
and processes them.

`user.py`
- Contains `User` class.
- The `User` class stores the user's current game state and updates it when
necessary.

`workQueue.py`
- Contains `WorkQueue` class.
- The `WorkQueue` class is a thread safe queue that can be used by a
producer-consumer model to push work onto the queue and pop work off from the
queue.

`thread_safe_list.py`
- Contains `Thread_Safe_List` class.
- The `Thread_Safe_List` class is a Python list that is thread safe. It includes
functions to append to the list and remove from the list, which behave like
`list.append` and `list.remove` in Python, but are thread safe.

`Format.py`
- Contains a function for creating an ANSI-code formatted string.
The string is formatted to print colors for correct and semi-correct letters.

`*-test.py`
- These are test files for testing code.

`wordlist-large.txt`
- This file contains a larger list of guessable 5-letter words - it is taken
from the original Wordle game, and contains 12,972 guessable 5 letter words.

`wordlist-targets.txt`
- This file contains all the possible target words for our game - it is taken
from the original Wordle game, and contains 2,315 common(ish) English words
for use as Wordle answers.