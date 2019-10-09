#coding: utf-8
########################################################
# 		      	BULLY ALGORITHM                        #
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
    def __init__(self, senderId, time, type, ack, data):
        self.senderId = senderId
        self.time = time
        self.type = type
        self.ack = ack
        self.data = data

    # Send message in broadcast for each process
    def sendToAll(self):
        for i in range (0, 5):
            try:
                # Open socket
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverAddress = ('localhost', 9000 + i)
                mySocket.connect(serverAddress)

                # Send message
                self.receiverId = i
                codeMessage = pickle.dumps(self)
                mySocket.send(codeMessage)
                mySocket.close()
            except Exception as e:
                print 'Error sending request to process: ', i,'Erro: ', e

    # Send message in broadcast for a specific process
    def sendToOne(self, receiverId):
        for i in range (0, 5):
            try:
                # Open socket
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverAddress = ('localhost', 9000 + i)
                mySocket.connect(serverAddress)

                # Send message
                self.receiverId = receiverId
                codeMessage = pickle.dumps(self)
                mySocket.send(codeMessage)
                mySocket.close()
            except Exception as e:
                print 'Error sending request to process: ', i,'Erro: ', e

    def sendToGreater(self):
        for i in range (self.senderId + 1, 5):
            try:
                # Open socket
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverAddress = ('localhost', 9000 + i)
                mySocket.connect(serverAddress)

                # Send message
                self.receiverId = i
                codeMessage = pickle.dumps(self)
                mySocket.send(codeMessage)
                mySocket.close()
            except Exception as e:
                print 'Error sending request to process: ', i,'Erro: ', e

class Process:
    def __init__(self, id):
        self.timeoutValue = 5
        self.id = id
        self.time = id
        self.alive = True
        self.leader = 'NotSet'
        self.timeoutArray = ['NotSet', 'NotSet', 'NotSet', 'NotSet', 'NotSet']
        self.electionTimeout = 'NotSet'

    def menu(self):
        print 'Menu\n-------------------------------------'
        print '1 - Try to make first election'
        print '2 - Kill this process'
        print '3 - Revive process'
        print '4 - Send general message'
        print '5 - Show leader PId'
        
        option = input()
        if (not self.alive and option != 3):
            print 'This process are dead, start it again to chose this option'
        else:
            if (option == 1):
                self.firstElection()
            elif (option == 2):
                self.killProcess()
            elif (option == 3):
                self.reviveProcess()
            elif (option == 4):
                self.sendGeneralMessage()
            elif (option == 5):
                self.showLeader()
            else:
                print 'Invalid option...'

    def firstElection(self):
        if (self.leader == 'NotSet'):
            self.startElection();
        else:
            print 'The first election already had happen'

    def killProcess(self):
        self.alive = False

    def reviveProcess(self):
        if (not self.alive):
            self.alive = True
            self.startElection()
        else:
            print 'This process is already alive'

    def sendGeneralMessage(self):
        message = Message(self.id, self.time, 'general', False, 'I am a general message')
        message.sendToAll()
        for i in range(0, 5):
            self.timeoutArray[i] = self.timeoutValue

    def showLeader(self):
        print 'My leader is the process: ', self.leader

    def receiveMessage(self, message):
        self.updateProcessTime(message)
        if (message.type == 'general'):
            if (message.ack and message.receiverId == self.id):
                self.stopProcessTimeout(message.senderId)
            elif (not message.ack):
                ackMessage = Message(self.id, self.time, 'general', True, 'Not important')
                ackMessage.sendToOne(message.senderId)
        elif (message.type == 'election'):
            if (message.ack and message.receiverId == self.id):
                self.stopElectionTimeout()
            elif (not message.ack):
                ackMessage = Message(self.id, self.time, 'election', True, 'Not important')
                ackMessage.sendToOne(message.senderId)
                self.startElection();
        elif (message.type == 'newLeader'):
            self.leader = message.senderId    
        else:
            print 'Invalid message type'

    def updateProcessTime(self, message):
        if self.time < message.time:
            self.time = message.time + 1
        else:
            self.time += 1

    def stopProcessTimeout(self, processId):
        self.timeoutArray[processId] = 'NotSet'

    def stopElectionTimeout(self):
        self.electionTimeout = 'NotSet'

    def startElection(self):
        message = Message(self.id, self.time, 'election', False, 'Not important')
        message.sendToGreater();
        self.electionTimeout = self.timeoutValue

    def turnIntoLeader(self):
        print 'Estou me tornando lider'
        message = Message(self.id, self.time, 'newLeader', False, 'Not important')
        message.sendToAll();

def processThread():
    print 'Starting process: ', sys.argv[2]
    while True:
        try:
            process.menu()
        except Exception as e:
            print 'Error in process: ', e

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
                    if (process.alive):
                        process.receiveMessage(message)
                except Exception as e:
                    print 'Error to receive message:', e
        except Exception as e:
            print 'Error to open socket:', e

def electionTimeoutThread():
    while True:
        if (isinstance(process.electionTimeout, int) and process.electionTimeout > 0):
            process.electionTimeout -= 1
            time.sleep(1)
        elif (process.electionTimeout == 0):
            process.electionTimeout = 'NotSet'
            process.turnIntoLeader() 

def processTimeoutThread(processId):
    while True:
        if (isinstance(process.timeoutArray[processId], int) and process.timeoutArray[processId] > 0):
            process.timeoutArray[processId] -= 1
            time.sleep(1)
        elif (process.timeoutArray[processId] == 0):
            process.timeoutArray[processId] = 'NotSet'
            process.startElection()

# Starting program
global process 
process = Process(int(sys.argv[2]))

def main():
    thread.start_new_thread(receiveThread, ())
    thread.start_new_thread(processThread, ())
    thread.start_new_thread(electionTimeoutThread, ())
    for i in range(0, 5):
        thread.start_new_thread(processTimeoutThread, (i,))
    signal.pause()

if __name__ == "__main__":
    sys.exit(main())