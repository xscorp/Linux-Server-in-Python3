#!/usr/bin/env python3

import socket
import sys

def printUsage():
	print("[ERROR]: Invalid number of arguments!")
	print(
	"\nUSAGE:\n"+
	"______\n\n"+
	"$ ./server.py [port]\n"+
	"[NOTE] You need to be root for using port below 1025\n\n")
	sys.exit()

def errorExit():
	client_socket.close()
	sys.exit()


if len(sys.argv) != 2:
	printUsage()

#check if the port number entered by user is numeric or not
try:
	port = int(sys.argv[1])
except ValueError:
	print("Invalid value of port! Port must be numeric!")
	sys.exit()


#creating socket
try:
	server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM , 0)
except socket.error:
	print("Error occured in socket.socket() : " , socket.error)
	server_socket = None
else:	
	print("[+]TCP IPV4 socket created")


#binding localhost IP address and port to the socket
try:
	server_socket.bind(("127.0.0.1" , port))
except socket.error:
	print("[ERROR]: bind(): " , socket.error)
	errorExit()
	
else:
	print("[+]IP address and port is binded to socket")


#listening on the socket for connections
try:
	server_socket.listen(5)
except socket.error:
	print("[ERROR]: listen(): " , socket.error)
	errorExit()
	
else:
	print("[+]Server listening for incomming connections")
	
#accepting connection request from client
try:
	client_socket , client_address = server_socket.accept()
except socket.error:
	print("[ERROR]: accept(): " , socket.error)
	errorExit()
else:
	print("\n***Received connection from:" , client_address[0] , "***")
	

#talking to client
while True:
	print("\nYou:")
	try:
		#the data must be sent in the form of byte string and not string
		#To convert data to byte string, encode() is used
		client_socket.sendall(input().encode())

	except socket.error:
		print("[ERROR]: sendall(): " , socket.error)
		errorExit()
	
	except:
		print("\n[+]You closed the connection\n")
		errorExit()
		
	try:
		client_message = client_socket.recv(1024)	
		if len(client_message) == 0:		#0 bytes received
			print("\n\nConnection closed by the client!")
			errorExit()
			
	except socket.error:
		print("[ERROR]: recv(): " , socket.error)
		errorExit()
		
	except:
		print("\n[+]Connection closed!")
		errorExit()
		
	else:
		print("\nThey:")
		#data received is of type 'byte'. Decode it in either ASCII or UTF-8
		print(client_message.decode("ascii"))
		

#closing the socket
server_socket.close()
