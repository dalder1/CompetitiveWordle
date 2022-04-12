import random
import socket, threading
import pickle
from unicodedata import decimal

WORDLIST_FILE = 'wordlist.txt'

def accept_player(word, server_sock, conn_list):
    # accept
    conn, addr = server_sock.accept()
    # TODO: not thread safe
    conn_list.append(conn)
    thread_client = threading.Thread(target = player_thread, args=[conn, word])
    thread_client.start()
    thread_client.join()

def player_thread(player_sock, word):
    keepPlaying = True
    while keepPlaying:
        try:
            data = pickle.loads(player_sock.recv(1024))
            if data:
                guess = data["guess"]
                numGuesses = data["numGuesses"]
                response = dict()
                if (guess == word):
                    response["response"] = "Great job! You guessed the word in " + str(numGuesses) + " guesses."
                    # TODO: create new word, continue game
                    keepPlaying = False
                elif (numGuesses >= 5):
                    response["response"] = "sorry you have lost, the word was " + word + "."
                    keepPlaying = False
                else:
                    response["response"] = "try again"
                send_to_player(player_sock, pickle.dumps(response))
                # send_to_all_players(player_sock, response.encode())
        except Exception as x:
            print(x.message)
            break

# send_to_player
# takes in current player's socket and message, sends message to current player
def send_to_player(player_sock, msg):
    player_sock.send(msg)


# send_to_all_players
# takes in current player's socket and message, sends message to all players
# except current
def send_to_all_players(player_sock, msg):
    for client in conn_list:
        print("sending")
        if client != player_sock:
            client.send(msg)


# main
# main function: initializes server and calls game logic
def main():
    # --- choose starting word ---
    #TODO: get list of words for the whole game
    with open(WORDLIST_FILE) as wordlistFile:
        wordlist = wordlistFile.read().splitlines() 
    word = wordlist[random.randint(0, (len(wordlist) - 1))]
    print('Chosen word: ' + word)

    # --- server socket setup ---
    conn_list = []

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
    thread_ac = threading.Thread(target = accept_player, args=(word, server_sock, conn_list))
    thread_ac.start()
    # TODO: accept more connections for more players
    thread_ac.join()

    for con in conn_list:
        con.close()

if __name__ == "__main__":
    main()

    exit(0) 