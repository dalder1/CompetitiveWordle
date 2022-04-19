import pickle
import socket, threading

from workQueue import WorkQueue

# one thread that handles game, one thread that does all listening

def send(username, client_sock, queue, end_flag):
    prev_print = ""
    while True:
        # take input and send guess
        guess = input("Guess: ")
        # check if client is quitting
        if guess == "quit":
            end_flag.set()
            print("goodbye!")
            client_sock.send(pickle.dumps({"status": 1}))
            break
        # light input validation
        if (len(guess) != 5):
            print("Guess must be 5 letters.")
            continue
        data = {"status": 0, "guess": guess.lower()}
        # send to server
        client_sock.send(pickle.dumps(data))

        # process result
        response = queue.getWork()
        status = response["status"]
        if status == 0:
            prev_print = response["toPrint"]
            print(prev_print)
            print("Score: " + str(response["score"]))
        elif status == 1:
            prev_print = response["toPrint"]
            print(prev_print)
            print("You guessed this word!")
            prev_print = "" # reset for new word
            print("Score: " + str(response["score"]))
        elif status == 2:
            print(response["toPrint"])
            print("You're out of guesses on this word.")
            prev_print = "" # reset for new word
            print("Score: " + str(response["score"]))
        elif status == 10:
            print(response["toPrint"])
            print("You've finished guessing every word!")
            print("Your final score: " + str(response["score"]))
            break
        elif status == 4:
            print(prev_print)
            print("Sorry, that's not in our word list.")


def receive(client_sock, queue, end_flag):
    while True:
        # check if client is quitting
        if end_flag.is_set():
            break
        data = pickle.loads(client_sock.recv(1024))
        if data:
            status = data["status"]
            if status < 10:
                # send to game handler
                queue.addWork(data)
            elif status == 10:
                # end game
                queue.addWork(data)
                # TODO: don't break, keep listening for all scores
                break
            elif status == 11:
                # TODO: print another player's board
                print("someone sent a board lol")
            elif status == 20:
                # disconnect client
                break
            else:
                # TODO: error of some kind?
                print("someone goofed")

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

    client_sock.connect((HOST, PORT))     
    print('Connected to the game...')

    # send name
    client_sock.send(pickle.dumps({"status": 2, "name": username}))

    thread_receive = threading.Thread(target = receive, args=[client_sock, queue, end_flag])
    thread_receive.start()

    thread_send = threading.Thread(target = send, args=[username, client_sock, queue, end_flag])
    thread_send.start()

    thread_send.join()
    thread_receive.join()

    client_sock.close()

if __name__ == "__main__":
    main()
    exit(0)