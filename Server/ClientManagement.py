from socket import *
from threading import Thread

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
