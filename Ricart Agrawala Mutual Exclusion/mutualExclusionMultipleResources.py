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
import random

class Message:
    def __init__(self, resourceNumber, senderId, type, time, response):
      self.resourceNumber = resourceNumber
      self.senderId = senderId
      self.type = type
      self.time = time
      self.response = response
      self.receiverId = -1

    def getTime(self):
        return self.time

    def send(self):
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

    def sendToQueue(self, queue):
        for i in range (0, int(len(queue))):
            self.receiverId = queue[i].senderId
            try:
                # Open socket
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverAddress = ('localhost', 9000 + queue[i].senderId)
                mySocket.connect(serverAddress)

                # Send message
                codeMessage = pickle.dumps(self)
                mySocket.send(codeMessage)
                mySocket.close()
            except Exception as e:
                print 'Error sending message to process: ', i,'Erro: ', e

    def sendResponse(self, receiverId):
        self.receiverId = receiverId
        try:
            # Open socket
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverAddress = ('localhost', 9000 + receiverId)
            mySocket.connect(serverAddress)

            # Send message
            codeMessage = pickle.dumps(self)
            mySocket.send(codeMessage)
            mySocket.close()
        except Exception as e:
            print 'Error sending message to process: ', i,'Erro: ', e
class Process:
    def __init__(self, id):
        self.id = id
        self.time = id
        self.resources = [False, False, False] #True while is used by resource, False while not
        self.permissionsToUseResource = [0, 0, 0] #If permission n = 3, the process can use resource n
        self.requestsToUseResources = [False, False, False]
        self.queuesToUseResources = [[], [], []] #Queues to use each resource

    def useResource(self, resourceNumber):
        #del self.queuesToUseResources[resourceNumber][0]
        self.resources[resourceNumber] = True
        useTime = random.randint(5, 10)
        while useTime > 0:
            print 'Using resource ', resourceNumber,'for more ', useTime,' seconds...'
            useTime -= 1
            time.sleep(1)
        self.freeResource(resourceNumber)

    def freeResource(self, resourceNumber):
        self.resources[resourceNumber] = False
        self.requestsToUseResources[resourceNumber] = False
        message = Message(resourceNumber, self.id, 'response', self.time, 'OK')
        message.sendToQueue(self.queuesToUseResources[resourceNumber])
    
    def requestResource(self, resourceNumber):
        print 'Requesting resource: ', resourceNumber
        self.permissionsToUseResource[resourceNumber] = 0
        message = Message(resourceNumber, self.id, 'request', self.time, 'NOT_IMPORTANT')
        self.requestsToUseResources[resourceNumber] = message
        message.send()

    def receiveMessage (self, message):
        #print 'receiving message from process:', message.senderId,' of type: ', message.type,' to resource:', message.resourceNumber,' with reponse: ',message.response
        self.updateProcessTime(message)
        if message.type == 'response':
            self.receiveResponseMessage(message)
        elif message.type == 'request':
            self.receiveRequestMessage(message)
        else:
            print 'Error to receive message: Type "', message.type,'" of message is invalid'

    def receiveResponseMessage(self, message):
        print 'receiving response: ', message.response,' from process: ', message.senderId,' to use resource: ', message.resourceNumber
        if message.response == 'OK':
            self.permissionsToUseResource[message.resourceNumber] += 1
            if self.permissionsToUseResource[message.resourceNumber] == 2:
                self.useResource(message.resourceNumber)

    def receiveRequestMessage(self, message):
        if message.senderId != self.id:
            if self.resources[message.resourceNumber] == False and not self.requestsToUseResources[message.resourceNumber]:
                responseMessage = Message(message.resourceNumber, self.id, 'response', self.time, 'OK')
                responseMessage.sendResponse(message.senderId)
            elif self.resources[message.resourceNumber] == True:
                responseMessage = Message(message.resourceNumber, self.id, 'response', self.time, 'NO')
                responseMessage.sendResponse(message.senderId)
            elif self.resources[message.resourceNumber] == False and self.requestsToUseResources[message.resourceNumber]:
                if message.time < self.requestsToUseResources[message.resourceNumber]:
                    responseMessage = Message(message.resourceNumber, self.id, 'response', self.time, 'OK')
                    responseMessage.sendResponse(message.senderId)
                else:
                    self.queuesToUseResources[message.resourceNumber].append(message)
                    self.queuesToUseResources[message.resourceNumber] = sorted(self.queuesToUseResources[message.resourceNumber], key = Message.getTime)
                    responseMessage = Message(message.resourceNumber, self.id, 'response', self.time, 'NO')
                    responseMessage.sendResponse(message.senderId)
            else:
                print 'Error to receive request: No valid action'

    def updateProcessTime(self, message):
        if self.time < message.time:
            self.time = message.time + 1
        else:
            self.time += 1

def processThread():
    print 'Starting process: ', sys.argv[2]

    while True:
        try:
            time.sleep(random.randint(10, 20))
            resourceNumber = random.randint(0, 2)
            #Check if it's not using any resource
            if not process.resources[resourceNumber] and process.requestsToUseResources[resourceNumber] == False:
                    process.requestResource(resourceNumber)
        except Exception as e:
            print 'Error requesting resource: ', resourceNumber,'Erro: ', e

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
process = Process(int(sys.argv[2]))

def main():
    thread.start_new_thread(receiveThread, ())
    thread.start_new_thread(processThread, ())
    signal.pause()

if __name__ == "__main__":
    sys.exit(main())