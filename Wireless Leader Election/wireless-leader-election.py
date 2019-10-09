
#coding: utf-8
########################################################
# 		      	WIRELES LEADER ELECTION                  #
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
    def __init__(self, senderId, time, type, electionId, electionSource, newLeaderId):
        self.senderId = senderId
        self.time = time
        self.type = type
        self.electionId
        self.electionSource = electionSource
        self.newLeaderId = newLeaderId

    def sendElectionMessage(self, neighbors, fatherPId):
        for i in range (0, int(len(neighbors))):
            if neighbors[i].pId != fatherPId:
                self.receiverId = neighbors[i].pId
                try:
                    # Open socket
                    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    serverAddress = ('localhost', 9000 + self.receiverId)
                    mySocket.connect(serverAddress)

                    # Send message
                    codeMessage = pickle.dumps(self)
                    mySocket.send(codeMessage)
                    mySocket.close()
                except Exception as e:
                    print 'Error sending request to process: ', self.receiverId,'Erro: ', e

    def sendAck(self, receiverId):
        self.receiverId = receiverId
        try:
            # Open socket
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverAddress = ('localhost', 9000 + self.receiverId)
            mySocket.connect(serverAddress)

            # Send message
            codeMessage = pickle.dumps(self)
            mySocket.send(codeMessage)
            mySocket.close()
        except Exception as e:
            print 'Error sending request to process: ', self.receiverId,'Erro: ', e

    def sendElectionResponse (self, fatherId):
        self.receiverId = fatherId
        try:
            # Open socket
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverAddress = ('localhost', 9000 + self.receiverId)
            mySocket.connect(serverAddress)

            # Send message
            codeMessage = pickle.dumps(self)
            mySocket.send(codeMessage)
            mySocket.close()
        except Exception as e:
            print 'Error sending request to process: ', self.receiverId,'Erro: ', e

    def sendNewLeaderMessage ():
        for i in range (0, 10)
            self.receiverId = i
            try:
                # Open socket
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverAddress = ('localhost', 9000 + self.receiverId)
                mySocket.connect(serverAddress)

                # Send message
                codeMessage = pickle.dumps(self)
                mySocket.send(codeMessage)
                mySocket.close()
            except Exception as e:
                print 'Error sending request to process: ', self.receiverId,'Erro: ', e

class Neighbor:
    def __init__(self, pId, capacity):
        self.pId = pId
        self.capacity = capacity

class Response:
    def __init__(self, pId, responseType, response, capacity):
        self.pId = pId
        self.responseType = responseType
        self.response = response
        self.capacity = capacity

class Process:
    def __init__(self, id):
        self.id = id
        self.time = id
        self.leader = False
        self.fatherId = False
        self.electionId = False
        # Construc topology
        if (id == 1):
            self.capacity = 30
            self.neighbors[0] = Neighbor(2, 50)
            self.neighbors[1] = Neighbor(3, 20)
            self.neighbors[2] = Neighbor(5, 90)
        elif (id == 2):
            self.capacity = 50            
            self.neighbors[0] = Neighbor(1, 30)
            self.neighbors[1] = Neighbor(3, 20)
            self.neighbors[2] = Neighbor(4, 80)
            self.neighbors[3] = Neighbor(5, 90)
        elif (id == 3):
            self.capacity = 20
            self.neighbors[0] = Neighbor(1, 30)
            self.neighbors[1] = Neighbor(2, 50)
            self.neighbors[2] = Neighbor(7, 82)
            self.neighbors[3] = Neighbor(8, 32)
        elif (id == 4):
            self.capacity = 80
            self.neighbors[0] = Neighbor(2, 50)
            self.neighbors[1] = Neighbor(6, 45)
        elif (id == 5):
            self.capacity = 90
            self.neighbors[0] = Neighbor(1, 30)
            self.neighbors[1] = Neighbor(2, 50)
            self.neighbors[2] = Neighbor(6, 45)
            self.neighbors[3] = Neighbor(9, 67)
        elif (id == 6):
            self.capacity = 45
            self.neighbors[0] = Neighbor(4, 80)
            self.neighbors[1] = Neighbor(5, 90)
            self.neighbors[2] = Neighbor(8, 32)
            self.neighbors[3] = Neighbor(9, 67)
        elif (id == 7):
            self.capacity = 82
            self.neighbors[0] = Neighbor(3, 20)
            self.neighbors[1] = Neighbor(10, 9)
        elif (id == 8):
            self.capacity = 32
            self.neighbors[0] = Neighbor(3, 20)
            self.neighbors[1] = Neighbor(6, 45)
            self.neighbors[2] = Neighbor(9, 67)
            self.neighbors[3] = Neighbor(10, 9)
        elif (id == 9):
            self.capacity = 67
            self.neighbors[0] = Neighbor(5, 90)
            self.neighbors[1] = Neighbor(6, 45)
            self.neighbors[2] = Neighbor(8, 32)
            self.neighbors[3] = Neighbor(10, 9)
        elif (id == 10):
            self.capacity = 9
            self.neighbors[0] = Neighbor(7, 82)
            self.neighbors[1] = Neighbor(8, 32)
            self.neighbors[2] = Neighbor(9, 67)
        else:
            print 'Invalid Process ID'
            sys.exit()

    def menu(self):
        print 'Menu\n-------------------------------------'
        print '1 - Start Election'
        print '2 - Show leader PId'
        
        option = input()
        if (not self.alive and option != 3):
            print 'This process are dead, start it again to chose this option'
        else:
            if (option == 1):
                self.startElection()
            elif (option == 2):
                self.showLeader()
            else:
                print 'Invalid option...'

    def startElection(self):
        if (self.election == False):
            electionMessage = Message(self.id, self.time, 'election', self.id)
            electionMessage.sendElectionMessage(self.neighbors, self.id)
        else:
            print 'I\'m already in a election so can\'t start another one'

    def showLeader(self):
        print 'My leader is the process: ', self.leader

    def receiveMessage(self, message):
        self.updateProcessTime(message)
        if (message.type == 'eletction'):
            self.receiveElectionMessage(message)
        elif (message.type == 'electionRespone'):
            self.receiveElectionResponse(message)
        elif (message.type == 'ack'):
            self.receiveAck(message)
        elif (message.type == 'newLeader'):
            self.receiveNewLeaderMessage(message)
        else:
            print 'Invalid message type'

    def updateProcessTime(self, message):
        if self.time < message.time:
            self.time = message.time + 1
        else:
            self.time += 1

    def receiveElectionMessage(self, message):
        changedElection = self.setHighestIdElection(message.electionId)
        changedFather = self.setFatherIfDontHaveOne(message.senderId)
        # change and start an election are the same thing
        if (changedElection):
            self.initResponseWaitVector()
            electionMessage = Message(self.id, self.time, 'election', self.fatherId)
            electionMessage.sendElectionMessage(self.neighbors, self.fatherId)
        else:
            ackMessage = Message(self.id, self.time, 'ack', self.electionId)
            ackMessage.sendAck(message.senderId)

    def initResponseWaitVector(self):
        for i in range(0, int(len(self.neighbors))):
            if (neighbors.pId != self.fatherId):
                self.responseWaitVector[i] = Response(neighbors[i].pId, False, False, False)
            else:
                self.responseWaitVector[i] = Response(neighbors[i].pId, 'father', False, False)

    def setHighestIdElection(self, newElectoinId):
        if (not self.electionId or newElectoinId > self.electionId):
            self.electionId = newElectoinId
            self.fatherId = False
            return newElectoinId
        else:
            return False

    def setFatherIfDontHaveOne(self, fahterId):
        if (not self.fatherId):
            self.fatherId = fatherId
            return fatherId
        else:
            return False

    def receiveElectionResponse(self, message):
        if (message.electionId == self.electionId):
            for i in range(0 int(len(self.responseWaitVector))):
                if (self.responseWaitVector[i].pId == message.senderId):
                    self.responseWaitVector[i].responseType = message.type
                    self.responseWaitVector[i].response = message.response
                    self.responseWaitVector[i].capacity = message.capacity
            if (self.receiveAllResponses()):
                self.electLeader(message)

    def receiveAck(self, message):
        if (message.electionId == self.electionId):
            for i in range(0, int(len(self.responseWaitVector))):
                if (self.responseWaitVector[i].pId == message.senderId):
                    self.responseWaitVector[i].responseType = message.type
                    self.responseWaitVector[i].response = message.response
                    self.responseWaitVector[i].capacity = message.capacity
            if (self.receiveAllResponses()):
                self.electLeader(message)

    def receiveAllResponses(self):
        receiveAllResponses = True
        for i in range(0, int(len(self.responseWaitVector))):
            if (not self.responseWaitVector.response):
                receiveAllResponses = False
        return receiveAllResponses
    
    def electLeader(self, message):
        bestLeaderId = self.getBestLeader()
        if (message.electionSource == self.id):
            newLeaderMessage = Message(self.id, self.time, 'newLeader', self.electionId, self.id, bestLeaderId)
            newLeaderMessage.sendNewLeaderMessage()
        else:
            responseElectionMessage = Message(self.id, self.time, 'electionResponse', self.eletionId, message.electionSource, bestLeaderId)
            responseElectionMessage.sendElectionResponse(self.fatherId)

    def getBestLeader():
        bestLeader = self.id
        bestCapacity = self.capacity
        for i in range(0, int(len(self.responseWaitVector))):
            if (self.responseWaitVector[i].capacity > bestCapacity):
                bestLeader = self.responseWaitVector[i].pId
                bestCapacity = self.responseWaitVector[i].capacity
        return bestLeader

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

# Starting program
global process 
process = Process(int(sys.argv[2]))

def main():
    thread.start_new_thread(receiveThread, ())
    thread.start_new_thread(processThread, ())

if __name__ == "__main__":
    sys.exit(main())