# GROUP 13 : DSCD PROJECT 2023
# File for Master


# Importing Registry server proto -
import Master_pb2;
import Master_pb2_grpc;

# For Spawning - 
import subprocess;

# importing grpc
import grpc;



# MASTER ADDRESS -
MASTER_SERVER_ADDRESS = "localhost:8000";

print("\n--------------------------------------------------------------");
print("\n WELCOME MASTER SERVER !! Your address:", MASTER_SERVER_ADDRESS);

# Taking Input - 
print("\n Please Provide Following Information - \n");

input_data_location = input("\n ENTER INPUT DATA LOCATION : ");
number_of_mappers = int(input("\n ENTER M (Number of Mappers) : "));
number_of_reducers = int(input("\n ENTER R (Number of Reducers) : "));
output_data_location = input("\n ENTER OUTPUT DATA LOCATION : ");

print("\n--------------------------------------------------------------\n");




# STEP 0 : SPAWNING MAPPERS AND REDUCERS - 

mapWorker_addressList = [];
spawning_commands = [];
# Get the path of the cmd.exe executable
cmd_path = subprocess.check_output('where cmd.exe').decode().split()[0]

# Spawning MapWorkers - 
for i in range(number_of_mappers):
	# MapWorkers start from 5000 ports
	port = 5000 + i;
	address = "localhost:" + str(port);

	# Adding this Address to mapWorker_addressList
	mapWorker_addressList.append(address);

	# creating spawning commands - 
	spawning_commands.append('python mapWorker.py '+ address);

# Spawning
for run_mapWorkers in spawning_commands:
	subprocess.Popen([cmd_path, '/c', 'start', 'cmd', '/k', run_mapWorkers]);



# DEMO COMMUNICATION - 

FileLocations = Master_pb2.FileLocations();
new_location = FileLocations.fileLocation;
new_location.append(output_data_location);

for mapWorkers in mapWorker_addressList:
	# Creating Insecure Channel
	mapWorker_channel = channel = grpc.insecure_channel(mapWorkers);
	# Creating Stub-
	mapWorker_stub = Master_pb2_grpc.MapWorkerServiceStub(mapWorker_channel);

	# Calling RPC -
	mapWorker_response = mapWorker_stub.MapWorker(FileLocations);

	print("Recieved Response:");
	for file in mapWorker_response.fileLocation:
		print(file);





# STEP 1 : Spliting the Data from Input Location






