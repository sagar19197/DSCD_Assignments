# GROUP 13 : DSCD ASSIGNMENT
# File for SERVER Implementation - 

import grpc
from concurrent import futures;

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;


# For taking input from commandline
import sys;

if len(sys.argv) != 2:
	print("Please ENTER address of the server as argument. Usage: python server.py [address]");


PRIMARY_SERVER = "";
server_address = sys.argv[1];

print("\nWELCOME SERVER, Your address:", server_address);

print("Initiating Connection with Registry SERVER");
channel = grpc.insecure_channel("localhost:8000");
# ServerStub - 
server_stub =  RegistryServer_pb2_grpc.RegisterServiceStub(channel);
registry_server_request = RegistryServer_pb2.ServerRequest(address =server_address);
registry_server_response = server_stub.Register(registry_server_request);

PRIMARY_SERVER = registry_server_response.address;

print("PRIMARY SERVER PRESENT AT:", PRIMARY_SERVER);


