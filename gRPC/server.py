# GROUP 13 : DSCD ASSIGNMENT
# File for SERVER Implementation - 

import grpc
from concurrent import futures;

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;

# Importing Server proto
import Server_pb2;
import Server_pb2_grpc;

print("\nWELCOME SERVER, PLEASE ENTER -");
server_name = input("SERVER NAME: ");
server_address = input("SERVER ADDRESS: ");

print("Initiating Connection with Registry SERVER");
channel = grpc.insecure_channel("localhost:8000");
# ServerStub - 
server_stub =  RegistryServer_pb2_grpc.RegisterServiceStub(channel);
registry_server_request = RegistryServer_pb2.ServerRequest(name = server_name, address =server_address);
registry_server_response = server_stub.Register(registry_server_request);
print(registry_server_response.response);


class JoinServerServiceServicer(Server_pb2_grpc.JoinServerServiceServicer):
	def JoinServer(self, request, context):
		global MAXCLIENTS;
		global CLIENTELE;

		server_msg = f"JOIN REQUEST FROM {request.client_id}";
		print(server_msg);

		new_client = CLIENTELE.add();
		new_client.client_id = request.client_id;
		return Server_pb2.ServerResponse(response = "SUCCESS");


# Setting MAX_CLIENTS 
MAXCLIENTS = 10;
# CLIENTELE 
CLIENTELE = Server_pb2.CLIENTELE().clients;

if (registry_server_response.response == "SUCCESS"):
	
	# Server info  -
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10));
	# Adding services -
	Server_pb2_grpc.add_JoinServerServiceServicer_to_server(JoinServerServiceServicer(), server);
	# Adding insecure port - 
	server.add_insecure_port(server_address);
	server.start();
	print("\nSERVER STARTED SUCCESSFULLY !!");
	server.wait_for_termination();


