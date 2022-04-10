import re
import pickle
import socket, threading

#TODO: one thread that sends/receives for your game, one thread that receives updates on others' games

def send(username, client_sock):
    numGuesses = 0
    while (numGuesses < 6):
        guess = input('\nGuess number ' + str(numGuesses) + ': ')
        # TODO: do error handling of guess on backend (in wordlist, is valid word etc)
        if (len(guess) != 5):
            print('Guess must be 5 letters.')
            continue
        numGuesses += 1
        data = {"numGuesses": numGuesses, "guess": guess}
        print(type(client_sock))
        client_sock.send(pickle.dumps(data))

def receive(client_sock):
    while True:
        data = pickle.loads(client_sock.recv(1024))
        #TODO: send flag field instead of searching in response
        response = data["response"]
        if "Great job!" in response:
            print(response)
            break
        elif "sorry" in response:
            print(response)
            break
        else: 
            print(response)

def main():
    # socket
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    HOST = 'localhost'
    PORT = 5023

    username = input('Enter your name to enter the game > ')

    client_sock.connect((HOST, PORT))     
    print('Connected to the game...')

    print(type(client_sock))

    thread_send = threading.Thread(target = send, args=[username, client_sock])
    thread_send.start()

    thread_receive = threading.Thread(target = receive, args=[client_sock])
    thread_receive.start()

    thread_send.join()
    thread_receive.join()

    client_sock.close()

if __name__ == "__main__":
    main()
    exit(0)