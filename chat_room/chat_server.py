import socket, threading

def accept_client(stop_threads):
    while True:
        #accept    
        cli_sock, cli_add = ser_sock.accept()
        CONNECTION_LIST.append(cli_sock)
        thread_client = threading.Thread(target = broadcast_usr, args=[cli_sock, stop_threads])
        thread_client.start()

def broadcast_usr(cli_sock, stop_threads):
    while True:
        try:
            data = cli_sock.recv(1024)
            if data:
               b_usr(cli_sock, data)
        except Exception as x:
            print(x.message)
            break


def b_usr(cs_sock, msg):
    for client in CONNECTION_LIST:
        if client != cs_sock:
            client.send(msg)

if __name__ == "__main__":    
    CONNECTION_LIST = []

    # socket
    ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind
    HOST = 'localhost'
    PORT = 5023
    ser_sock.bind((HOST, PORT))

    # listen    
    ser_sock.listen(1)
    print('Chat server started on port : ' + str(PORT))
    stop_threads = False
    thread_ac = threading.Thread(target = accept_client, args=(stop_threads,))
    thread_ac.start()