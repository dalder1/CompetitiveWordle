import re
import pickle
import socket, threading

def send(username):
    numGuesses = 1
    while (numGuesses < 6):
        guess = input('\nGuess number ' + str(numGuesses) + ': ')
        if (len(guess) != 5):
            print('Guess must be 5 letters.')
            continue
        data = {"numGuesses": numGuesses, "guess": guess}
        numGuesses += 1
        cli_sock.send(pickle.dumps(data))

def receive():
    while True:
        data = pickle.loads(cli_sock.recv(1024))
        response = data["response"]
        if "Great job!" in response:
            print(response)
            break
        elif "sorry" in response:
            print(response)
            break
        else: 
            print(response)

if __name__ == "__main__":   
    # socket
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    HOST = 'localhost'
    PORT = 5023

    username = input('Enter your name to enter the game > ')

    cli_sock.connect((HOST, PORT))     
    print('Connected to the game...')


    thread_send = threading.Thread(target = send,args=[username])
    thread_send.start()

    thread_receive = threading.Thread(target = receive)
    thread_receive.start()