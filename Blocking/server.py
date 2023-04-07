# GROUP 13 : DSCD ASSIGNMENT
# File for SERVER Implementation - 

import grpc
from concurrent import futures;

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;


# For taking input from commandline
import sys;


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




# Setting MAXSERVERS
MAXSERVERS = 10;
# Creating variable for ServerList - 
ServerList = RegistryServer_pb2.ServerList();

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


# Creating  Server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
# ADDING services
RegistryServer_pb2_grpc.add_InformPrimaryServerServiceServicer_to_server(InformPrimaryServerServiceServicer(), server);
# adding insecure port - 
server.add_insecure_port(server_address);
server.start();

server.wait_for_termination();