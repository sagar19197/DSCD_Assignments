# GROUP 13 : DSCD PROJECT 2023
# File for ReduceWorkers 


# Importing modules - 
from concurrent import futures;
import grpc;

# Importing Registry server proto -
import Master_pb2;
import Master_pb2_grpc;

# For taking input from commandline -
import sys;
# FOR handling FIles -
import os;


# MASTER ADDRESS - 
MASTER_SERVER_ADDRESS = "localhost:8000";


# Service for ReduceWorker
class ReduceWorkerServiceServicer(Master_pb2_grpc.ReduceWorkerServiceServicer):
	def ReduceWorker(self, request, context):

		print("Request from MASTER: Recieved Following File Locations:\n");

		FileLocations = Master_pb2.FileLocations();
		new_location = FileLocations.fileLocation;

		for file in request.fileLocation:
			print(file);
			new_location.append(file);

		return FileLocations;


# Checking Condition for Usage of this file - 
if len(sys.argv) != 3:
	print("Usage ERROR: Please ENTER address of the server as argument. Usage: python reduceWorker.py [address] [OPERATION]");
	exit();


reduceWorker_address = sys.argv[1];
reduceWorker_operation = sys.argv[2];


# Creating directories for storing files 
server_dir = os.path.join(os.getcwd(), "Files");

# If Files Directory not exists
if not os.path.exists(server_dir):
	os.mkdir(server_dir);

server_dir = os.path.join(server_dir, "reduce_Worker_"+ reduceWorker_address[10:]);
# If Server Directory not exists
if not os.path.exists(server_dir):
	os.mkdir(server_dir);



print("\n WELCOME REDUCE Worker SERVER, Your address:", reduceWorker_address,"\n");

# SETTING UP THE reduceWorker Servers -
reduceWorker_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10));

# Adding Services - 
Master_pb2_grpc.add_ReduceWorkerServiceServicer_to_server(ReduceWorkerServiceServicer(), reduceWorker_server);

# adding insecure port - 
reduceWorker_server.add_insecure_port(reduceWorker_address);
reduceWorker_server.start();

reduceWorker_server.wait_for_termination();