from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
# This creates the server allowing other clients to join 
clients = {}
addresses = {}

HOST = 'localhost'
PORT = 1234
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections(): # This handles sending the welcoming message to incoming connections
    
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to WebChat! Please type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client): # This handles individual clients 
    

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome To WebChat %s! To leave the chatroom, type /quit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        # This tells other clients that one of the clients have left the chat.
        if msg != bytes("/quit", "utf8"): 
            broadcast(msg, name+": ")
       
        else:
            client.send(bytes("/quit", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # This sends each clients messages to other clients
    

    for server_socket in clients:
        server_socket.send(bytes(prefix, "utf8")+msg)

        

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
