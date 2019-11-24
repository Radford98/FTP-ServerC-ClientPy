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
from time import sleep

"""
InitContact(): Creates a TCP socket connecting to the engr flip server from the first argument on provided port.
Pre: Port number for established connection. FlipX of server provided in command line.
Post: Returns socket connected to the server.
"""
def InitContact(port):
	# Connect to server
	serverName = sys.argv[1] + ".engr.oregonstate.edu"
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect((serverName, port))

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
	controlSocket.send(request.encode())
	#controlSocket.close()	# Close the socket now that we're done

"""
RecData(): Creates the data connection socket and receives data from the server.
Pre:
Post:
"""
def RecData(dataPort):
	# Create data socket to receive information; Sleep for a second to give server time to create socket
	sleep(1)
	dataSock = InitContact(dataPort)

	# Receive first line of information, which is all the information if an invalid command
	# was sent or the directory needs to be listed.
	data = dataSock.recv(1024).decode()

	# If the command was invalid, display the message from the server.
	if data.find("Invalid", 0, 10) != -1:	# This is a "minus one," not "dash l" for listing
		print(data)
	elif sys.argv[4] == "-l":
		print("Receiving directory structure from " + sys.argv[1] + ":" + sys.argv[3])
		print(data)
	clientSocket.close()


if __name__ == "__main__":
	# Validate commandline
	# Convert ports to ints
	serverPort = int(sys.argv[2])
	dataPort = int(sys.argv[3])

	# Validate commandline input
	if len(sys.argv) < 5 or (sys.argv[4] == "-g" and len(sys.argv) != 6) or len(sys.argv) > 6:
		sys.exit("USAGE: ./" + sys.argv[0] + " <flip num> <control port> <data port> -l/-g [text filename]")
	# Validate port numbers
	if serverPort < 1028 or serverPort > 65535 or dataPort < 1028 or dataPort > 65535:
		sys.exit("Please choose a valid port between 1028 and 65535.")
	# Validate command; This validation is removed so grader can see rejection message from the server, as
	# per the program specifications
	#if sys.argv[4] != "-l" and sys.argv[4] != "-g":
	#	sys.exit("USAGE: ./" + sys.argv[0] + " <flip num> <control port> <data port> -l/-g [text filename]")
	# Confirm asking for a .txt file
	if len(sys.argv) == 6 and ".txt" not in sys.argv[5]:
		sys.exit("USAGE: ./" + sys.argv[0] + " <flip num> <control port> <data port> -l/-g [text filename]")


	# Set up socket
	clientSocket = InitContact(serverPort)

	# Make a request from the server
	MakeRequest(clientSocket)

	# Receive requested data
	RecData(dataPort)


