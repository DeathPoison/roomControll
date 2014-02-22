#!/usr/bin/env python

import socket
import sys

import argparse  # argument is key and option is --key...

def isOpen(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False

if __name__ == "__main__":
    try:
        serverIP = '192.168.0.111'
        serverPORT = 10000

        tryConnect = False

        parser = argparse.ArgumentParser()
        parser.add_argument('action', help="actions are: start, status, startBoard, startMenu, stop")
        args = parser.parse_args()

        #if isOpen(serverIP, serverPORT):
            
        tryConnect = True

        print 'start'
        print args.action

        
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port on the server given by the caller
        server_address = (serverIP, serverPORT)
        #print >>sys.stderr, 'connecting to %s port %s' % server_address
        print 'connecting to %s port %s' % server_address
        sock.connect(server_address)

        try:
            message = str(args.action)
            print >>sys.stderr, 'sending "%s"' % message
            sock.sendall(message)

            print 'miao!'
            print str(args.action)
                #amount_received = 0
                #amount_expected = len(message)
                #while amount_received < amount_expected:
                #    data = sock.recv(16)
                #    amount_received += len(data)
                #    print >>sys.stderr, 'received "%s"' % data


    finally:
        #if tryConnect:
        #    sock.close()
        quit()
