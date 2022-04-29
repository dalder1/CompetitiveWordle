#!/usr/bin/env python3

###
### Daniel Alderman, Ann Marie Burke, Ethan Schreiber
### CS 21 Concurrent Programming
### Spring 2022
### Project: Wordle with Friends
### wordle_client.py:
###     Implements the client for the Wordle game
### 

import pickle
import socket, threading

from workQueue import WorkQueue
from status_codes import Status

# --- one thread that handles game, one thread that does all listening ---

def run_game(username, client_sock, queue, end_flag):
    """
        takes a username, socket, thread-safe queue, and event.
        
        the username is the client's username for the game
        the socket is used to send to the server
        the queue is used to grab the server's responses from the listener
        the event is used to signal the listener if the client quits manually

        runs a single client's wordle game - is responsible
        for sending the client's guesses to the server and processing
        the response.
    """
    prev_print = ""
    while True:
        # take input and send guess
        guess = input("Guess: ")

        # check if client is quitting
        if guess == "quit" or guess == "q":
            end_flag.set()
            print("goodbye!")
            client_sock.send(pickle.dumps({"status": Status.CLIENT_QUIT}))
            break
        
        # light input validation
        if (len(guess) != 5):
            print("Guess must be 5 letters.")
            continue
        data = {"status": Status.GUESS_MADE, "guess": guess.lower()}

        # send to server
        client_sock.send(pickle.dumps(data))

        # process result
        response = queue.getWork()
        status = response["status"]
        if status == Status.INCORRECT_GUESS:
            prev_print = response["toPrint"]
            print(prev_print)
            print("Score: " + str(response["score"]))
        elif status == Status.CORRECT_GUESS:
            prev_print = response["toPrint"]
            print(prev_print)
            print("You guessed this word!")
            prev_print = "" # reset for new word
            print("Your score: " + str(response["score"]))
        elif status == Status.OUT_OF_GUESSES:
            print(response["toPrint"])
            print("You're out of guesses on this word. The word was " \
                + response['word'])
            prev_print = "" # reset for new word
            print("Score: " + str(response["score"]))
        elif status == Status.GAME_COMPLETE:
            print(response["toPrint"])
            print("You've gotten through every word.")
            print("Your final score: " + str(response["score"]))
            break
        elif status == Status.INVALID_GUESS:
            print(prev_print)
            print("Sorry, that's not in our word list.")


def receive(client_sock, queue, end_flag):
    """
        takes a socket, thread-safe queue, and event.

        the socket is used to receive messages from the server
        the queue is used to message the server's responses to the game thread
        the event is used to check if the client quits manually

        listens to the server and serves the responses back to the game thread
        future work: prints other clients' boards and scores

        raises value error if invalid status code is received from server
    """
    while True:
        # check if client is quitting
        if end_flag.is_set():
            break
        data = pickle.loads(client_sock.recv(1024))
        if data:
            status = data["status"]
            if status <= Status.GAME_COMPLETE:
                # send to game handler
                queue.addWork(data)
            elif status == Status.FULL_GAME_COMPLETE:
                # game is over
                print("\n** Final scores **")
                for user in data['users']:
                    print(user[0] + ": " + str(user[1]))
                break
            elif status == Status.SCORE_UPDATE:
                print(data['toPrint'])
                print(data['name'] + "'s score: " + data['score'])
            elif status == Status.TERMINATE:
                # disconnect client
                break
            elif status == Status.GAME_UPDATE:
                print("\n" + data['name'] + " has finished with score " + 
                                                                  data['score'])
                print("Guess: ")
            else:
                # wrong status code
                raise ValueError("Error: invalid status code in response " + 
                                                                 "from server.")

def main():
    # socket
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    HOST = 'localhost'
    PORT = 5023

    # set up queue and game ender
    queue = WorkQueue()
    end_flag = threading.Event()

    username = input('Enter your name to enter the game > ')
    while (not username):
        username = input('Please type a name > ')

    client_sock.connect((HOST, PORT))     
    print('Connected to the game...')

    # send name
    client_sock.send(pickle.dumps({"status": Status.CLIENT_NAME, "name": 
                                                                     username}))

    # start receiver
    thread_receive = threading.Thread(target = receive, args=[client_sock, 
                                                               queue, end_flag])
    thread_receive.start()

    # start listener
    thread_send = threading.Thread(target = run_game, args=[username, 
                                                  client_sock, queue, end_flag])
    thread_send.start()

    # join both
    thread_send.join()
    thread_receive.join()

    # only close after both threads complete
    client_sock.close()

if __name__ == "__main__":
    main()
    exit(0)