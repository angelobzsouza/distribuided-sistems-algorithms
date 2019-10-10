
#coding: utf-8
########################################################
# 		      	WIRELES LEADER ELECTION                #
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
    def __init__(self, senderId, time, type, electionId, electionSource, newLeaderId, capacity):
        self.senderId = senderId
        self.time = time
        self.type = type
        self.electionId = electionId
        self.electionSource = electionSource
        self.newLeaderId = newLeaderId
        self.capacity = capacity

    def sendToNeighbors(self, neighbors, fatherId, receiverId = False):
        for i in range (0, int(len(neighbors))):
            if (neighbors[i]):
                if neighbors[i].pId != fatherId:
                    if (receiverId):
                        self.receiverId = receiverId
                    else:
                        self.receiverId = neighbors[i].pId
                    try:
                        # Open socket
                        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        serverAddress = ('localhost', 9000 + neighbors[i].pId)
                        mySocket.connect(serverAddress)

                        # Send message
                        codeMessage = pickle.dumps(self)
                        mySocket.send(codeMessage)
                        mySocket.close()
                    except Exception as e:
                        print 'Error sending message to process: ', neighbors[i].pId,'Erro: ', e
    
    def sendToFather(self, fatherId):
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
            print 'Error sending new leader message to process: ', self.receiverId,'Erro: ', e

class Neighbor:
    def __init__(self, pId, capacity):
        self.pId = pId
        self.capacity = capacity

class Response:
    def __init__(self, pId, responseType, response, capacity, processWithBestCapacity):
        self.pId = pId
        self.responseType = responseType
        self.response = response
        self.capacity = capacity

class Process:
    def __init__(self, id):
        self.id = id
        self.time = id
        self.leaderId = False
        self.fatherId = False
        self.electionId = False
        self.neighbors = [False, False, False, False]
        self.responseWaitVector = [False, False, False, False]

        # Construc topology
        if (self.id == 1):
            self.capacity = 30
            self.neighbors[0] = Neighbor(2, 50)
            self.neighbors[1] = Neighbor(3, 20)
            self.neighbors[2] = Neighbor(5, 90)
        elif (self.id == 2):
            self.capacity = 50            
            self.neighbors[0] = Neighbor(1, 30)
            self.neighbors[1] = Neighbor(3, 20)
            self.neighbors[2] = Neighbor(4, 80)
            self.neighbors[3] = Neighbor(5, 90)
        elif (self.id == 3):
            self.capacity = 20
            self.neighbors[0] = Neighbor(1, 30)
            self.neighbors[1] = Neighbor(2, 50)
            self.neighbors[2] = Neighbor(7, 82)
            self.neighbors[3] = Neighbor(8, 32)
        elif (self.id == 4):
            self.capacity = 80
            self.neighbors[0] = Neighbor(2, 50)
            self.neighbors[1] = Neighbor(6, 45)
        elif (self.id == 5):
            self.capacity = 90
            self.neighbors[0] = Neighbor(1, 30)
            self.neighbors[1] = Neighbor(2, 50)
            self.neighbors[2] = Neighbor(6, 45)
            self.neighbors[3] = Neighbor(9, 67)
        elif (self.id == 6):
            self.capacity = 45
            self.neighbors[0] = Neighbor(4, 80)
            self.neighbors[1] = Neighbor(5, 90)
            self.neighbors[2] = Neighbor(8, 32)
            self.neighbors[3] = Neighbor(9, 67)
        elif (self.id == 7):
            self.capacity = 82
            self.neighbors[0] = Neighbor(3, 20)
            self.neighbors[1] = Neighbor(10, 9)
        elif (self.id == 8):
            self.capacity = 32
            self.neighbors[0] = Neighbor(3, 20)
            self.neighbors[1] = Neighbor(6, 45)
            self.neighbors[2] = Neighbor(9, 67)
            self.neighbors[3] = Neighbor(10, 9)
        elif (self.id == 9):
            self.capacity = 67
            self.neighbors[0] = Neighbor(5, 90)
            self.neighbors[1] = Neighbor(6, 45)
            self.neighbors[2] = Neighbor(8, 32)
            self.neighbors[3] = Neighbor(10, 9)
        elif (self.id == 10):
            self.capacity = 9
            self.neighbors[0] = Neighbor(7, 82)
            self.neighbors[1] = Neighbor(8, 32)
            self.neighbors[2] = Neighbor(9, 67)
        else:
            print 'Invalid Process ID'

    def menu(self):
        print 'Menu\n-------------------------------------'
        print '1 - Start Election'
        print '2 - Show leader PId'
        print '3 - Show father PId'
        print '4 - Show Election Id'
        print '5 - Show Neighbors'
        print '6 - Show Wait Vector'
        
        option = input()
        if (option == 1):
            self.startElection()
        elif (option == 2):
            self.showLeader()            
        elif (option == 3):
            self.showFather()
        elif (option == 4):
            self.showElection()
        elif (option == 5):
            self.showNeighbors()
        elif (option == 6):
            self.showWaitVector()
        else:
            print 'Invalid option...'
    
    def showFather(self):
        print 'My father is ', self.fatherId

    def showElection(self):
        print 'My election is ', self.electionId

    def showNeighbors(self):
        print 'My neighbors vector is:'
        for i in range (0, int(len(self.neighbors))):
            if (self.neighbors[i]):
                print i, ' - ID: ', self.neighbors[i].pId, ' CAP: ', self.neighbors[i].capacity
            else:
                print i, ' ', self.neighbors[i]

    def showWaitVector(self):
        print 'My response wait vector is:'
        for i in range (0, int(len(self.responseWaitVector))):
            if (self.responseWaitVector[i]):
                print i, ' - ID: ', self.responseWaitVector[i].pId, ' ResTYPE: ', self.responseWaitVector[i].responseType, ' RESP:', self.responseWaitVector[i].response, ' CAP: ', self.responseWaitVector[i].capacity
            else:
                print i, ' ', self.responseWaitVector[i]

    def startElection(self):
        if (self.electionId == False):
            self.electionId = self.id
            self.initResponseWaitVector()
            electionMessage = Message(self.id, self.time, 'election', self.electionId, self.id, False, False)
            electionMessage.sendToNeighbors(self.neighbors, False, False)
        else:
            print 'I\'m already in a election so can\'t start another one'

    def showLeader(self):
        if (not self.leaderId):
            print 'The leader dosn\'t have been elected yet'
        else:
            print 'My leader is the process: ', self.leaderId

    def receiveMessage(self, message):
        if (message.receiverId == self.id and message.senderId != self.id):
            # print 'Receiving ', message.type,' message from process ', message.senderId
            self.updateProcessTime(message)
            if (message.type == 'election'):
                self.receiveElectionMessage(message)
            elif (message.type == 'electionResponse'):
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
            electionMessage = Message(self.id, self.time, 'election', message.electionId, message.electionSource, False, False)
            electionMessage.sendToNeighbors(self.neighbors, self.fatherId, False)
        else:
            ackMessage = Message(self.id, self.time, 'ack', self.electionId, message.electionSource, False, False)
            ackMessage.sendToNeighbors(self.neighbors, False, message.senderId)

    def initResponseWaitVector(self):
        for i in range(0, int(len(self.neighbors))):
            if (self.neighbors[i]):
                if (self.neighbors[i].pId != self.fatherId):
                    self.responseWaitVector[i] = Response(self.neighbors[i].pId, False, False, False, False)
                else:
                    self.responseWaitVector[i] = Response(self.neighbors[i].pId, 'father', False, False, False)

    def setHighestIdElection(self, newElectoinId):
        if (not self.electionId or newElectoinId > self.electionId):
            self.electionId = newElectoinId
            self.fatherId = False
            return newElectoinId
        else:
            return False

    def setFatherIfDontHaveOne(self, fatherId):
        if (not self.fatherId):
            self.fatherId = fatherId
            return fatherId
        else:
            return False

    def receiveElectionResponse(self, message):
        if (message.electionId == self.electionId):
            for i in range(0, int(len(self.responseWaitVector))):
                if (self.responseWaitVector[i] and self.responseWaitVector[i].pId == message.senderId):
                    self.responseWaitVector[i].responseType = message.type
                    self.responseWaitVector[i].response = True
                    self.responseWaitVector[i].capacity = message.capacity
                    self.responseWaitVector[i].processWithBestCapacity = message.newLeaderId
            if (self.receiveAllResponses()):
                self.electLeader(message)

    def receiveAck(self, message):
        if (message.electionId == self.electionId):
            for i in range(0, int(len(self.responseWaitVector))):
                if (self.responseWaitVector[i] and self.responseWaitVector[i].pId == message.senderId):
                    self.responseWaitVector[i].responseType = message.type
                    self.responseWaitVector[i].response = True
                    self.responseWaitVector[i].capacity = False
            if (self.receiveAllResponses()):
                self.electLeader(message)
            
    def receiveAllResponses(self):
        receiveAllResponses = True
        for i in range(0, int(len(self.responseWaitVector))):
            if (self.responseWaitVector[i] and self.responseWaitVector[i].responseType != 'father' and not self.responseWaitVector[i].response):
                receiveAllResponses = False
        return receiveAllResponses
    
    def electLeader(self, message):
        [bestLeaderId, bestLeaderCapacity] = self.getBestLeader()
        if (message.electionSource == self.id):
            self.leaderId = bestLeaderId
            self.election = False
            self.fatherId = False
            newLeaderMessage = Message(self.id, self.time, 'newLeader', self.electionId, self.id, bestLeaderId, False)
            newLeaderMessage.sendToNeighbors(self.neighbors, False, False)
        else:
            responseElectionMessage = Message(self.id, self.time, 'electionResponse', self.electionId, message.electionSource, bestLeaderId, bestLeaderCapacity)
            if (self.fatherId):
                responseElectionMessage.sendToFather(self.fatherId)

    def getBestLeader(self):
        bestLeader = self.id
        bestCapacity = self.capacity
        for i in range(0, int(len(self.responseWaitVector))):
            if (self.responseWaitVector[i] and self.responseWaitVector[i].responseType != 'father' and self.responseWaitVector[i].capacity > bestCapacity):
                bestLeader = self.responseWaitVector[i].processWithBestCapacity
                bestCapacity = self.responseWaitVector[i].capacity
        return [bestLeader, bestCapacity]

    def receiveNewLeaderMessage(self, message):
        self.leaderId = message.newLeaderId
        self.election = False
        self.fatherId = False
        message.sendToNeighbors(self.neighbors, False, False)

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