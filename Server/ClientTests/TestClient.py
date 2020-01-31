from socket import *
from threading import Thread

port1 = 60000
port2 = 65000


class Test(Thread):
    def __init__(self, message_sock):
        Thread.__init__(self)
        self.message_sock = message_sock

    def run(self):
        while True:
            try:
                message = self.message_sock.recv(1024).decode('utf-8')
                print(message)

            except Exception as e:
                print("Error code: ", e)
                break

clientSock1 = socket(AF_INET, SOCK_STREAM)
clientSock1.connect(('localhost', port1))

recvData = clientSock1.recv(1024).decode('utf-8')
print("[Client] Received " + str(recvData))

clientSock1.send("300".encode("utf-8"))
print("[Client] Sent " + str(300))

clientSock2 = socket(AF_INET, SOCK_STREAM)
clientSock2.connect(('localhost', port2))

print('접속 완료')

Test(clientSock2).start()

while True:
    try:
        send_massage = input("[Client] Send: ")
        if send_massage == "!!exit()":
            clientSock2.send(send_massage.encode('utf-8'))
            break
        else:
            clientSock2.send(send_massage.encode('utf-8'))
    except:
        break
