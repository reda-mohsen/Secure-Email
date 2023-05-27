import socket, threading
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES

class ClientThread(threading.Thread):
    Client_Master_Keys = {"18P5141@eng.asu.edu.eg": "C\xa9\x8foQw/\xac\xeb\xfc\x9c\xdf%$n\xcc",
                          "18P5722@eng.asu.edu.eg": "x\xeb(\x02vV\xa6\xef\xb9\x00\x08\xa1G\x8f\xe8\x82",
                          "ai.reda.mohsen@gmail.com": "\x0e\x13O\x9b\xack\x89\x13s\x02\xaeS\x8f\xf0\x91\x81"
                          }

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.csocket = clientsocket
        print("[+] New thread started for ", ip, ":", str(port))

    def run(self):
        print("Connection from : ", ip, ":", str(port))
        clientsock.send("Welcome to the multi-thraeded server".encode())
        data = "dummydata"

        iterator = 0
        while len(data):
            if iterator == 0:
                Sender_ID = self.csocket.recv(2048).decode()
                Sender_Secret_Key = self.Get_Secret_Key(Sender_ID)
                Session_Key = self.Generate_Session_Key()
                print(Session_Key)
                Encrypted_Sender_Session_Key = self.Encrypt_Key(Sender_Secret_Key.encode(), Session_Key)
                self.csocket.send(Encrypted_Sender_Session_Key)
                print("Encrypted Sender Session Key Sent:", Encrypted_Sender_Session_Key)
                iterator += 1
            elif iterator == 1:
                Receiver_ID = self.csocket.recv(2048).decode()
                Receiver_Secret_Key = self.Get_Secret_Key(Receiver_ID)
                Encrypted_Receiver_Session_Key = self.Encrypt_Key(Receiver_Secret_Key.encode(), Session_Key)
                self.csocket.send(Encrypted_Receiver_Session_Key)
                print("Encrypted Receiver Session Key Sent:", Encrypted_Receiver_Session_Key)
                iterator += 1
            elif iterator == 2:
                self.csocket.close()
                print("Client at ", self.ip, " disconnected...")
                data = ''

    def Get_Secret_Key(self, email):
        return self.Client_Master_Keys[email]

    def Generate_Session_Key(self):
        return get_random_bytes(16)

    def Encrypt_Key(self, key, message):
        AES_Cipher = AES.new(key, AES.MODE_ECB)
        encrypted_message = AES_Cipher.encrypt(message)
        return encrypted_message


host = "0.0.0.0"
port = 10000
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((host, port))
while True:
    tcpsock.listen(4)
    print("Listening for incoming connections...")
    (clientsock, (ip, port)) = tcpsock.accept()
    # pass clientsock to the ClientThread thread object being created
    newthread = ClientThread(ip, port, clientsock)
    newthread.run()

