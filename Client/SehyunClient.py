import threading
import socket

class Client:
    def __init__(self):
        self.port=int("연결할 Port 입력")
        clientSock=socket(AF_INET,SOCK_STREAM)
        clientSock.connect((self.IP,self.port))
    
    def Connection(self):
        recvData=clientSock.recv(1024)
        if (recvData.decode('utf-8')=="200"):
            sendData='300'
            clientSock.send(sendData.encode('utf-8'))
            print("정상적으로 연결이 되었음")
            return true
        else:
            print("정상적으로 연결이 되지 않음")
            return false
            
    def send_get(self):
        self.port=int("매세지 보내고 받을 Port 새로 입력")
        clientSock=socket(AF_INET,SOCK_STREAM)
        clientSock.connect((self.IP,self.port))

    def send_Message(self):
        message=input("Input Message(quit:!!exit)")
        clientSock.send(message.encode('utf-8'))

    def get_Message(self,peer_name):
        recvData=clientSock.recv(1024)
        if (peer_name=='self_IP_address'):
            print()
        else:
            print("{%s}:%s" % (peer_name,recvData.decode('utf-8')))
            
if __name__=="__main__":
    Client cl=new Client()
    if(cl.Connection()):
        cl.send_get()
        while True:
            try:
                threading.Thread(target=send_Message).start()
                threading.Thread(target=get_message).start()
                time.sleep(1)
            except:
                pass
