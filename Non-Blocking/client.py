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

import sys;

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
registry_server_request = RegistryServer_pb2.ClientRequest(client_id = client_id);
registry_server_response = CLIENT_STUB.GetServerList(registry_server_request);

serverList = registry_server_response.serverList.servers;
# Printing  information abot servers -
print("\nFollowing Information is Recieved from REGISTRY SERVER:");
for server in serverList:
	print(server.address);


#---------------------------------------------------------

def generateUID():
	return str(uuid.uuid1());


def ConnectToServer(server_address):
	if server_address == REGISTRY_SERVER_ADDRESS:
		print("FAILED, Can not connect Registry SERVER");
		server_address = "Not connected";
	else :
		# Insecure Channel-
		global CHANNEL;
		CHANNEL = grpc.insecure_channel(server_address);
		print("\nCONNECTION ESTABLISHED SUCCESSFULLY:",server_address);



def Write(filename, content, uuid):
	print("\nPROCESSING YOUR REQUEST \n");
	global CHANNEL;
	server_stub = Server_pb2_grpc.ClientWriteServiceStub(CHANNEL);
	clientWriteRequest = Server_pb2.ClientWriteRequest(name = filename, content = content, uuid = uuid);
	clientWriteResponse = server_stub.ClientWrite(clientWriteRequest);
	if clientWriteResponse.status == "SUCCESS":
		print("STATUS : ", clientWriteResponse.status);
		print("UUID : ",clientWriteResponse.uuid);
		print("VERSION : ", clientWriteResponse.timestamp);
	else:
		print("STATUS : ", clientWriteResponse.status);




def Read(file_uuid):
	print("\n PROCESSING YOUR REQUEST \n");
	global CHANNEL;
	server_stub = Server_pb2_grpc.ClientReadServiceStub(CHANNEL);
	clientReadRequest = Server_pb2.ClientReadRequest(uuid = file_uuid);
	clientReadResponse = server_stub.ClientRead(clientReadRequest);
	print("STATUS : ",clientReadResponse.status);
	print("NAME : ", clientReadResponse.name);
	print("CONTENT :", clientReadResponse.content);
	print("VERSION : ", clientReadResponse.timestamp);



def Delete(file_uuid):
	print("\n PROCESSING YOUR REQUEST \n");
	server_stub = Server_pb2_grpc.ClientDeleteServiceStub(CHANNEL);
	clientDeleteRequest = Server_pb2.ClientDeleteRequest(uuid = file_uuid);
	clientDeleteResponse = server_stub.ClientDelete(clientDeleteRequest);
	print("STATUS : ", clientDeleteResponse.status);




#-----------------------------------------------------

# NORMAL MODE
def NormalMode():
	print("-----------------------------------");
	global serverList;
	# Making connection with last Server in the list
	last_server = serverList[-1];
	ConnectToServer(last_server.address);
	# Performing Write Operation
	print("\n-----Performing WRITE operation-----\n");
	filename = "HelloWorld";
	content = "HELLO WORLD FROM PYTHON. Welcome";
	file_uuid = generateUID();
	Write(filename, content, file_uuid);

	print("\n-----Reading from all servers-----\n");
	# Reading from all servers one by one
	for server in serverList:
		# Making connection
		ConnectToServer(server.address);
		Read(file_uuid);

	# AGAIN PEFORMING WRITE OPERATION
	print("\n-----Performing WRITE operation-----\n");
	filename2 = "HelloWorld2";
	content2 = "THIS IS SECOND FILE. HELLO WORLD.";
	file_uuid2 = generateUID();
	Write(filename2, content2, file_uuid2);

	print("\n-----Reading from all servers-----\n");
	# Reading from all servers one by one
	for server in serverList:
		# Making connection
		ConnectToServer(server.address);
		Read(file_uuid2);


	print("\n-----Deleting Last created File-----\n");
	# Deleting recently created file
	Delete(file_uuid2);

	print("\n-----Reading DELETED file all servers-----\n");
	# Reading DELETED FILE from all servers one by one
	for server in serverList:
		# Making connection
		ConnectToServer(server.address);
		Read(file_uuid2);

	print("\n-----DELETING DELETED FILE-----\n");
	# Deleting DELETED FILE from all servers one by one
	for server in serverList:
		# Making connection
		ConnectToServer(server.address);
		Delete(file_uuid2);

	print("\n-----Writting with UUID of Deleted files-----\n");
	Write(filename2, content2, file_uuid2)

	print("\n-----Writting with NEW UUID But With Existing Filename-----\n");
	Write(filename, content, generateUID());

	print("\n-----Overwritng Existing FILE-----\n");
	Write(filename, content2, file_uuid);

	print("\n-----Reading from all servers-----\n");
	# Reading DELETED FILE from all servers one by one
	for server in serverList:
		# Making connection
		ConnectToServer(server.address);
		Read(file_uuid);

	print("\n-----Reading of UNKNOWN UUID-----\n");
	# Reading DELETED FILE from all servers one by one
	new_uuid = generateUID();
	for server in serverList:
		# Making connection
		ConnectToServer(server.address);
		Read(new_uuid);

	





#----------------------------------------------


# CUSTOM MODE
def CustomMode():
	server_address = "Not connected";

	while(True):
		print("-----------------------------------------");
		print("Please Enter Number of one of the following options:");
		print("1. Connect to Server");
		print("2. Write a File");
		print("3. Read a File");
		print("4. Delete a File");
		print("5. My Connection");
		print("6. Generate UUID ");
		print("7. EXIT")

		option = input("\n Enter Option Number : ");
		print("----------------------------------------\n")

		# Case handling - 
		if option == "1":

			server_address = input("Enter Server Address to Connect : ");
			ConnectToServer(server_address);

		elif option == "2" :

			if (server_address =="Not connected"):
				print("Please join to some server to do this operation.");
			else:
				# Write the file
				filename = input("Enter File Name : ");
				content = input("Enter Content : ");
				file_uuid = input("Enter UUID : ");
				Write(filename, content, file_uuid);


		elif option == "3" :

			if (server_address =="Not connected"):
				print("Please join to some server to do this operation.");
			else:
				# uuid -
				file_uuid = input("Enter UUID : ");
				Read(file_uuid);


		elif option == "4" :

			if (server_address =="Not connected"):
				print("Please join to some server to do this operation.");
			else:
				# uuid -
				file_uuid = input("Enter UUID : ");
				Delete(file_uuid);


		elif option == "5" :

			print("You are connected to : ",server_address);
			print("\nUse Connect to Server for changing connections");

		elif option == "6":
			print("UUID : ",generateUID());

		elif option == "7" :

			break;

		else:
			print("Invalid Input!! Please Enter again.");





mode = "CUSTOM";

if len(sys.argv) == 2:
	mode = sys.argv[1];


if mode == "CUSTOM":
	CustomMode();
else:
	NormalMode();



