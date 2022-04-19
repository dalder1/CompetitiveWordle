import random
import socket, threading
import pickle
from user import User
from unicodedata import decimal

WORDLIST_FILE = 'wordlist.txt'
MAX_PLAYERS = 1

def player_thread(player_sock, words):
    # TODO: this is terrible practice
    global WORDLIST

    # get player's name
    name = ""
    try:
        data = pickle.loads(player_sock.recv(1024))
        if data and data["status"] == 2:
            name = data["name"]
            print("player '" + name + "' joined the game")
        else:
            print("communication error")
            player_sock.close()
            return
    except Exception as x:
        print(x.message)
        player_sock.close()
        return

    # create user
    user = User(name, words)
    while True:
        try:
            data = pickle.loads(player_sock.recv(1024))
            if data:
                if data["status"] == 0:    
                    guess = data["guess"]
                    if guess not in WORDLIST:
                        response = {"status": 4}
                        send_to_player(player_sock, pickle.dumps(response))
                        continue
                    status, guesses = user.makeGuess(guess)
                    response = {"status": status,
                                "toPrint": guesses,
                                "score": user.getScore()}
                    send_to_player(player_sock, pickle.dumps(response))
                    if status == 10:
                        break
                elif data["status"] == 1:
                    print("client disconnected")
                    send_to_player(player_sock, pickle.dumps({"status": 20}))
                    return
        except Exception as x:
            print(x.message)
            break
    # end the game
    print("player '" + name + "' has finished guessing")
    player_sock.close()

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
    global WORDLIST
    # --- choose starting word ---
    # get list of words for the whole game
    with open(WORDLIST_FILE) as wordlistFile:
        WORDLIST = wordlistFile.read().splitlines() 
    words = [WORDLIST[random.randint(0, (len(WORDLIST) - 1))] for x in range(5)]
    print(words)

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

    # loop accepting new clients
    client_threads = []
    for i in range(MAX_PLAYERS):
        # accept
        conn, addr = server_sock.accept()
        # TODO: not thread safe
        conn_list.append(conn)
        thread = threading.Thread(target = player_thread, args=[conn, words])
        client_threads.append(thread)
        thread.start()

    # TODO: accept more connections for more players
    for thread in client_threads:
        thread.join()

    # TODO: end the game (send scores etc)

if __name__ == "__main__":
    main()

    exit(0) 