import os
import socket
from threading import Thread

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8000
try:
    soc.connect((host, port))
except:
    print("Connection Error")
    os._exit(1)


message = ""


def sender_thread():
    while True:
        message = input("")
        if message.lower()=="n":
            soc.sendall(message.encode("utf8"))
            print("Client Terminated")
            soc.close()
            os._exit(1)
        else:
            soc.sendall(message.encode("utf8"))


def receiver_thread():
    while True:
        server_response = soc.recv(5120).decode("utf8")
        print("Server : " + server_response)
        if server_response=="I have no more jokes to tell.":
            soc.close()
            os._exit(1)
            print("Client Terminated")
        if server_response == "":
            soc.close()
            print("Server Error")
            os._exit(1)
            print("Client Terminated")


def main():
    Thread(target=receiver_thread, args=()).start()
    Thread(target=sender_thread, args=()).start()




if __name__ == "__main__":
   main()