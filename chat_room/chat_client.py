import socket, threading

def send(username):
    while True:
        msg = input('\nMe > ')
        data = username + '>' + msg
        cli_sock.send(data.encode())

def receive():
    while True:
        data = cli_sock.recv(1024)
        print('\n'+ str(data.decode()))

if __name__ == "__main__":   
    # socket
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    HOST = 'localhost'
    PORT = 5023

    username = input('Enter your name to enter the chat > ')

    cli_sock.connect((HOST, PORT))     
    print('Connected to remote host...')


    thread_send = threading.Thread(target = send,args=[username])
    thread_send.start()

    thread_receive = threading.Thread(target = receive)
    thread_receive.start()