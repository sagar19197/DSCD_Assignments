# GROUP 13 : DSCD PROJECT 2023
# File for Master


# Importing Registry server proto -
import Master_pb2;
import Master_pb2_grpc;

# For Spawning - 
import subprocess;

# importing grpc
import grpc;
# For managing directory - 
import os;


#---------------------------------------------------------------------
# SETTING UP

# MASTER ADDRESS -
MASTER_SERVER_ADDRESS = "localhost:8000";

print("\n--------------------------------------------------------------");
print("		WELCOME TO MAP REDUCE FRAMEWORK !!")
print("--------------------------------------------------------------");

print("\n WELCOME MASTER SERVER !! Your address:", MASTER_SERVER_ADDRESS);

while(True):
	print("\n Choose one of the following Applications/Queries:")
	print("\n  1. WORD COUNT ");
	print("  2. INVERTED INDEX");
	print("  3. NATURAL JOIN ");
	type_of_operation = input("\n Enter Option Number (1-3) from above : ");

	if type_of_operation == "1":
		print("\n You have chosen WORD COUNT.");
		break;
	elif type_of_operation == "2":
		print("\n You have chosen INVERTED INDEX.");
		break;
	elif type_of_operation == "3":
		print("\n You have chosen NATURAL JOIN.");
		break;
	else:
		print("\n PLEASE PROVIDE VALID INPUT!!");

print("--------------------------------------------------------------");

number_of_mappers = int(input("\n  Enter M (Number of Mappers) : "));
number_of_reducers = int(input("\n  Enter R (Number of Reducers) : "));
input_data_location = input("\n  Enter INPUT Data Location (Directory) : ");

# Checking Condition for valid directory -
if not os.path.isdir(input_data_location):
	print("ERROR : Please Provide Valid Directory. ABORTING !!");
	exit();

output_data_location = input("\n  Enter OUTPUT Data Location (Directory): ");

# Checking Condition for valid directory -
if not os.path.isdir(output_data_location):
	print("ERROR : Please Provide Valid Directory. ABORTING !!");
	exit();

print("\n--------------------------------------------------------------\n");





#---------------------------------------------------------------------
# STEP 0 : SPAWNING MAPPERS AND REDUCERS - 

mapWorker_addressList = [];
reduceWorker_addressList = [];
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
	spawning_commands.append('python mapWorker.py '+ address+' '+type_of_operation+' '+str(number_of_reducers));


# Spawning Reduce Workers -
for i in range(number_of_reducers):
	# MapWorkers start from 6000 ports
	port = 6000 + i;
	address = "localhost:" + str(port);

	# Adding this Address to mapWorker_addressList
	reduceWorker_addressList.append(address);

	# creating spawning commands - 
	spawning_commands.append('python reduceWorker.py '+ address+' '+type_of_operation);


# Spawning
for run_mapWorkers in spawning_commands:
	subprocess.Popen([cmd_path, '/c', 'start', 'cmd', '/k', run_mapWorkers]);

#--------------------------------------------------------------------



#---------------------------------------------------------------------
# STEP 1 : Spliting the Data from Input Location

input_file_paths = [];

input_file_names = os.listdir(input_data_location);

for input_file_name in input_file_names:
	# Considering only input files - 
	if input_file_name.endswith('.txt'):
		# Storing their Paths 
		input_file_paths.append(os.path.join(input_data_location, input_file_name));

#---------------------------------------------------------------------




#---------------------------------------------------------------------
# STEP 2 : Sending List of Input Locations to assigned to particular Mappers

# Integer Divsion
number_of_files_for_each_atleast = len(input_file_paths) // number_of_mappers;
# Modulus Divsion
number_of_files_left = len(input_file_paths) % number_of_mappers;

print("\n MAP WORKERS INVOCATION STARTS -\n");
input_file_index = 0;
# ITERATING OVER ALL MAPPERS -
for mapWorkers in mapWorker_addressList:

	if (number_of_files_for_each_atleast == 0 and number_of_files_left == 0):
		# No files 
		break;

	print("\nSending Following Input File Locations to MAPWORKER -", mapWorkers,"\n");
	# Creating Variable for storing FileLocations-
	FileLocations = Master_pb2.FileLocations();
	new_location = FileLocations.fileLocation;

	# Iterating over alteast files -
	for i in range(number_of_files_for_each_atleast):
		print(input_file_paths[input_file_index]);
		new_location.append(input_file_paths[input_file_index]);
		input_file_index += 1;

	# Iterating Over extra files
	if (number_of_files_left != 0):
		print(input_file_paths[input_file_index]);
		new_location.append(input_file_paths[input_file_index]);
		input_file_index += 1;
		number_of_files_left -= 1;


	# Sending to MapWorkers - 

	# Creating Insecure Channel
	mapWorker_channel = channel = grpc.insecure_channel(mapWorkers);
	# Creating Stub-
	mapWorker_stub = Master_pb2_grpc.MapWorkerServiceStub(mapWorker_channel);
	# Calling RPC -
	mapWorker_response = mapWorker_stub.MapWorker(FileLocations);

	print("\nRecieved Following File Locations Response: from MAPWORKER - ", mapWorkers,"\n");
	for file in mapWorker_response.fileLocation:
		print(file);










