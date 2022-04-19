import random
import socket, threading
import pickle
from unicodedata import decimal

WORDLIST_FILE = 'wordlist.txt'
MAX_PLAYERS = 1

def player_thread(player_sock, words):
    # TODO: call and utilize client class and format class
    #get player's name
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
    score = 0
    for word in words:
        keepPlaying = True
        numGuesses = 0
        while keepPlaying:
            try:
                data = pickle.loads(player_sock.recv(1024))
                if data:
                    if data["status"] == 0:    
                        guess = data["guess"]
                    elif data["status"] == 1:
                        print("client disconnected")
                        send_to_player(player_sock, pickle.dumps({"status": 20}))
                        return
                    if (guess == word):
                        #TODO send actual score and formatted guess
                        score += 100
                        response = {"status": 1, "toPrint": guess, "score": score}
                        if words[-1] == word:
                            response["status"] = 10
                        keepPlaying = False
                    elif (numGuesses >= 5):
                        response = {"status": 2, "toPrint": guess, "score": score}
                        if words[-1] == word:
                            response["status"] = 10
                        keepPlaying = False
                    else:
                        response = {"status": 0, "toPrint": guess, "score": score}
                    numGuesses += 1
                    send_to_player(player_sock, pickle.dumps(response))
            except Exception as x:
                print(x.message)
                break
    #end the game
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
    # --- choose starting word ---
    #TODO: get list of words for the whole game
    with open(WORDLIST_FILE) as wordlistFile:
        wordlist = wordlistFile.read().splitlines() 
    words = [wordlist[random.randint(0, (len(wordlist) - 1))] for x in range(5)]
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

    # TODO: end the game

if __name__ == "__main__":
    main()

    exit(0) 