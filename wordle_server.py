#!/usr/bin/env python3

###
### Daniel Alderman, Ann Marie Burke, Ethan Schreiber
### CS 21 Concurrent Programming
### Spring 2022
### Project: Wordle with Friends
### wordle_server.py:
###     Implements the server for the Wordle game
###

import random
import socket, threading
import pickle

from user import User
from status_codes import Status
from thread_safe_list import Thread_Safe_List

WORDLIST_ALL = 'wordlist-large.txt'
WORDLIST_TARGETS = 'wordlist-targets.txt'
WORDLIST = []
MAX_PLAYERS = 3
NUM_WORDS = 5

def player_thread(player_sock, words, users_conns, finalScores, index):
    # get player's name
    name = ""
    try:
        data = pickle.loads(player_sock.recv(1024))
        if data and data["status"] == Status.CLIENT_NAME:
            name = data["name"]
            print("player '" + name + "' joined the game")
        else:
            print("communication error")
            users_conns.remove(player_sock)
            player_sock.close()
            return
    except Exception as x:
        print(x.message)
        users_conns.remove(player_sock)
        player_sock.close()
        return

    # create user
    user = User(name, words)

    # main loop - run game for this client
    while True:
        try:
            # receive a guess
            data = pickle.loads(player_sock.recv(1024))
            if data:
                # guess made case
                if data["status"] == Status.GUESS_MADE:    
                    guess = data["guess"]

                    # validate guess
                    if guess not in WORDLIST:
                        response = {"status": Status.INVALID_GUESS}
                        send_to_player(player_sock, pickle.dumps(response))
                        continue

                    # -- get current word, make guess, and form response --
                    word = user.getWord()
                    status, guesses = user.makeGuess(guess)
                    score = user.getScore()

                    response = {"status": status,
                                "toPrint": guesses,
                                "score": str(score),
                                "word": word}
                    send_to_player(player_sock, pickle.dumps(response))

                    # if game complete, i.e., if user guesses all words
                    if status == Status.GAME_COMPLETE:
                        # make msg = final score, player name
                        broadcast = {"status": Status.GAME_UPDATE,
                                "name": name,
                                "score": str(score),
                                "toPrint": user.getShareBoard()}
                        send_to_all_players(player_sock, 
                                           pickle.dumps(broadcast), users_conns)
                        # add user name + score to array of users
                        finalScores[index] = (name, score)
                        break
                    # if user guesses a word
                    elif (status == Status.CORRECT_GUESS or 
                                               status == Status.OUT_OF_GUESSES):
                        # make msg = final score, player name
                        broadcast = {"status": Status.SCORE_UPDATE,
                                "name": name,
                                "score": str(score),
                                "toPrint": user.getShareBoard()}
                        send_to_all_players(player_sock, 
                                           pickle.dumps(broadcast), users_conns)

                # client quit case
                elif data["status"] == Status.CLIENT_QUIT:
                    print("client disconnected")
                    send_to_player(player_sock, pickle.dumps({"status": 
                                                             Status.TERMINATE}))
                    users_conns.remove(player_sock)
                    player_sock.close()
                    # user gets a score of 0 b/c the user quit the game
                    finalScores[index] = (name, 0)
                    return

                # invalid communication
                else:
                    raise ValueError("Error: invalid status code from client: "
                                                          + str(data["status"]))
        except Exception as err:
            # print and close connection - server should keep running
            print(err)
            users_conns.remove(player_sock)
            player_sock.close()
            return
    # end the game
    print("\nplayer '" + name + "' has finished guessing")
    return user.getScore()

# send_to_player
# takes in current player's socket and message, sends message to current player
def send_to_player(player_sock, msg):
    player_sock.send(msg)


# send_to_all_players
# takes in current player's socket and message, sends message to all players
# except current
def send_to_all_players(player_sock, msg, conn_list):
    # TODO: may run into race condition if client removed during iteration
    for client in conn_list:
        if client != player_sock:
            client.send(msg)


# main
# main function: initializes server and calls game logic
def main():
    global MAX_PLAYERS
    global WORDLIST
    global NUM_WORDS

    # --- game starter can customize game ---
    MAX_PLAYERS = int(input("How many players will be playing? "))

    NUM_WORDS = int(input("How many words do you want? "))


    # --- get target words and guessable words ---
    # get list of all target words
    with open(WORDLIST_TARGETS) as wordlistFile:
        WORDLIST = wordlistFile.read().splitlines()

    # get unique list of words
    words = random.sample(WORDLIST, NUM_WORDS)

    # get all guessable words
    with open(WORDLIST_ALL) as wordlistFile:
        WORDLIST = wordlistFile.read().splitlines()

    # --- server socket setup ---
    conn_list = Thread_Safe_List()

    # socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind
    HOST = 'localhost'
    PORT = 5023
    server_sock.bind((HOST, PORT))

    # listen
    server_sock.listen(1)
    print('Wordle server started on port : ' + str(PORT))

    # loop accepting new clients
    client_threads = []
    finalScores = [None for i in range(MAX_PLAYERS)]
    for i in range(MAX_PLAYERS):
        # accept user connections
        conn, addr = server_sock.accept()
        # add to list and start thread
        conn_list.append(conn)
        thread = threading.Thread(target = player_thread, 
                                  args=[conn, words, conn_list, finalScores, i])
        client_threads.append(thread)
        thread.start()

    # wait for all players to finish their game
    for thread in client_threads:
        thread.join()

    # sort users in descending order
    finalScores.sort(reverse=True, key=lambda tuple: tuple[1])

    # send all users' final scores to all users
    msg = {
        "status": Status.FULL_GAME_COMPLETE,
        "users": finalScores
    }
    send_to_all_players('', pickle.dumps(msg), conn_list)
    for user in conn_list:
        user.close()

if __name__ == "__main__":
    main()

    exit(0)
