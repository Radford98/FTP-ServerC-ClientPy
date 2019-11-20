"""
Author: Brad Powell
Program: ftclient.py
Description: A client designed to connect with ftserver.c. It can either send "-l" for directory contents or
"-g <filename>" to get a .txt file. In either case it sends a port number along to open a data stream.
Course: CS 372-400 Computer Networks
Last Modified: 11/19/2019
Citations:
	Basic structure of how to set up a Python client from Computer Networking by Kurose and Ross.

"""

import socket	# Access socket API
import sys	# Access command line arguments

"""
InitContact(): Creates a TCP socket connecting to the engr flip in the first argument on the port in the second
argument. It first validates all of the command line parameter.
Pre: Program ran with command-line arguments: <flip num> <control port> <data port> -l/-g [text filename]
Post: Returns socket connected to the server.
"""
def InitContact():
	# Convert ports to ints (dataPort only for validation in this function)
	serverPort = int(sys.argv[2])
	dataPort = int(sys.argv[3])

	# Validate commandline input
	if len(sys.argv) < 5 or (sys.argv[4] == "-g" and len(sys.argv) != 6) or len(sys.argv) > 6:
		sys.exit("USAGE: ./" + sys.argv[0] + " <flip num> <control port> <data port> -l/-g [text filename]")
	# Validate port numbers
	if serverPort < 1028 or serverPort > 65535 or dataPort < 1028 or dataPort > 65535:
		sys.exit("Please choose a valid port between 1028 and 65535.")
	# Validate command
	if sys.argv[4] != "-l" and sys.argv[4] != "-g":
		sys.exit("USAGE: ./" + sys.argv[0] + " <flip num> <control port> <data port> -l/-g [text filename]")
	# Confirm asking for a .txt file
	if len(sys.argv) == 6 and ".txt" not in sys.argv[5]:
		sys.exit("USAGE: ./" + sys.argv[0] + " <flip num> <control port> <data port> -l/-g [text filename]")

	# Connect to server
	serverName = sys.argv[1] + ".engr.oregonstate.edu"
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect((serverName, serverPort))

	return clientSocket

"""
MakeRequest(controlSocket): Constructs a string from the command line arguments and sends the encoded request
to the server.
Pre: Socket connected to ftserver.c
Post: Request sent to server.
"""
def MakeRequest(controlSocket):
	# Send request
	request = sys.argv[3] + " " + " " + sys.argv[4]
	if sys.argv[4] == "-g":
		request += " " + sys.argv[5]
	print(request)
	controlSocket.send(request.encode())
	#controlSocket.close()	# Close the socket now that we're done

"""
RecData(): Creates the data connection socket and receives data from the server.
Pre:
Post:
"""
def RecData(clientSocket):
	##### Create data socket #####
	data = clientSocket.recv(1024)
	if sys.argv[4] == "-l":
		print("Receiving directory structure from " + sys.argv[1] + ":" + sys.argv[3])
		print(data.decode())
	clientSocket.close()


if __name__ == "__main__":
	# Set up socket
	clientSocket = InitContact()

	# Make a request from the server
	MakeRequest(clientSocket)

	# Receive requested data
	RecData(clientSocket)


