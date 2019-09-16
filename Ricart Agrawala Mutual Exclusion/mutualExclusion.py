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
import threading

class Message:
    def __init__(self, senderId, time, type, response):
      self.senderId = senderId
      self.type = type
      self.time = time
      self.response = response

    def getTime(self):
        return self.time

    def sendRequestInBroadcast(self):
        for i in range (0, 3):
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
                print 'Error sending request to process: ', i,'Erro: ', e

    def sendToQueue(self, queue):
        for i in range (0, int(len(queue))):
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
                print 'Error sending response to process: ', i,'Erro: ', e

    def sendResponse(self, receiverId):
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
            print 'Error sending response to process: ', i,'Erro: ', e

class Process:
    def __init__(self, id):
        self.id = id
        self.time = id
        self.usingResource = False
        self.waitingToUseResource = False #True if waiting to use resource
        self.permissionsToUseResource = 0
        self.queueToUseResource = [] #Queue to use resource

    def useResource(self):
        self.usingResource = True
        useTime = random.randint(5, 10)
        while useTime > 0:
            print 'Using resource for more ', useTime,' seconds...'
            useTime -= 1
            time.sleep(1)

    def freeResource(self):
        self.usingResource = False
        self.waitingToUseResource = False
        self.permissionsToUseResource = 0
        message = Message(self.id, self.time, 'response', 'OK')
        message.sendToQueue(self.queueToUseResource)
        self.queueToUseResource = []
    
    def requestResource(self):
        print 'Requesting to use resource'
        message = Message(self.id, self.time, 'request', 'NOT_IMPORTANT')
        self.waitingToUseResource = message
        message.sendRequestInBroadcast()

    def receiveMessage (self, message):
        self.updateProcessTime(message)
        if message.type == 'response':
            self.receiveResponseMessage(message)
        elif message.type == 'request':
            self.receiveRequestMessage(message)
        else:
            print 'Error to receive message: Type "', message.type,'" of message is invalid'

    def receiveResponseMessage(self, message):
        print 'receiving response: ', message.response,' from process: ', message.senderId,' to use resource'
        if message.response == 'OK':
            self.permissionsToUseResource += 1
            if self.permissionsToUseResource == 2:
                self.usingResource = True

    def receiveRequestMessage(self, message):
        if message.senderId != self.id:
            if not self.usingResource and not self.waitingToUseResource:
                responseMessage = Message(self.id, self.time, 'response', 'OK')
                responseMessage.sendResponse(message.senderId)
            elif self.usingResource == True:
                self.queueToUseResource.append(message)
                self.queueToUseResource = sorted(self.queueToUseResource, key = Message.getTime)
                responseMessage = Message(self.id, self.time, 'response', 'NO')
                responseMessage.sendResponse(message.senderId)
            elif not self.usingResource and self.waitingToUseResource:
                if message.time < self.waitingToUseResource.time:
                    responseMessage = Message(self.id, self.time, 'response', 'OK')
                    responseMessage.sendResponse(message.senderId)
                else:
                    self.queueToUseResource.append(message)
                    self.queueToUseResource = sorted(self.queueToUseResource, key = Message.getTime)
                    responseMessage = Message(self.id, self.time, 'response', 'NO')
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
            time.sleep(random.randint(10, 15))
            #Check if it's not using resource
            if not process.usingResource and not process.waitingToUseResource:
                    process.requestResource()
        except Exception as e:
            print 'Error requesting resource: ', e

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

def useResourceThread():
    while True:
        if process.usingResource == True:
            process.useResource()
            process.freeResource()

# Starting program
global process 
process = Process(int(sys.argv[2]))

def main():
    thread.start_new_thread(receiveThread, ())
    thread.start_new_thread(processThread, ())
    thread.start_new_thread(useResourceThread, ())
    signal.pause()

if __name__ == "__main__":
    sys.exit(main())