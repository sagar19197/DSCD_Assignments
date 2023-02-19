# GROUP 13 : DSCD ASSIGNMENT
# File for CLIENT Implementation - 

import grpc

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;
import uuid;

#Generating client id
client_id = str(uuid.uuid1());
print("\nWELCOME CLIENT USER, YOUR UUID:",client_id);

print("Fetching List of active Servers from Registry SERVER...\n");
channel = grpc.insecure_channel("localhost:8000");

# ClientStub - 
client_stub =  RegistryServer_pb2_grpc.GetServerListServiceStub(channel);
registry_server_request = RegistryServer_pb2.ClientRequest(client_id = client_id);
registry_server_response = client_stub.GetServerList(registry_server_request);

serverList = registry_server_response.serverList.servers;
# Printing  information abot servers -
for server in serverList:
	print(server.name,"-",server.address);
