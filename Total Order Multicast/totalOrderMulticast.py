#coding: utf-8
########################################################
# 		    	       	TOTAL ORDER MULTICAS            	 #
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

class Package:
    def __init__(self, id, type, time, data):
        self.id = id
        self.type = type
        self.time = time
        self.data = data
        self.acks = 0

    def getTime(self):
        return self.time

class Process:
    def __init__(self, id):
        self.id = id
        self.time = 0
        self.packageQueue = []
        self.ackQueue = []
        self.appPackages = [] #Used just too see which packages was sent to app

    def sendPackageToApp(self):
        if int(len(self.packageQueue)) > 0:
            if self.packageQueue[0].acks == 4:
                self.appPackages.append(self.packageQueue[0])
                del self.packageQueue[0]
                self.showAppQueue()

    def sendPackage(self, type, data):
        self.time += 1 
        packageId = str(self.time)+str(self.id)
        package = Package(packageId, type,  self.time, data)

		# Send package to the four open process
        for i in range(0, 4):
            try:
                # Open socket
                mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serverAddress = ('localhost', 9000 + i)
                mySocket.connect(serverAddress)

                # Send package
                codeMessage = pickle.dumps(package)
                mySocket.send(codeMessage)
                mySocket.close()
            except Exception as e:
                print 'Error sending package to process: ', i,'Erro: ', e
            if type == 'data':
                time.sleep(random.randint(0, 5)) #Used to make acks arrived before package in some cases

    def receivePackage(self, package):
        if package.type == 'data':
            self.sendPackage('ack', package.id)
            self.updateProcessTime(package)
            self.addReceivedAcks(package)
            self.updatePackageQueue(package)
            self.showUpdatedQueue()

        elif package.type == 'ack':
            print '\nReceiving ack of package: ', package.data
            self.updateAcks(package)

        else:
            print 'Error receiving message: invalid type of message'

        self.sendPackageToApp()

    def updateProcessTime(self, package):
        if self.time < package.time:
            self.time = package.time

    def addReceivedAcks(self, package):
        package.acks += sum(ack.data == package.id for ack in self.ackQueue)

        remainingAcks = sum(ack.data == package.id for ack in self.ackQueue)
        while remainingAcks > 0:
            for i in range(0, int(len(self.ackQueue))):
                if self.ackQueue[i].data == package.id:
                    del self.ackQueue[i]
                    break
            remainingAcks = sum(ack.data == package.id for ack in self.ackQueue)
   
    def updatePackageQueue(self, package):
        self.packageQueue.append(package);
        self.packageQueue = sorted(self.packageQueue, key = Package.getTime)

    def showUpdatedQueue(self):
        print '\n\n\nUPDATED QUEUE:'
        for i in range(0, int(len(self.packageQueue))):
            print '------------------------------------------'
            print 'Package Id:', self.packageQueue[i].id
            print 'Package Type:', self.packageQueue[i].type
            print 'Package Time:', self.packageQueue[i].time
            print 'Package Data:', self.packageQueue[i].data
            print '------------------------------------------\n'      

    def showAppQueue(self):
        print '\n\n\nAPP PACKAGES:'
        for i in range(0, int(len(self.appPackages))):
            print '------------------------------------------'
            print 'Package Id:', self.appPackages[i].id
            print 'Package Type:', self.appPackages[i].type
            print 'Package Time:', self.appPackages[i].time
            print 'Package Data:', self.appPackages[i].data
            print '------------------------------------------\n'

    def updateAcks(self, package):
        findMessage = False
        for i in range(0, int(len(self.packageQueue))):
            if self.packageQueue[i].id == package.data:
                findMessage = True
                self.packageQueue[i].acks += 1

        if not findMessage:
            self.ackQueue.append(package)

def processThread():
    print 'Starting process: ', sys.argv[2]

    while True:
        try:
            data = raw_input("At any time, type a little string to send and press \"enter\": ")
            process.sendPackage('data', data)
        except Exception as e:
            print 'Error to send package: ', e

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
                    package = pickle.loads(data)
                    process.receivePackage(package)
                except Exception as e:
                    print 'Error to receive package:', e
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