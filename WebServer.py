import socket
import sys
import signal

def handler(signum, frame):
    print("Closing Listening Socket")
    listen_socket.close() # Closing listening socket
    raise KeyboardInterrupt

HOST, PORT = 'localhost', int(sys.argv[1])                         # defining the host (in this case localhost) and the port
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creating our listening socket (server socket) 
listen_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  # set socket options so we can reuse the same address after we end this program
listen_socket.bind((HOST,PORT))  # bind our listening socket to the indicated host and port. This socket will listen to that address and port 
listen_socket.listen(1)          # Start listening for connections with a backlog of 1

print("Servin HTTP on port %d" % PORT)

signal.signal(signal.SIGINT,handler)

while True:
    client_connection, client_address = listen_socket.accept() # accept a new connection
    request_data = client_connection.recv(1024)                # receive request from client
    print(request_data.decode("utf-8"))                        # decode request using utf-8 format

    http_response = b'HTTP/1.1 200 OK \n\n <h1>Hello!</h1>'    # response 
    print("response:",http_response) 
    client_connection.sendall(http_response)                   # send response
    client_connection.close()                                  # close connection with client
