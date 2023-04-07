# GROUP 13 : DSCD ASSIGNMENT
# File for CLIENT Implementation - 

import grpc

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;

import uuid;


# REGISTRY SERVER ADDRESS - 
REGISTRY_SERVER_ADDRESS = "localhost:8000";

#Generating client id
client_id = str(uuid.uuid1());
print("\nWELCOME CLIENT USER, YOUR ACCOUNT UUID:",client_id,"\n");

print("Fetching List of active Servers from REGISTRY SERVER...");

# Creating Channel
CHANNEL = grpc.insecure_channel(REGISTRY_SERVER_ADDRESS);
# ClientStub - 
CLIENT_STUB =  RegistryServer_pb2_grpc.GetServerListServiceStub(CHANNEL);
registry_server_request = RegistryServer_pb2.ClientRequest(client_id = client_id);
registry_server_response = CLIENT_STUB.GetServerList(registry_server_request);

serverList = registry_server_response.serverList.servers;
# Printing  information abot servers -
print("\nFollowing Information is Recieved from REGISTRY SERVER:");
for server in serverList:
	print(server.address);


server_address = "Not connected";

while(True):
	print("-------------------------------------");
	print("Please Enter Number of one of the following options:");
	print("1. Connect to Server");
	print("2. Write a File");
	print("3. Read a File");
	print("4. Delete a File");
	print("5. My Connection");
	print("6. EXIT");

	option = input("\n Enter Option Number : ");
	print("----------------------------------------\n")

	# Case handling - 
	if option == "1":

		server_address = input("Enter Server Address to Connect : ");
		if server_address == REGISTRY_SERVER_ADDRESS:
			print("FAILED, Can not connect Registry SERVER");
			server_address = "Not connected";
		else :
			# Insecure Channel-
			CHANNEL = grpc.insecure_channel(server_address);

	elif option == "2" :

		if (server_address =="Not connected"):
			print("Please join to some server to do this operation.");
		else:
			print("Will implement this method");

	elif option == "3" :

		if (server_address =="Not connected"):
			print("Please join to some server to do this operation.");
		else:
			print("Will implement this method");

	elif option == "4" :

		if (server_address =="Not connected"):
			print("Please join to some server to do this operation.");
		else:
			print("Will implement this method");

	elif option == "5" :

		print("You are connected to : ",server_address);
		print("\nUse Connect to Server for changing connections");

	elif option == "6" :

		break;

	else:
		print("Invalid Input!! Please Enter again.");


