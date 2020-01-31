from socket import *
from threading import Thread, Lock
import sys
import os
import time


"""
1.60000 connection handshake
2.65000 message connection object create
3.make thread using that connection object as parameter
"""
global message_user_list
global message_user_name_dict
message_user_list = list()
message_user_name_dict = dict()

class ClientManagement(Thread):
    # user_list : Store every client, include myself
    # user_name : Asign name each client
    user_list = message_user_list
    user_name = message_user_name_dict

    def __init__(self, client_connectionSock):
        Thread.__init__(self)
        self.__client_connectionSock = client_connectionSock

    def run(self):
        # Make nickname 
        while True:
            try:
                # Create client nickname
                self.__client_connectionSock.send("[Server] Make your nickname: ".encode('utf-8'))

                self.__client_connectionSock.settimeout(100)
                user_nickname = self.__client_connectionSock.recv(1024).decode('utf-8')
                
                # Check client nickname
                self.__client_connectionSock.settimeout(100)
                check_nickname = "[Server] Is " + user_nickname + " your nickname? : Y | N : "
                self.__client_connectionSock.send(check_nickname.encode('utf-8'))

                self.__client_connectionSock.settimeout(50)
                clientAnswer = self.__client_connectionSock.recv(1024).decode('utf-8')

                # If client send '1' or 'yes', message_user_name_dict is added a client nickname
                if clientAnswer.upper() == 'Y':
                    # Lock.acquire()
                    ClientManagement.user_name[self.__client_connectionSock] = user_nickname
                    # Lock.release()
                    self.__client_connectionSock.send("[Server] Connected!!".encode('utf-8'))
                    self.__client_connectionSock.send("[Server] Your nickname is successfully made".encode('utf-8'))

                    # Lock.acquire()
                    ClientManagement.user_list.append(self.__client_connectionSock)
                    # Lock.release()

                    print("[Server] IP " + str(self.__client_connectionSock.getpeername()) +
                        " was added to user list")
                    break

                # If client send '2' or 'no', send a messgae to client
                elif clientAnswer.upper() == 'N':
                    self.__client_connectionSock.send("[Server] Nickname didn't match".encode('utf-8'))
                    self.__client_connectionSock.send("[Server] Try again".encode('utf-8'))
                    continue

                # If client send a wrong message, send a message to client that you send a wrong message
                else:
                    self.__client_connectionSock.send("[Server] Sorry, your code has been entered incorrectly. Try again".encode('utf-8'))
                    continue

            except Exception as e:
                print("Error code : {}".format(e))
                try:
                    self.__client_connectionSock.send("[Server] Server Error".encode('utf-8'))
                except ConnectionError:
                    break

        self.__show_command()

        while True:
            try:
                # temp_recvData is decoded message
                # recvData is encoded message
                # temp_recvData is check command string
                recvData = self.__client_connectionSock.recv(1024).decode('utf-8')
                temp_recvData = list(recvData)
                if temp_recvData[0] == '/':
                    if self.__check_command(recvData) == -1:
                        break
                else:
                    message = ClientManagement.user_name.get(self.__client_connectionSock) + " : " + recvData
                    print('[Server]', message)
                    encode_message = message.encode('utf-8')
                    for client_object in ClientManagement.user_list:
                        client_object.send(encode_message)
            
            except ConnectionError:
                try:
                    # Lock.acquire()
                    ClientManagement.user_list.remove(self.__client_connectionSock)
                    del user_name[self.__client_connectionSock]
                    # Lock.release()
                    print("[Server] Remove {} client".format(self.__client_connectionSock))
                    break
                except:
                    pass

            except Exception as e:
                print(e)
                pass

    # Show command list to client
    def __show_command(self):
        # command_msg : send a message to client
        command_msg = '\n================ COMMAND LIST ================\n'

        # f : open command.txt
        f = open("C:/Users/wnduf/Documents/Visual_Studio_Code/Server/command.txt", 'r')
        lines = f.readlines()
        for commands in lines:
            command_msg += commands + "\n"
        f.close()
        self.__client_connectionSock.send(command_msg.encode('utf-8'))
    
    # If client send a command, send a command information or run client thread
    def __check_command(self, msg):
        command_msg = ''

        # show command list
        if msg == '/command':
            # print __show_command()
            f = open("C:/Users/wnduf/Documents/Visual_Studio_Code/Server/command.txt", 'r')
            lines = f.readlines()
            for commands in lines:
                command_msg += commands + "\n"
            f.close()
            self.__client_connectionSock.send(command_msg.encode('utf-8'))
            return 0
        # show userlist
        elif msg == '/userlist':
            command_msg += 'UserList : '
            for user in ClientManagement.user_name.values():
                command_msg += user + ','
            self.__client_connectionSock.send(command_msg.encode('utf-8'))
            return 0

        # Run when client exit server
        elif msg == '/exit':
            # Remove clientsock
            # Lock.acquire()
            ClientManagement.user_list.remove(self.__client_connectionSock)
            del ClientManagement.user_name[self.__client_connectionSock]
            # Lock.release()

            # sendData is message for another client
            sendData = "{} is disconnected.".format(self.__client_connectionSock)

            # Check in server
            print("[Server] ", sendData)
            # Send massage for every client
            for client_object in ClientManagement.user_list:
                client_object.send(sendData.encode('utf-8'))
            return -1

        # command that client send isn't exist in server command
        else:
            error_msg = "'{}' command is not exist.".format(msg)
            self.__client_connectionSock.send(error_msg.encode('utf-8'))
            return 1
            
        

class StartNewConnections:
    def __init__(self, handshake_port, message_port):
        # handshake_port : check connection port, message_port : send a message port
        self.__handshake_port = handshake_port
        self.__message_port = message_port

        self.__handshake_sock = socket(AF_INET, SOCK_STREAM)
        self.__message_sock = socket(AF_INET, SOCK_STREAM)

        self.__handshake_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__message_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        print("[Server] Handshake port : " + str(self.__handshake_port))
        print("[Server] Message port : " + str(self.__message_port))
        print("[Server] Starting Server...")


        try:
            self.__handshake_sock.bind(('', self.__handshake_port))
            self.__message_sock.bind(('', self.__message_port))
            print("[Server] Successfully binded sock")

        except:
            print("[Server] Cannot start server")
            exit()

    def check_new_connections(self):
        self.__handshake_sock.listen(1)
        self.__handshake_sock.settimeout(3)

        try:
            handshake_connection_sock, handshake_addr = self.__handshake_sock.accept()
            print("[Server] IP " + str(handshake_addr) + " connected.")

            """
            A method for getting new connections
            When a new connection is set, server sends 200
            If server gets 300 in return, it saves the socket object
            into the user list for future use.
            @param none
            @return none
            """
            handshake_connection_sock.send('200'.encode('utf-8'))
            handshake_connection_sock.settimeout(5)
            temp_data = handshake_connection_sock.recv(1024).decode('utf-8')

            if temp_data == '300':
                self.__message_sock.settimeout(5)
                self.__message_sock.listen(1)

                message_connection_sock, message_addr = self.__message_sock.accept()
                self.__make_new_connection_thread(message_connection_sock)

                print("[Server] Successful make thread!")
            else:
                print("[Server] Wrong code returned")
                
        except Exception as ex:
            # print("Exception Error", ex)
            pass

    def __make_new_connection_thread(self, connection_sock_object):
        print("[Server] Making new thread for " + str(connection_sock_object.getpeername()))
        ClientManagement(connection_sock_object).start()



if __name__ == "__main__":
    SNC = StartNewConnections(60000, 65000)
    while True:
        SNC.check_new_connections()
        # print(message_user_list)

        print("[Server] User list : ", end = "")
        for client in message_user_list:
            print(client.getpeername(), end = ", ")
        print("\n")
        print("[Server] User nickname : ", end = "")
        for client in message_user_list:
            print(client.getpeername(), ":", message_user_name_dict[client], end = ", ")
        print("\n")
