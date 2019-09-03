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

class Process:
    def __init__(self, id):
        self.id = id

# Trhead to send packages
def processThread():
    print 'Starting process: ', sys.argv[2]

    while True:
        try:
            raw_input("If you want to send a message press \"enter\" ?")
            process.sendPackage('data', 'some data')
        except Exception as e:
            print 'Error to send package: ', e

# Thread to receive packages
def receiveThread():
    while True:
        serverPort = int(sys.argv[1])
        serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            serverSocket.bind(('',serverPort))
            serverSocket.listen(1)
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
    thread.start_new_thread(processThread, ())
    thread.start_new_thread(receiveThread, ())
    signal.pause()

if __name__ == "__main__":
    sys.exit(main())