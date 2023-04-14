# GROUP 13 : DSCD ASSIGNMENT
# File for REGISTRY SERVER

# Importing modules - 
from concurrent import futures;
import grpc;

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;


# For generating Random N_r and N_w
import random;

# For taking input from commandline
import sys;

# REGISTRY SERVER ADDRESS - 
REGISTRY_SERVER_ADDRESS = "localhost:8000";



# Extending class for server servicer - 
class RegisterServiceServicer(RegistryServer_pb2_grpc.RegisterServiceServicer):
	def Register(self, request, context):
		global ServerList;
		global MAXSERVERS;
		global REGISTRY_SERVER_ADDRESS;

		# Checking condition for joining server - 
		if (len(ServerList.servers) >= MAXSERVERS):
			return RegistryServer_pb2.ServerResponse(address = "FAILED");
		if request.address == REGISTRY_SERVER_ADDRESS:
			return RegistryServer_pb2.ServerResponse(address = "FAILED, SERVER ADDRESS ALREADY TAKEN !!");
		for server in ServerList.servers:
			if server.address == request.address:
				return RegistryServer_pb2.ServerResponse(address = "FAILED, SERVER ADDRESS ALREADY TAKEN !!");

		server_msg = f"JOIN REQUEST FROM {request.address}";
		print(server_msg);

		# Adding servers - 
		new_server = ServerList.servers.add();
		new_server.address = request.address;
		return RegistryServer_pb2.ServerResponse(status = "SUCCESS");


# Extending class for clients servicer - 
class GetServerListServiceServicer(RegistryServer_pb2_grpc.GetServerListServiceServicer):
	def GetServerList(self, request, context):
		global ServerList;
		global N_r, N_w;
		if(request.requestType == "all"):
			server_msg = f"SERVER LIST REQUEST FROM {request.client_id}";
			print(server_msg);
			return RegistryServer_pb2.ClientResponse(serverList = ServerList);

		elif (request.requestType == "read"):
			server_msg = f"N_r SERVERS LIST REQUEST FROM {request.client_id}";
			print(server_msg);
			random_NR = random.sample(range(len(ServerList.servers)), N_r);
			i = 0;
			new_ServerList = RegistryServer_pb2.ServerList();
			for servers in ServerList.servers:
				if i in random_NR:
					new_server = new_ServerList.servers.add();
					new_server.address = servers.address;
				i = i+1;
			return RegistryServer_pb2.ClientResponse(serverList = new_ServerList);


		elif (request.requestType == "write" or request.requestType == "delete"):
			server_msg = f"N_w SERVERS LIST REQUEST FROM {request.client_id}";
			print(server_msg);
			random_NR = random.sample(range(len(ServerList.servers)), N_w);
			i = 0;
			new_ServerList = RegistryServer_pb2.ServerList();
			for servers in ServerList.servers:
				if i in random_NR:
					new_server = new_ServerList.servers.add();
					new_server.address = servers.address;
				i = i+1;
			return RegistryServer_pb2.ClientResponse(serverList = new_ServerList);

		else:
			new_ServerList = RegistryServer_pb2.ServerList();
			return RegistryServer_pb2.ClientResponse(serverList = new_ServerList);


		



# Setting MAXSERVERS
MAXSERVERS = 30;
# Creating variable for ServerList - 
ServerList = RegistryServer_pb2.ServerList();


# REGISTRY SERVERS INFO -
registry_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
# adding services - 
RegistryServer_pb2_grpc.add_RegisterServiceServicer_to_server(RegisterServiceServicer(), registry_server);
RegistryServer_pb2_grpc.add_GetServerListServiceServicer_to_server(GetServerListServiceServicer(), registry_server);


# adding insecure port - 
registry_server.add_insecure_port(REGISTRY_SERVER_ADDRESS);
registry_server.start();


if len(sys.argv) == 4:
	N = int(sys.argv[1]);
	N_r = int(sys.argv[2]);
	N_w = int(sys.argv[3]);
	# Checking Conditions - 
	if ((N_w > (N/2)) and ((N_r + N_w) > N)) == False:
		print("ERROR : Please Enter Valid Set of values for N, N_r and N_w");
		exit();
else:
	# Taking Input for NR, NW and N
	while(True):
		N = int(input("Enter Total Servers (N) : "));
		N_r = int(input("Enter Number of Read Quorams (N_r) : "));
		N_w = int(input("Enter Number of Write Quorams (N_w) : "));
		# Checking Conditions - 
		if (N_w > (N/2)) and ((N_r + N_w) > N):
			break;
		else:
			print("ERROR : Please Enter Valid set of values for N, N_r and N_w ");



print("\nWELCOME REGISTRY SERVER !! Your address:",REGISTRY_SERVER_ADDRESS);
registry_server.wait_for_termination();