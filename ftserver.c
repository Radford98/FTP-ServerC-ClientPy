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

/* Startup(int port): Creates and sets up a socket on the port number. Begins listening, but only accepts 1
 * connection at a time.
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
	listen(listenSocket, 1);					// Need to accept 1 connection at a time

	return listenSocket;

}

/* HandleRequest():
 * Pre:
 * Post:
 */
void HandleRequest() {



}

int main(int argc, char *argv[]) {
	int port, listenSocket;

	// Check for and validate port number.
	if (argc != 2) {
		fprintf(stderr, "USAGE: ./%s server_port\n", argv[0]);
		exit(0);
	}

	port = atoi(argv[1]);
	if (port == 0 || port < 1028 || port > 65535) {
		fprintf(stderr, "Please choose a valid port between 1028 and 65535.\n",);
		exit(0);
	}

	// Set up and receive socket for listening
	listenSocket = Startup(port);


	return 0;
}
