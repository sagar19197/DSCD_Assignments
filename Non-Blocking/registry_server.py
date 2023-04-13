# GROUP 13 : DSCD ASSIGNMENT
# File for REGISTRY SERVER

# Importing modules - 
from concurrent import futures;
import grpc;

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;


# REGISTRY SERVER ADDRESS - 
REGISTRY_SERVER_ADDRESS = "localhost:8000";


# Extending class for server servicer - 
class RegisterServiceServicer(RegistryServer_pb2_grpc.RegisterServiceServicer):
	def Register(self, request, context):
		global ServerList;
		global MAXSERVERS;
		global PRIMARY_SERVER;
		global PRIMARY_CHANNEL;
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

		if PRIMARY_SERVER == "":
			PRIMARY_SERVER = request.address;
			PRIMARY_CHANNEL = grpc.insecure_channel(PRIMARY_SERVER);
		else:
			# ServerStub - 
			print("SENDING ADDRESS:",request.address,"to PRIMARY SERVER");
			server_stub =  RegistryServer_pb2_grpc.InformPrimaryServerServiceStub(PRIMARY_CHANNEL);

			registry_server_request = RegistryServer_pb2.ServerRequest(address = request.address);
			registry_server_response = server_stub.InformPrimaryServer(registry_server_request);
			print(registry_server_response.response);
		return RegistryServer_pb2.ServerResponse(address = PRIMARY_SERVER);


# Extending class for clients servicer - 
class GetServerListServiceServicer(RegistryServer_pb2_grpc.GetServerListServiceServicer):
	def GetServerList(self, request, context):
		server_msg = f"SERVER LIST REQUEST FROM {request.client_id}";
		print(server_msg);
		global ServerList;
		return RegistryServer_pb2.ClientResponse(serverList = ServerList);



# Setting MAXSERVERS
MAXSERVERS = 30;
# Creating variable for ServerList - 
ServerList = RegistryServer_pb2.ServerList();

# Primary Server
PRIMARY_SERVER = "";
# PRIMARY CHANNEL
PRIMARY_CHANNEL ="";

# REGISTRY SERVERS INFO -
registry_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
# adding services - 
RegistryServer_pb2_grpc.add_RegisterServiceServicer_to_server(RegisterServiceServicer(), registry_server);
RegistryServer_pb2_grpc.add_GetServerListServiceServicer_to_server(GetServerListServiceServicer(), registry_server);


# adding insecure port - 
registry_server.add_insecure_port(REGISTRY_SERVER_ADDRESS);
registry_server.start();

print("\nWELCOME REGISTRY SERVER !! Your address:",REGISTRY_SERVER_ADDRESS);
registry_server.wait_for_termination();