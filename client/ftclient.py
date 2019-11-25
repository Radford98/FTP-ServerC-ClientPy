"""
Author: Brad Powell
Program: ftclient.py
Description: A client designed to connect with ftserver.c. It can either send "-l" for directory contents or
"-g <filename>" to get a .txt file. In either case it sends a port number along to open a data stream.
Course: CS 372-400 Computer Networks
Last Modified: 11/19/2019
Citations:
	Basic structure of how to set up a Python client from Computer Networking by Kurose and Ross.
	Finding a substring
		https://www.programiz.com/python-programming/methods/string/find
	How to check if a file already exists:
		https://linuxize.com/post/python-check-if-file-exists/
		https://docs.python.org/3/library/os.path.html#os.path.isfile
	I figured out the code myself to handle receiving split characters (see recData function), but the
	following github clued me in that UTF-8 wasn't encoded in single bytes (by saying latin-1 is)
	and wikipedia informed me that UTF-8 encodes in 1-4 bytes.
		https://github.com/google/seq2seq/issues/153
		https://en.wikipedia.org/wiki/UTF-8
"""

import socket	# Access socket API
import sys	# Access command line arguments
from time import sleep
from os import path

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
	request = sys.argv[3] + " " + sys.argv[4]
	if sys.argv[4] == "-g":
		request += " " + sys.argv[5]
				
	controlSocket.send(request.encode())

	# Wait for a moment to see if an error message is returned from the server.
	# If it timesout, it was successful and close the socket. Otherwise exit and display error message.
	controlSocket.settimeout(1)
	try:
		err = controlSocket.recv(1024).decode()
	except:
		pass
	else:
		controlSocket.close()
		sys.exit(err)

"""
RecData(): Creates the data connection socket and receives data from the server.
Pre:
Post:
"""
def RecData(controlSocket, dataPort):
	serverName = sys.argv[1] + ":" + sys.argv[3]

	# Create data socket to receive information
	dataSock = InitContact(dataPort)

	# First check for an invalid message on the control connection. If none come through, get
	# data from the data connection.
	controlSocket.settimeout(1)
	try:
		data = controlSocket.recv(1024).decode()
	except:
		pass
	if len(data) == 0:
		data = dataSock.recv(1024).decode()

	# If the file name was invalid, display the message from the server.
	if data.find("Invalid", 0, 10) != -1:	# This is a "minus one," not "dash l" for listing
		print(data)
	elif sys.argv[4] == "-l":
		print("Receiving directory structure from " + serverName)
		print(data)
	elif sys.argv[4] == "-g":
		# Check if the file already exists. Create a new file if not
		recFile = sys.argv[5]
		if path.isfile(recFile):
			res = input("Overwrite file \"" + recFile + "\"? (y/n)")
			if res == "y":
				print("Receiving \"" + recFile + "\" from " + serverName)
			else:
				# Create a newly named file
				txtIndex = recFile.find(".")
				recFile = recFile[:txtIndex] + "2.txt"
				print("Writing \"" + recFile + ".\"")

		# Open file for writing
		with open (recFile, 'w') as wFile:
			"""
			Since decode() uses UTF-8, which can use anywhere between 1 and 4 bytes, it is possible
			a character might be sent incomplete (C doesn't care, it's just sending bytes).
			When this happens decode() will throw an exception and the program will store that chunk
			of data and blank out the data variable. Next time around that chunk will be added back
			in to the data to be decoded, potentially being stashed again if the next chunk has a split
			character. Once a chunk of data is decode()d successfully, it will write to the file
			at the top of the loop.
			"""
			incomplete = bytearray()			# Create empty bytearray
			while(data.find("@@EOF@@") == -1):		# Loop until terminator is found
				wFile.write(data)			# Write data to file (already decoded)
				data = dataSock.recv(1024)		# Retrieve data from socket
				if len(incomplete) != 0:		# If there is a saved chunk of data
					data = incomplete + data	# Combine the data
					incomplete = bytearray()	# Reset incomplete to empty bytearray
				try:
					data = data.decode()		# Try to decode the data
				except:
					incomplete += data		# If a char was incomplete, store the data
					data = ""			# Empty data (so nothing is written)
			# Once the terminator is found, the last string of data still needs to be written to the
			# file. data[:XX] slices off everything from the index XX and later. find() returns the index
			# of the terminator. Combined, data[:data.find("@@EOF@@")] removes the terminator.
			wFile.write(data[:data.find("@@EOF@@")])
		print("File transfer complete.")
	# Close the sockets
	controlSocket.close()
	dataSock.close()

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
	RecData(clientSocket, dataPort)


