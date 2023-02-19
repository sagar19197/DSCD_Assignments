# GROUP 13 : DSCD ASSIGNMENT
# File for SERVER Implementation - 

import grpc

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;

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
