from socket import *
from threading import Thread
import sys
import os
import time



"""

1.60000 connection handshake
2.65000 message connection object create
3.make thread using that connection object as parameter


"""
global message_user_list
message_user_list = list()

class ClientManagement(Thread):
    # user_list : Store every client, include myself
    # user_name : Asign name each client
    user_list = list()
    user_name = dict()

    def __init__(self, client_connectionSock):
        Thread.__init__(self)
        self.__client_connectionSock = client_connectionSock
        ClientManagement.user_list.append(self.__client_connectionSock)

    def run(self):
        while True:
            # temp_recvData is decoded message
            # recvData is encoded message
            temp_recvData = self.__client_connectionSock.recv(1024)
            recvData = temp_recvData.decode('utf-8')
            if recvData == '!!exit()':
                # Remove clientsock
                ClientManagement.user_list.remove(self.__client_connectionSock)

                # sendData is message for another client
                sendData = "{} is disconnected.".format(self.__client_connectionSock)

                # Check in server
                print("[Server] " + sendData)
                # Send massage for every client
                for client_object in ClientManagement.user_list:
                    client_object.send(sendData.encode('utf-8'))
                break
            else:
                print(self.__client_connectionSock.getpeername(), " :", recvData)
                for client_object in ClientManagement.user_list:
                    client_object.send(recvData.encode('utf-8'))

class StartNewConnections:
    def __init__(self, handshake_port, message_port):
        self.handshake_port = handshake_port
        self.message_port = message_port

        self.handshake_sock = socket(AF_INET, SOCK_STREAM)
        self.message_sock = socket(AF_INET, SOCK_STREAM)

        self.handshake_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.message_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        print("[Server] Handshake port : " + str(self.handshake_port))
        print("[Server] Message port : " + str(self.message_port))
        print("[Server] Starting Server...")


        try:
            self.handshake_sock.bind(('', self.handshake_port))
            self.message_sock.bind(('', self.message_port))
            print("[Server] Successfully binded sock")

        except:
            print("[Server] Cannot start server")
            exit()

    def check_new_connections(self):
        self.handshake_sock.listen(3)
        self.handshake_sock.settimeout(1)

        try:
            handshake_connection_sock, handshake_addr = self.handshake_sock.accept()
            print("[Server] IP " + str(handshake_addr) + " connected.")

            handshake_connection_sock.send('200'.encode('utf-8'))
            handshake_connection_sock.settimeout(5)
            temp_data = handshake_connection_sock.recv(1024).decode('utf-8')

            if temp_data == '300':
                self.message_sock.settimeout(5)
                self.message_sock.listen(1)

                message_connection_sock, message_addr = self.message_sock.accept()
                message_user_list.append(message_connection_sock)

                print("[Server] IP " + str(handshake_connection_sock.getpeername()) +
                      " was added to user list")

                self.make_new_connection_thread(handshake_connection_sock)

            else:
                print("[Server] Wrong code returned")

        except:
            pass

    def make_new_connection_thread(self, connection_sock_object):
        print("[Server] Making new thread for " + str(connection_sock_object.getpeername()))
        ClientManagement(connection_sock_object).start()


if __name__ == "__main__":
    SNC = StartNewConnections(60000, 65000)
    SNC.check_new_connections()
    print(message_user_list)
