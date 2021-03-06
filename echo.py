# Import socket module
from socket import *
import sys  # In order to terminate the program
import time


class Server:
    def __init__(self, port_number):
        self.port_number = port_number

    def run(self):
        while True:
            # Add your code her
            sock = socket(AF_INET, SOCK_STREAM)
            sock.bind(('', self.port_number))
            sock.listen(1)
            print("Server is listening")
            #while True:
            #print >>sys.stderr, 'Waiting  for connection'
            connection, client_adress = sock.accept()
            #print >>sys.stderr, 'connection from', client_address
            while True:
                data = connection.recv(1024).decode()
                #print >>sys.stderr, 'received "%s"' % data
                if data:
                    #print >>sys.stderr, 'sending data back to the client'
                    connection.sendall(data.encode())
                else:
                    #print >>sys.stderr, 'no more data from', client_address
                    break
                # Clean up the connection
           # connection.send("OK")
            connection.close()
            
class Client:
    def __init__(self, server_port, server_ip):
        self.server_ip = server_ip
        self.server_port = server_port

    def run(self):
        # Create server socket
        client = socket(AF_INET, SOCK_STREAM)
        client.connect((self.server_ip, self.server_port))

        try:
            msg = input('Enter message: \n')
            while msg.strip():  # strip removes trailing whitespace
                # send message to the echo server
                client.send(msg.encode())
                # receive the reply from the echo server
                reply = client.recv(1024).decode()
                print("Server reply:\n%s" % reply)
                msg = input('Enter message: \n')
        except EOFError:
            pass

        client.close()
        time.sleep(3)# close the connection


if __name__ == '__main__':
    if len(sys.argv) < 3 or (sys.argv[1] == 'c' and len(sys.argv) < 4):
        print('Usage: myprog c <port> <address> or myprog s <port>')
    elif not sys.argv[2].isdigit() or (int(sys.argv[2]) < 1024 or int(sys.argv[2]) > 65535):
        print('port number should be larger than 1023 and less than 65536')
    elif sys.argv[1] == 's':
        server = Server(int(sys.argv[2]))
        server.run()
    elif sys.argv[1] == 'c':
        client = Client(int(sys.argv[2]), sys.argv[3])
        client.run()
    else:
        print('unkonwn commend type %s' % sys.argv[1])
