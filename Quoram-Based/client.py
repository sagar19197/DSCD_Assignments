# GROUP 13 : DSCD ASSIGNMENT
# File for CLIENT Implementation - 

import grpc

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;

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