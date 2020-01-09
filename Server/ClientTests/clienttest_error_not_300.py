from socket import *

port = 60000

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('aihost.kr', port))

recvData = clientSock.recv(1024).decode('utf-8')
print("[Client] Received " + str(recvData))

clientSock.send("400".encode("utf-8"))
print("[Client] Sent " + str(300))

print('접속 완료')

