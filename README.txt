Author: Brad Powell
Programs: Project 2
Description: An ftp server/client combination for transfering text files.
Course: CS 372-400 Computer Networks

-- Server Instructions
Run 'make' to run the makefile to compile the server.
If a time skew error occurs, run "gcc -o server ftserver.c"
Start the server with "server <control portnum>" and make a note of which flip the server is on.
	e.g. "server 65432"

-- Client Instructions
Client was created with Python. To start server, run
	"python3 ftclient.py flip<num> <control portnum> <data portnum> <-l/-g> [filename]"
	e.g. "python3 ftclient.py flip2 65432 54321 -l"

Client will close after a single connection, but the server keeps running. Recommend changing the data portnum
with each request incase the socket hasn't been completely released yet. Server is only closed with CTRL+C.

If the file to be transferred already exists, the client has the option to overwrite or not. If not, a new
file will be created called <filename>2.txt to store the transferred data.

Tested to make sure it works both on different servers and from different folders.
