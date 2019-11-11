import os
import random
import socket
import sys
import traceback
from threading import Thread
import json


with open('jokes.json', 'r') as file:
    jokesDB = json.loads(file.read())

total_clients = 0
total_jokes = len(jokesDB)
host = "127.0.0.1"
port = 8000  # arbitrary non-privileged port
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Socket created")
try:
    soc.bind((host, port))
except:
    print("Bind failed. Error : " + str(sys.exc_info()))
    sys.exit()
soc.listen(10)  # queue up to 6 requests
print("Socket now listening")






def start_server():

    # infinite loop- do not reset for every requests
    global total_clients
    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        try:
            Thread(target=clientThread, args=(connection, ip, port)).start()
            total_clients += 1
        except:
            print("Thread did not start.")
            traceback.print_exc()
            soc.close()




def clientThread(connection, ip, port, max_buffer_size=5120):
    is_active = True
    state = 0;
    global total_jokes
    jokes = random.sample(jokesDB, total_jokes)
    index = 0



    while is_active:

        if index == total_jokes:
            print("Server : I have no more jokes to tell.")
            connection.sendall("I have no more jokes to tell.".encode("utf8"))
            is_active = False

        if state == 0:
            connection.sendall("Knock Knock!".encode("utf8"))
            print("Server : Knock Knock!")
            client_input = receive_input(connection, max_buffer_size)
            print("Client : " + client_input)
            if client_input=='who\'s there?':
                state += 1
            else:
                connection.sendall("You are supposed to say, \"Who\'s there?\". Let\'s try again.".encode("utf8"))
                print("Server : You are supposed to say, \"Who\'s there?\". Let\'s try again.")

        if state == 1:
            connection.sendall(jokes[index]['serverSetup'].encode("utf8"))
            print("Server : " + jokes[index]['serverSetup'])
            client_input = receive_input(connection, max_buffer_size)
            print("Client : " + client_input)
            if client_input==jokes[index]['serverSetup'].lower() + " who?":
                state += 1
            else:
                print("Server : You are supposed to say, " + jokes[index]['serverSetup'] + " who?")
                msg = "You are supposed to say, "+ str(jokes[index]['serverSetup']) + " who?"
                connection.sendall(msg.encode("utf8"))


        if state == 2:
            connection.sendall(jokes[index]['serverPunchline'].encode("utf8"))
            print("Server : " + jokes[index]['serverPunchline'])

            connection.sendall("Would you like to listen to another? (Y/N)".encode("utf8"))
            print("Server : Would you like to listen to another? (Y/N)")
            client_input = receive_input(connection, max_buffer_size)
            print("Client : " + client_input)

            if client_input == "y":
                state = 0
                index += 1
            else:
                is_active = False
                global total_clients
                total_clients -= 1
                if total_clients == 0:
                    print("No more client to serve. Server closing")
                    soc.close()
                    os._exit(1)


def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)
    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))
    decoded_input = client_input.decode("utf8").rstrip()
    result = process_input(decoded_input)
    return result


def process_input(input_str):
    return str(input_str).lower()


def main():
    start_server()

if __name__ == "__main__":
    main()
