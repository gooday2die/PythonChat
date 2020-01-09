from socket import *
import time

port = 60000

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('aihost.kr', port))

recvData = clientSock.recv(1024).decode('utf-8')
print("[Client] Received " + str(recvData))

clientSock.send("300".encode("utf-8"))
print("[Client] Sent " + str(300))

print('Connected to server')

input("Enter for disconnecting the server")

clientSock.send("!!exit()".encode('utf-8'))
print("Disconnected to server")

