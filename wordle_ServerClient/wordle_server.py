import random
import socket, threading
import pickle
from unicodedata import decimal

def accept_player(word):
    #accept    
    cli_sock, cli_add = ser_sock.accept()
    CONNECTION_LIST.append(cli_sock)
    thread_client = threading.Thread(target = broadcast_player, args=[cli_sock, word])
    thread_client.start()

def broadcast_player(cli_sock, word):
    keepPlaying = True
    while keepPlaying:
        try:
            data = pickle.loads(cli_sock.recv(1024))
            if data:
                guess = data["guess"]
                numGuesses = data["numGuesses"]
                response = dict()
                if (guess == word):
                    response["response"] = "Great job! You guessed the word in " + numGuesses + " guesses." 
                elif (numGuesses >= 5):
                    response["response"] = "sorry you have lost, the word was " + word + "."
                    keepPlaying = False
                else:
                    response["response"] = "try again"
                send_to_player(cli_sock, pickle.dumps(response))
                # send_to_all_players(cli_sock, response.encode())
        except Exception as x:
            print(x.message)
            break

#update of your own score
def send_to_player(cs_sock, msg):
    cs_sock.send(msg)

#update to other players of your score
def send_to_all_players(cs_sock, msg):
    for client in CONNECTION_LIST:
        print("sending")
        if client != cs_sock:
            client.send(msg)

if __name__ == "__main__":    
    CONNECTION_LIST = []
    WORDLIST_FILE = 'wordlist.txt'

    with open(WORDLIST_FILE) as wordlistFile:
        wordlist = wordlistFile.read().splitlines() 
    word = wordlist[random.randint(0, (len(wordlist) - 1))]

    # socket
    ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind
    HOST = 'localhost'
    PORT = 5023
    ser_sock.bind((HOST, PORT))

    # listen    
    ser_sock.listen(1)
    print('Wordle server started on port : ' + str(PORT))
    thread_ac = threading.Thread(target = accept_player, args=(word,))
    thread_ac.start()