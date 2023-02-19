# GROUP 13 : DSCD ASSIGNMENT
# File for REGISTRY SERVER

# Importing modules - 
from concurrent import futures;
import grpc;

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;


# Extending class for server servicer - 
class RegisterServiceServicer(RegistryServer_pb2_grpc.RegisterServiceServicer):
	def Register(self, request, context):
		global ServerList;
		global MAXSERVERS;

		# Checking condition for joining server - 
		if (len(ServerList.servers) >= MAXSERVERS):
			return RegistryServer_pb2.ServerResponse(response = "FAILED");
		if request.address == "localhost:8000":
			return RegistryServer_pb2.ServerResponse(response = "FAILED, SERVER ADDRESS ALREADY TAKEN !!");
		for server in ServerList.servers:
			if server.name == request.name:
				return RegistryServer_pb2.ServerResponse(response = "FAILED, SERVER NAME ALREADY TAKEN !!");
			if server.address == request.address:
				return RegistryServer_pb2.ServerResponse(response = "FAILED, SERVER ADDRESS ALREADY TAKEN !!");

		server_msg = f"JOIN REQUEST BY {request.name} FROM {request.address}";
		print(server_msg);

		# Adding servers - 
		new_server = ServerList.servers.add();
		new_server.name = request.name;
		new_server.address = request.address;

		return RegistryServer_pb2.ServerResponse(response = "SUCCESS");

# Extending class for clients servicer - 
class GetServerListServiceServicer(RegistryServer_pb2_grpc.GetServerListServiceServicer):
	def GetServerList(self, request, context):
		server_msg = f"SERVER LIST REQUEST FROM {request.client_id}";
		print(server_msg);
		global ServerList;
		return RegistryServer_pb2.ClientResponse(serverList = ServerList);


# Setting MAXSERVERS
MAXSERVERS = 10;
# Creating variable for ServerList - 
ServerList = RegistryServer_pb2.ServerList();
# REGISTRY SERVERS INFO -
registry_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
# adding services - 
RegistryServer_pb2_grpc.add_RegisterServiceServicer_to_server(RegisterServiceServicer(), registry_server);
RegistryServer_pb2_grpc.add_GetServerListServiceServicer_to_server(GetServerListServiceServicer(), registry_server);
# adding insecure port - 
registry_server.add_insecure_port("[::]:8000");
registry_server.start();
print("\nWELCOME REGISTRY SERVER !! Your address: localhost:8000");
registry_server.wait_for_termination();