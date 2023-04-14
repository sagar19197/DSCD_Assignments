# GROUP 13 : DSCD ASSIGNMENT
# File for SERVER Implementation - 

import grpc
from concurrent import futures;

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;

# Importing Server Proto - 
import Server_pb2;
import Server_pb2_grpc;

# For taking input from commandline
import sys;
# For using DATETIME
from datetime import datetime 
# For storing information - 
import os;

# REGISTRY SERVER ADDRESS - 
REGISTRY_SERVER_ADDRESS = "localhost:8000";




# Service for Writting File
class ClientWriteServiceServicer(object):
	def ClientWrite(self, request, context):
		global FileList ;
		global server_dir;

		print("RECIEVED FILE WRITE REQUEST FROM CLIENT OF FILE UUID:", request.uuid);

		# Condition checks

		file_with_uuid = None;
		file_with_filename = None;

		for files in FileList.files:
			if (files.uuid == request.uuid):
				file_with_uuid = files;
				break;

		for files in FileList.files:
			if (files.filename == request.name):
				file_with_filename = files;
				break;

		res_new_file = False;
		res_update_file = False;

		if file_with_uuid == None:
			# UUID DOES NOT EXIST 
			if file_with_filename != None :
				# UUID DOES NOT EXIST, BUT FILE with Given Name Exist
				clientWriteResponse = Server_pb2.ClientWriteResponse(status = "FILE WITH SAME NAME ALREADY EXISTS", uuid = None , timestamp = None);
				return clientWriteResponse;
			else :
				# UUID DOES NOT EXIST AND FILE NAME NOT EXIST
				res_new_file = True;
		else:
			# UUID EXISTS
			if file_with_filename == None:
				# UUID EXISTS AND FILENAME DOES NOT EXISTS
				clientWriteResponse = Server_pb2.ClientWriteResponse(status = "DELETED FILE CAN NOT BE UPDATED", uuid = None , timestamp = None);
				return clientWriteResponse;

			elif (file_with_filename != None) and (file_with_filename != file_with_uuid):
				# UUID EXISTS, FILENAME EXISTS, But UUID DOES NOT MATCH WITH FILENAME
				# User is trying to create 2 FILES For same UUID
				clientWriteResponse = Server_pb2.ClientWriteResponse(status = "FILENAME DOES NOT MATCH WITH UUID", uuid = None , timestamp = None);
				return clientWriteResponse; 
			else:
				# UUID EXISTS, FILENAME EXISTS AND MAPPING EXISTS
				res_update_file = True;

		if (res_update_file == True) or (res_new_file == True): 

			if (res_update_file == False):
				new_file = FileList.files.add();
				new_file.uuid = request.uuid;
				new_file.filename = request.name;

				curr_now = datetime.now();
				new_file.timestamp = curr_now.strftime("%d/%m/%Y %H:%M:%S");
			else:
				new_file = file_with_uuid;
				curr_now = datetime.now();
				new_file.timestamp = curr_now.strftime("%d/%m/%Y %H:%M:%S");


			# Writting content : Making directory and saving files
			filename =  server_dir +"\\"+ str(request.name)+".txt";
			with open(filename, "w") as file:
				file.write(request.content);


			clientWriteResponse = Server_pb2.ClientWriteResponse(status = "SUCCESS", uuid = new_file.uuid, timestamp = new_file.timestamp);
			return clientWriteResponse;

		# SOMETHING BAD HAPPENED
		clientWriteResponse = Server_pb2.ClientWriteResponse(status = "SOMETHING BAD HAPPENED", uuid = None , timestamp = None);
		return clientWriteResponse;






# Creating Variable for FileList for storing Filename, uuid and Timestamp
FileList = Server_pb2.FileList();

if len(sys.argv) != 2:
	print("Please ENTER address of the server as argument. Usage: python server.py [address]");

server_address = sys.argv[1];

print("\nWELCOME SERVER, Your address:", server_address);

print("Initiating Connection with Registry SERVER");
channel = grpc.insecure_channel(REGISTRY_SERVER_ADDRESS);
# ServerStub - 
server_stub =  RegistryServer_pb2_grpc.RegisterServiceStub(channel);
registry_server_request = RegistryServer_pb2.ServerRequest(address =server_address);
registry_server_response = server_stub.Register(registry_server_request);

print("STATUS:", registry_server_response.status);



# Creating directories for storing files 
server_dir = os.path.join(os.getcwd(), "Files");

# If Files Directory not exists
if not os.path.exists(server_dir):
	os.mkdir(server_dir);

server_dir = os.path.join(server_dir, server_address[10:]);
# If Server Directory not exists
if not os.path.exists(server_dir):
	os.mkdir(server_dir);




# Creating  Server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# ADDING services

# Adding Write Services - 
Server_pb2_grpc.add_ClientWriteServiceServicer_to_server(ClientWriteServiceServicer(), server);
# Adding Read Services -
#Server_pb2_grpc.add_ClientReadServiceServicer_to_server(ClientReadServiceServicer(), server);
# Adding Delete Services -
#Server_pb2_grpc.add_ClientDeleteServiceServicer_to_server(ClientDeleteServiceServicer(), server);

# adding insecure port - 
server.add_insecure_port(server_address);
server.start();

server.wait_for_termination();
