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




# Service for InformingPrimaryServer
class InformPrimaryServerServiceServicer(RegistryServer_pb2_grpc.InformPrimaryServerServiceServicer):
	def InformPrimaryServer(self, request, context):
		global ServerList;
		global MAXSERVERS;

		server_msg = f"JOIN REQUEST FROM {request.address}";
		print(server_msg);
		# Adding servers - 
		new_server = ServerList.servers.add();
		new_server.address = request.address;

		return RegistryServer_pb2.PrimaryResponse(response = ("PRIMARY REPLICA ADDED "+str(request.address)+" Successfully"));




# Service for Writting File
class ClientWriteServiceServicer(object):
	def ClientWrite(self, request, context):
		global PRIMARY_CHANNEL;
		global FileList ;
		global ServerList;
		global server_dir;

		if PRIMARY_CHANNEL == "":
			# Primary server
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

				# Blocking CALL 

				for servers in ServerList.servers:
					channel = grpc.insecure_channel(servers.address);
					server_stub = Server_pb2_grpc.PrimaryWriteServiceStub(channel);
					clientWriteRequest = Server_pb2.ClientWriteRequest(name = new_file.filename, content = request.content, uuid = new_file.uuid);
					primary_write_request = Server_pb2.PrimaryWriteRequest(clientWriteRequest = clientWriteRequest, timestamp = new_file.timestamp);
					primary_write_response = server_stub.PrimaryWrite(primary_write_request);
					if(primary_write_response.status != "SUCCESS"):
						clientWriteResponse = Server_pb2.ClientWriteResponse(status = "FAILED");
						return clientWriteResponse;

				# IF all are SUCCESS -
				clientWriteResponse = Server_pb2.ClientWriteResponse(status = "SUCCESS", uuid = new_file.uuid, timestamp = new_file.timestamp);
				return clientWriteResponse;

			# SOMETHING BAD HAPPENED
			clientWriteResponse = Server_pb2.ClientWriteResponse(status = "SOMETHING BAD HAPPENED", uuid = None , timestamp = None);
			return clientWriteResponse;

		else:
			# Sending to Primary
			print("RECIEVED FILE WRITE REQUEST FROM CLIENT OF FILE UUID:", request.uuid);
			primary_stub = Server_pb2_grpc.ClientWriteServiceStub(PRIMARY_CHANNEL);
			clientWriteRequest = Server_pb2.ClientWriteRequest(name = request.name, content = request.content, uuid = request.uuid);
			return primary_stub.ClientWrite(clientWriteRequest);






# SERVICE FOR READING FILES FROM REPLICA
class ClientReadServiceServicer(object):
	def ClientRead(self, request, context):
		global FileList;
		global server_dir;

		print("RECIEVED READ REQUEST FROM CLIENT FOR FILE UUID:",request.uuid);
		# Conditions checking
		file = None;
		for files in FileList.files:
			if files.uuid == request.uuid:
				file = files;
				break;

		if file == None:
			# UUID Does not exist
			clientReadResponse = Server_pb2.ClientReadResponse(status = "FILE DOES NOT EXIST", name= None, content = None, timestamp = None);
			return clientReadResponse;
		else :
			# UUID EXISTS
			file_path = server_dir + "\\" + file.filename+".txt";
			if not os.path.exists(file_path):
				# UUID EXISTS BUT File does not exist
				clientReadResponse = Server_pb2.ClientReadResponse(status = "FILE ALREADY DELETED", name= None, content = None, timestamp = None);
				return clientReadResponse;
			else:
				# UUID EXISTS AND FILE ALSO EXISTS
				content = "";
				with open(file_path, "r") as f:
					content = f.read(); 
				clientReadResponse = Server_pb2.ClientReadResponse(status = "SUCCESS", name= file.filename, content = content, timestamp = file.timestamp);
				return clientReadResponse;






# SERVICE FOR DELETING FILE FROM SERVER
class ClientDeleteServiceServicer(object):
	def ClientDelete(self, request, context):
		global PRIMARY_CHANNEL;
		global FileList ;
		global ServerList;
		global server_dir;

		if PRIMARY_CHANNEL == "":
			# Primary server
			print("RECIEVED DELETE REQUEST FROM CLIENT OF FILE UUID:", request.uuid);

			# Condition checks

			file_with_uuid = None;

			for files in FileList.files:
				if (files.uuid == request.uuid):
					file_with_uuid = files;
					break;

			if file_with_uuid == None :
				# UUID DOES NOT EXIST
				clientDeleteResponse = Server_pb2.ClientDeleteResponse(status = "FILE DOES NOT EXIST");
				return clientDeleteResponse;
			else:
				# UUID EXISTS
				file_path = server_dir + "\\" + file_with_uuid.filename+".txt";

				if not os.path.exists(file_path):
					# UUID EXISTS BUT File does not exist
					clientDeleteResponse = Server_pb2.ClientDeleteResponse(status = "FILE ALREADY DELETED");
					return clientDeleteResponse;
				else:
					# UUID EXISTS AND FILE ALSO EXISTS

					# Deleting from local storage -
					os.remove(file_path);
					# Deleting from in-memory and updating timestamp-
					file_with_uuid.filename = "";
					curr_now = datetime.now();
					file_with_uuid.timestamp = curr_now.strftime("%d/%m/%Y %H:%M:%S");


				# Blocking CALL 

				for servers in ServerList.servers:
					channel = grpc.insecure_channel(servers.address);
					server_stub = Server_pb2_grpc.PrimaryDeleteServiceStub(channel);
					clientDeleteRequest = Server_pb2.ClientDeleteRequest(uuid = request.uuid);
					primary_Delete_response = server_stub.PrimaryDelete(clientDeleteRequest);
					if(primary_Delete_response.status != "SUCCESS"):
						clientDeleteResponse = Server_pb2.ClientDeleteResponse(status = "FAILED");
						return clientDeleteResponse;

				# IF all are SUCCESS -
				clientDeleteResponse = Server_pb2.ClientDeleteResponse(status = "SUCCESS");
				return clientDeleteResponse;
		else:
			# Sending to Primary
			print("RECIEVED DELETE REQUEST FROM CLIENT OF FILE UUID:", request.uuid);
			primary_stub = Server_pb2_grpc.ClientDeleteServiceStub(PRIMARY_CHANNEL);
			clientDeleteRequest = Server_pb2.ClientDeleteRequest(uuid = request.uuid);
			return primary_stub.ClientDelete(clientDeleteRequest);






# Service which invokes when PRIMARY SENDS Write Request to REPLICAS
class PrimaryWriteServiceServicer(object):
	def PrimaryWrite(self, request, context):
		global server_dir;
		global FileList;

		print("RECIEVED FILE WRITE REQUEST FROM PRIMARY OF FILE UUID:", request.clientWriteRequest.uuid);
		# Condition checks
			
		file_with_uuid = None;
		file_with_filename = None;

		for files in FileList.files:
			if (files.uuid == request.clientWriteRequest.uuid):
				file_with_uuid = files;
				break;

		for files in FileList.files:
			if (files.filename == request.clientWriteRequest.name):
				file_with_filename = files;
				break;

		res_new_file = False;
		res_update_file = False;

		if file_with_uuid == None:
			# UUID DOES NOT EXIST 
			if file_with_filename != None :
				# UUID DOES NOT EXIST, BUT FILE with Given Name Exist
				clientWriteResponse = Server_pb2.PrimaryWriteResponse(status = "FILE WITH SAME NAME ALREADY EXISTS");
				return clientWriteResponse;
			else :
				# UUID DOES NOT EXIST AND FILE NAME NOT EXIST
				res_new_file = True;
		else:
			# UUID EXISTS
			if file_with_filename == None:
				# UUID EXISTS AND FILENAME DOES NOT EXISTS
				clientWriteResponse = Server_pb2.PrimaryWriteResponse(status = "DELETED FILE CAN NOT BE UPDATED");
				return clientWriteResponse;

			elif (file_with_filename != None) and (file_with_filename != file_with_uuid):
				# UUID EXISTS, FILENAME EXISTS, But UUID DOES NOT MATCH WITH FILENAME
				# User is trying to create 2 FILES For same UUID
				clientWriteResponse = Server_pb2.PrimaryWriteResponse(status = "FILENAME DOES NOT MATCH WITH UUID");
				return clientWriteResponse; 
			else:
				# UUID EXISTS, FILENAME EXISTS AND MAPPING EXISTS
				res_update_file = True;



		if (res_update_file == True) or (res_new_file == True): 

			if (res_update_file == False):
				new_file = FileList.files.add();
				new_file.uuid = request.clientWriteRequest.uuid;
				new_file.filename = request.clientWriteRequest.name;
				new_file.timestamp = request.timestamp;

			else:
				new_file = file_with_uuid;
				new_file.timestamp = request.timestamp;

			filename =  server_dir +"\\"+ str(request.clientWriteRequest.name)+".txt";
			with open(filename, "w") as file:
				file.write(request.clientWriteRequest.content);

			return Server_pb2.PrimaryWriteResponse(status = "SUCCESS");

		return Server_pb2.PrimaryWriteResponse(status = "FAILED");






# SERVICE WILL BE INVOKED WHEN PRIMARY SEND REQUEST TO REPLICAS
class PrimaryDeleteServiceServicer(object):
	def PrimaryDelete(self, request, context):
		print("RECIEVED DELETE REQUEST FROM PRIMARY OF FILE UUID:", request.uuid);

		# Condition checks

		file_with_uuid = None;

		for files in FileList.files:
			if (files.uuid == request.uuid):
				file_with_uuid = files;
				break;

		if file_with_uuid == None :
			# UUID DOES NOT EXIST
			clientDeleteResponse = Server_pb2.PrimaryWriteResponse(status = "FILE DOES NOT EXIST");
			return clientDeleteResponse;
		else:
			# UUID EXISTS
			file_path = server_dir + "\\" + file_with_uuid.filename+".txt";

			if not os.path.exists(file_path):
				# UUID EXISTS BUT File does not exist
				clientDeleteResponse = Server_pb2.PrimaryWriteResponse(status = "FILE ALREADY DELETED");
				return clientDeleteResponse;
			else:
				# UUID EXISTS AND FILE ALSO EXISTS

				# Deleting from local storage -
				os.remove(file_path);
				# Deleting from in-memory and updating timestamp-
				file_with_uuid.filename = "";
				curr_now = datetime.now();
				file_with_uuid.timestamp = curr_now.strftime("%d/%m/%Y %H:%M:%S");

				return Server_pb2.PrimaryWriteResponse(status = "SUCCESS");








# Setting MAXSERVERS
MAXSERVERS = 10;
# Creating variable for ServerList - 
ServerList = RegistryServer_pb2.ServerList();


# Creating Variable for FileList for storing Filename, uuid and Timestamp
FileList = Server_pb2.FileList();


if len(sys.argv) != 2:
	print("Please ENTER address of the server as argument. Usage: python server.py [address]");


PRIMARY_SERVER = "";
server_address = sys.argv[1];

print("\nWELCOME SERVER, Your address:", server_address);

print("Initiating Connection with Registry SERVER");
channel = grpc.insecure_channel(REGISTRY_SERVER_ADDRESS);
# ServerStub - 
server_stub =  RegistryServer_pb2_grpc.RegisterServiceStub(channel);
registry_server_request = RegistryServer_pb2.ServerRequest(address =server_address);
registry_server_response = server_stub.Register(registry_server_request);

PRIMARY_SERVER = registry_server_response.address;

print("PRIMARY SERVER PRESENT AT:", PRIMARY_SERVER);

PRIMARY_CHANNEL = "";
if PRIMARY_SERVER != server_address:
	PRIMARY_CHANNEL = grpc.insecure_channel(PRIMARY_SERVER);



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
RegistryServer_pb2_grpc.add_InformPrimaryServerServiceServicer_to_server(InformPrimaryServerServiceServicer(), server);

# Adding Write Services - 
Server_pb2_grpc.add_ClientWriteServiceServicer_to_server(ClientWriteServiceServicer(), server);
Server_pb2_grpc.add_PrimaryWriteServiceServicer_to_server(PrimaryWriteServiceServicer(), server);
# Adding Read Services -
Server_pb2_grpc.add_ClientReadServiceServicer_to_server(ClientReadServiceServicer(), server);
# Adding Delete Services -
Server_pb2_grpc.add_ClientDeleteServiceServicer_to_server(ClientDeleteServiceServicer(), server);
Server_pb2_grpc.add_PrimaryDeleteServiceServicer_to_server(PrimaryDeleteServiceServicer(), server);

# adding insecure port - 
server.add_insecure_port(server_address);
server.start();

server.wait_for_termination();