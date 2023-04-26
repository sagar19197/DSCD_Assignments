# GROUP 13 : DSCD PROJECT 2023
# File for MapWorkers 


# Importing modules - 
from concurrent import futures;
import grpc;

# Importing Registry server proto -
import Master_pb2;
import Master_pb2_grpc;

# For taking input from commandline -
import sys;


# MASTER ADDRESS - 
MASTER_SERVER_ADDRESS = "localhost:8000";


class MapWorkerServiceServicer(Master_pb2_grpc.MapWorkerServiceServicer):
	def MapWorker(self, request, context):


		print("Request from Master");

		FileLocations = Master_pb2.FileLocations();
		new_location = FileLocations.fileLocation;

		for file in request.fileLocation:
			print(file);
			new_location.append(file);

		return FileLocations;





# Checking Condition for Usage of this file - 
if len(sys.argv) != 2:
	print("Usage ERROR: Please ENTER address of the server as argument. Usage: python mapWorker.py [address]");
	exit();


mapWorker_address = sys.argv[1];

print("\n WELCOME MapWorker SERVER, Your address:", mapWorker_address);

# SETTING UP THE mapWorker Servers -
mapWorker_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10));

# Adding Services - 
Master_pb2_grpc.add_MapWorkerServiceServicer_to_server(MapWorkerServiceServicer(), mapWorker_server);

# adding insecure port - 
mapWorker_server.add_insecure_port(mapWorker_address);
mapWorker_server.start();

mapWorker_server.wait_for_termination();
