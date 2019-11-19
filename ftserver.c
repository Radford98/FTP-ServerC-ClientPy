/* Author: Brad Powell
 * Program: ftserver.c
 * Description: An ftp server for transferring text files with ftclient. It waits on the port specified in
 * the command line for a request from ftclient and will either display the current directory or send
 * the requested file.
 * Course: CS 372-400 Computer Networks
 * Last Modified: 11/14/2019
 * Citations:
 * 	Basic framework (setting up socket, how the send and recv commands work, etc.) based on material from cs344
 * 	Beej's guide (http://beej.us/guide/bgnet/) was used as a reference.
 * 		Particularly: getpeername and getnameinfo to report name of connecting client.
 * 	Info on how to use fread to read the contents of an entire file:
 * 		https://stackoverflow.com/questions/14002954/c-programming-how-to-read-the-whole-file-contents-into-a-buffer
 *
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

/* Error(const char* msg): Combines perror with exit(0) for error reporting. Saves on typing exit(0) multiple times.
 * Pre: Error message.
 * Post: Program closed.
 */
void Error(const char *msg) {
	perror(msg);
	exit(0);
}

/* Startup(int port): Creates and sets up a TCP socket on the port number. Begins listening and returns the socket.
 * Pre: Port in int form.
 * Post: Created and listening socket. Returns listening socket file descriptor.
 */
int Startup(int port) {
	int listenSocket;
	struct sockaddr_in serverAddress;

	// Set up the server address struct
	memset((char *)&serverAddress, '\0', sizeof(serverAddress));	// Clear address struct
	serverAddress.sin_family = AF_INET;				// Create socket for network
	serverAddress.sin_port = htons(port);				// Convert port number
	serverAddress.sin_addr.s_addr = INADDR_ANY;			// Allow any address

	// Set up socket
	listSocket = socket(AF_INET, SOCK_STREAM, 0);			// Create TCP socket
	if (listenSocket < 0) {
		Error("ERROR creating socket.");
	}

	// Bind socket with port and begin listening
	if (bind(listenSocket, (struct sockaddr *)&serverAddress, sizeof(serverAddress)) < 0) {
		Error("ERROR binding socket.");
	}
	listen(listenSocket, 5);	// Only needs to accept 1 connection, but set up a backlog of up to 5.

	return listenSocket;

}

/* HandleRequest(estSock): Handles a request sent by the client on the established connection passed it.
 * Will either list directory contents with '-l' or send a file with '-g <filename>'.
 * Pre: A TCP socket already established with a client.
 * Post: Returns -1 if there was an error, or 1 if appropriate information wass sent to the client.
 */
int HandleRequest(int estSock) {
	int chRead, i, dataPort;
	char buffer[256], *token, command[3][50];


	// Receive the command with the client.
	memset(buffer, '\0', 256);
	chRead = recv(estSock, buffer, 255, 0);		// Read command, leaving '\0' at end
	if (chRead < 0) {
		Error("ERROR reading socket.");
	}

	// Break the command into its individual parts
	i = 0;
	while (token = strsep(&buffer, " ")) {		// Store pieces (space as delim) in token
		if (i >= 3){				// Confirm only up to 3 commands are sent (eg "2031 -g file")
			send(estSock, "Invalid command. USAGE: <port> -l/-g [file]", 43, 0);
			return -1;
		}
		strcpy(command[i], token);		// Copy token into array
		i++;					// Increment index
	}

	// Validate port number
	dataPort = atoi(command[0]);
	if (dataPort < 1028 || dataPort > 65535) {
		send(estSock, "Invalid command. USAGE: <port> -l/-g [file]", 43, 0);
		return -1;
	}

	// Validate command. Logic: this OR that -> not (this OR that) == not this AND not that
	// If the command is neither -l not -g, report the error.
	if (strcmp(command[1], "-l") != 0 && strcmp(command[1], "-g") != 0) {
		send(estSock, "Invalid command. USAGE: <port> -l/-g [file]", 43, 0);
		return -1;
	}
	
	// Execute command
	// Send directory
	if (strcmp(command[1], "-l") == 0) {

	}
	else {

	}
	

}

int main(int argc, char *argv[]) {
	int port, listenSocket, establishedSocket, valid;
	socklen_t sizeOfClient;
	struct sockaddr_in clientAddress;
	char host[1024], service[1024];

	// Check for and validate port number.
	if (argc != 2) {
		fprintf(stderr, "USAGE: ./%s server_port\n", argv[0]);
		exit(0);
	}

	// Convert the argument to a number and validate it's not a reserved port.
	port = atoi(argv[1]);
	if (port < 1028 || port > 65535) {
		fprintf(stderr, "Please choose a valid port between 1028 and 65535.\n",);
		exit(0);
	}

	// Set up and receive socket for listening
	listenSocket = Startup(port);

	printf("Server open on %d.\n", port);

	// Continuously accept clients and handle their requests. Must be interrupted with a signal.
	while(1) {
		// Accept a connection, waiting until a connection is established.
		sizeOfClient = sizeof(clientAddress);
		establishedSocket = accept(listenSocket, (struct sockaddr *)&clientAddress, &sizeOfClient);
		if (establishedSocket < 0) {
			Errror("ERROR accepting connection.");
		}

		// Print client info
		getpeername(establishedSocket, (struct sockaddr *)&clientAddress, &sizeOfClient);
		memset(host, '\0', sizeof(host));
		memset(service, '\0', sizeof(service));
		getnameinfo(&clientAddress, sizeOfClient, host, sizeof(host), service, sizeof(service), 0);
// could use NI_NOFQDN to "return only the hostname part of t he fully qualified domain name"
// could also try setting service to NULL, and sizeof(service) to 0
		printf("Connection from %s.\n", host);

		// Pass new socket to function to handle the request. It returns -1 on an error, in which case
		// the program attempts to handle the request again. When a 1 is returned, the loop breaks.
		valid = -1;
		while(valid == -1) {
			valid = HandleRequest(establishedSocket);
		}

		// Close the socket
		close(establishedSocket);
		

	}


	return 0;
}
