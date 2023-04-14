# GROUP 13 : DSCD ASSIGNMENT
# File for CLIENT Implementation - 

import grpc

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;

# Importing Server Proto - 
import Server_pb2;
import Server_pb2_grpc;

import uuid;

#----------------------------------------------------
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
registry_server_request = RegistryServer_pb2.ClientRequest(client_id = client_id, requestType = "all");
registry_server_response = CLIENT_STUB.GetServerList(registry_server_request);

serverList = registry_server_response.serverList.servers;
# Printing  information abot servers -
print("\nFollowing Information is Recieved from REGISTRY SERVER:");
for server in serverList:
	print(server.address);


#---------------------------------------------------------

def generateUID():
	return str(uuid.uuid1());



def getServerList():
	getServerList_operation("all");



def getServerList_operation(requestType):
	global CHANNEL;

	# ClientStub - 
	CLIENT_STUB =  RegistryServer_pb2_grpc.GetServerListServiceStub(CHANNEL);
	registry_server_request = RegistryServer_pb2.ClientRequest(client_id = client_id, requestType = requestType);
	registry_server_response = CLIENT_STUB.GetServerList(registry_server_request);

	new_serverList = registry_server_response.serverList.servers;
	# Printing  information abot servers -
	print("Following Information is Recieved from REGISTRY SERVER:");
	for server in new_serverList:
		print(server.address);

	return new_serverList;




def Write(filename, content, file_uuid):
	print("\nPROCESSING YOUR REQUEST \n");

	# Contacting Registry Servers for Fetching list of N_w Servers
	new_serverList = getServerList_operation("write");

	for server in new_serverList:
		# Generating channel
		channel = grpc.insecure_channel(server.address);
		server_stub = Server_pb2_grpc.ClientWriteServiceStub(channel);
		clientWriteRequest = Server_pb2.ClientWriteRequest(name = filename, content = content, uuid = file_uuid);
		clientWriteResponse = server_stub.ClientWrite(clientWriteRequest);
		print("\nResponse from:",server.address);
		if clientWriteResponse.status == "SUCCESS":
			print("STATUS : ", clientWriteResponse.status);
			print("UUID : ",clientWriteResponse.uuid);
			print("VERSION : ", clientWriteResponse.timestamp);
		else:
			print("STATUS : ", clientWriteResponse.status);



#-----------------------------------------------------------


server_address = "Not connected";

while(True):
	print("-----------------------------------------");
	print("Please Enter Number of one of the following options:");
	print("1. GetServerList");
	print("2. Write a File");
	print("3. Read a File");
	print("4. Delete a File");
	print("5. Generate UUID ");
	print("6. EXIT")

	option = input("\n Enter Option Number : ");
	print("----------------------------------------\n")

	# Case handling - 
	if option == "1":

		getServerList();

	elif option == "2" :

		filename = input("Enter File Name : ");
		content = input("Enter Content : ");
		file_uuid = input("Enter UUID : ");
		Write(filename, content, file_uuid);


	elif option == "3" :

		file_uuid = input("Enter UUID : ");
		#Read(file_uuid);


	elif option == "4" :
		
		file_uuid = input("Enter UUID : ");
		#Delete(file_uuid);


	elif option == "5" :

		print("UUID : ",generateUID());

	elif option == "6":

		break;

	else:
		print("Invalid Input!! Please Enter again.");
