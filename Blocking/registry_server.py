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
		global PRIMARY_SERVER;

		# Checking condition for joining server - 
		if (len(ServerList.servers) >= MAXSERVERS):
			return RegistryServer_pb2.ServerResponse(response = "FAILED");
		if request.address == "localhost:8000":
			return RegistryServer_pb2.ServerResponse(response = "FAILED, SERVER ADDRESS ALREADY TAKEN !!");
		for server in ServerList.servers:
			if server.address == request.address:
				return RegistryServer_pb2.ServerResponse(response = "FAILED, SERVER ADDRESS ALREADY TAKEN !!");

		server_msg = f"JOIN REQUEST FROM {request.address}";
		print(server_msg);

		# Adding servers - 
		new_server = ServerList.servers.add();
		new_server.address = request.address;

		if PRIMARY_SERVER == "":
			PRIMARY_SERVER = request.address;

		return RegistryServer_pb2.ServerResponse(address = PRIMARY_SERVER);



# Setting MAXSERVERS
MAXSERVERS = 10;
# Creating variable for ServerList - 
ServerList = RegistryServer_pb2.ServerList();

# Primary Server
PRIMARY_SERVER = "";

# REGISTRY SERVERS INFO -
registry_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
# adding services - 
RegistryServer_pb2_grpc.add_RegisterServiceServicer_to_server(RegisterServiceServicer(), registry_server);

# adding insecure port - 
registry_server.add_insecure_port("[::]:8000");
registry_server.start();

print("\nWELCOME REGISTRY SERVER !! Your address: localhost:8000");
registry_server.wait_for_termination();