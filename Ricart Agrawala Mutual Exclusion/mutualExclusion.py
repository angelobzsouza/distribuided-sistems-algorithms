#coding: utf-8
########################################################
# 		      	MUTUAL EXCLUSION RICART-AGRAWALA         #
# Nome: Angelo Bezerra de Souza RA: 726496             #
# Nome: Giuliano Crespe RA: 743543                     #
########################################################
from random import *
import thread
import socket
import sys
import signal
import pickle
import time

class Message:
    def __init__(self, resouceNumber, senderId, type, time, response):
      self.resouceNumber = resouceNumber
      self.senderId = senderId
      self.type = type
      self.time = time
      self.response = response
      self.receiverId

    def getTime(self):
        return self.time

    def send():
        for i in range (0, 3):
            self.receiverId = i
            try:
                # Open socket
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverAddress = ('localhost', 9000 + i)
                mySocket.connect(serverAddress)

                # Send message
                codeMessage = pickle.dumps(self)
                mySocket.send(codeMessage)
                mySocket.close()
            except Exception as e:
                print 'Error sending message to process: ', i,'Erro: ', e     

class Process:
    def __init__(self, id, time):
        self.id = id
        self.time = time
        self.resources = [False, False, False] #True while is used by resource, False while not
        self.permissionsToUseResouce = [0, 0, 0] #If permission n = 3, the process can use resource n
        self.queuesToUseResources = []

    def useResource(self, resourceNumber):
        self.resources[resourceNumber] = True
        useTime = random.randint(5, 10)
        while useTime > 0:
            print 'Using resource ', resourceNumber,'for more ', useTime,' seconds\n'
            useTime -= 1
            sleep(1)
        self.freeResource(resourceNumber)

    def freeResource(self, resourceNumber):
        self.resources[resourceNumber] = False
        self.sendMessage('response', resourceNumber, 'OK')
    
    def requestResource(self, resourceNumber):
        self.sendMessage('request', resourceNumber, 'NOT_IMPORTANT')

    def sendMessage (self, type, resourceNumber, response):
        self.time += 1
        message = Message(resourceNumber, self.id, type, self.time, response)
        message.send()

    def receiveMessage (self, message):
        if message.type == 'response':
            self.receiveResponseMessage(message)
        elif message.type == 'request':
            self.receiveRequestMessage(message)
        else:
            print 'Error to receive message: Type "', message.type,'" of message is invalid'

    def receiveResponseMessage(self, message):

    def receiveRequestMessage(self, message):
        
def processThread():
    print 'Starting process: ', sys.argv[2]

    while True:
        sleep(random.randint(2, 7))
        resourceNumber = random.randint(0, 2)
        #Check if it's not using any resource
        if (not process.resources[resourceNumber] && process.id not in process.queuesToUseResource[resourceNumber]):
            requestResource(resourceNumber)

def receiveThread():
    while True:
        serverPort = int(sys.argv[1])
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            serverSocket.bind(('',serverPort))
            serverSocket.listen(50)
            while True:
                connectionSocket, addr = serverSocket.accept()
                try:
                    data = connectionSocket.recv(1024)
                    message = pickle.loads(data)
                    process.receiveMessage(message)
                except Exception as e:
                    print 'Error to receive message:', e
        except Exception as e:
            print 'Error to open socket:', e

# Starting program
global process 
process = Process(int(sys.argv[2]), int(sys.argv[2]))
def main():
    thread.start_new_thread(receiveThread, ())
    thread.start_new_thread(processThread, ())
    signal.pause()

if __name__ == "__main__":
    sys.exit(main())