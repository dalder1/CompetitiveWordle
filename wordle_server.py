#!/usr/bin/env python3
import random
import socket, threading
import pickle
from user import User
from status_codes import Status
from unicodedata import decimal
from thread_safe_list import Thread_Safe_List

WORDLIST_FILE = 'wordlist.txt'
MAX_PLAYERS = 2
NUM_WORDS = 2

def player_thread(player_sock, words, users_conns, users, index):
    # TODO: this is terrible practice
    global WORDLIST

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

                    # -- make guess and form response --
                    status, guesses = user.makeGuess(guess)
                    score = user.getScore()
                    response = {"status": status,
                                "toPrint": guesses,
                                "score": str(score)}
                    send_to_player(player_sock, pickle.dumps(response))

                    # if game complete
                    if status == Status.GAME_COMPLETE:

                        # make msg = final score, player name
                        broadcast = {"status": Status.GAME_UPDATE,
                                "name": name,
                                "score": str(score)}
                        send_to_all_players(player_sock, pickle.dumps(broadcast), users_conns)
                        # add user name + score to some array of users
                        users[index] = (name, str(score))
                        break
                    # if user guesses a word
                    elif status == Status.CORRECT_GUESS:
                        # make msg = final score, player name
                        broadcast = {"status": Status.SCORE_UPDATE,
                                "name": name,
                                "score": str(score),
                                "toPrint": guesses}
                        send_to_all_players(player_sock, pickle.dumps(broadcast), users_conns)
                        # add user name + score to some array of users
                        users[index] = (name, score)

                # client quit case
                elif data["status"] == Status.CLIENT_QUIT:
                    print("client disconnected")
                    send_to_player(player_sock, pickle.dumps({"status": Status.TERMINATE}))
                    return

                # invalid communication
                else:
                    raise ValueError("Error: invalid status code from client: " + str(data["status"]))
        except Exception as x:
            # print and close connection - server should keep running
            print(x)
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
    global WORDLIST
    # --- choose starting word ---
    # get list of words for the whole game
    with open(WORDLIST_FILE) as wordlistFile:
        WORDLIST = wordlistFile.read().splitlines() 
    words = [WORDLIST[random.randint(0, (len(WORDLIST) - 1))] for x in range(NUM_WORDS)]
    print(words)
    # TODO: make sure words are unique

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
    users = [None for i in range(MAX_PLAYERS)]
    for i in range(MAX_PLAYERS):
        # accept user connections
        conn, addr = server_sock.accept()
        conn_list.append(conn)
        thread = threading.Thread(target = player_thread, args=[conn, words, conn_list, users, i])
        client_threads.append(thread)
        thread.start()

    # TODO: accept more connections for more players
    for thread in client_threads:
        thread.join()

    # sort users in descending order
    users.sort(reverse=True, key=lambda tuple: tuple[1])

    # send all users' final scores to all users
    msg = {
        "status": Status.FULL_GAME_COMPLETE,
        "users": users
    }
    send_to_all_players('', pickle.dumps(msg), conn_list)
    for user in conn_list:
        user.close()

if __name__ == "__main__":
    main()

    exit(0) 