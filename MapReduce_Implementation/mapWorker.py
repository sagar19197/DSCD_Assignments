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
# FOR handling FIles -
import os;


# MASTER ADDRESS - 
MASTER_SERVER_ADDRESS = "localhost:8000";


# Service for MAPWORKER
class MapWorkerServiceServicer(Master_pb2_grpc.MapWorkerServiceServicer):
	def MapWorker(self, request, context):


		print("Request from MASTER: Recieved Following File Locations:\n");

		FileLocations = Master_pb2.FileLocations();
		new_location = FileLocations.fileLocation;

		for file in request.fileLocation:
			print(file);
			new_location.append(file);

		# Generating Key-values from input
		Input_Key, Input_Value = GenerateKeyValue_wordCount(FileLocations);

		# Calling Map()
		Intermediate_Key, Intermediate_Value = MAP_wordCount(Input_Key, Input_Value);

		# Writting Content to IF - 
		Write_KeyValues(Intermediate_Key, Intermediate_Value, "IntermediateFile");

		# Partitioning  - 
		list_of_partition = PARTITION_wordCount(Intermediate_Key, Intermediate_Value);
		
		print("\n Intermediate FILE PARTITION LOCATIONS: Sending to MASTER\n");
		# Sending it to MASTER - 
		FileLocations = Master_pb2.FileLocations();
		new_location = FileLocations.fileLocation;

		for file in list_of_partition:
			print(file);
			new_location.append(file);


		return FileLocations;




#-----------------------------------------------------------------------
# WORD COUNT FUNCTION DEFINITIONS - 

# Function for Generating Key-Value Pair from input fILES FOR WORD COUNT
def GenerateKeyValue_wordCount(FileLocations):

	Key = [];
	Value = [];

	line_index = 0;
	for input_file_path in FileLocations.fileLocation:

		# Reading files - 
		with open(input_file_path, "r") as file:
			input_file_lines = file.readlines();

		# GENEATING key Value as Line number, content
		for line_content in input_file_lines:
			Key.append(line_index);
			Value.append(line_content.strip());
			line_index += 1;

	print("\n GENERATED KEY VALUE PAIRS FROM INPUT:\n");
	for key,value in zip(Key, Value):
		print(" ",key, ":", value);

	return Key,Value;




# MAP FUNCTION : Takes key value pair as input and generate Key value pair
def MAP_wordCount(Input_Key, Input_Value):

	Key = [];
	Value = [];

	for value in Input_Value:
		# Iterating over Values
		word_list = value.split(" ");
		# FOR EACH WORD IN values
		for word in word_list:
			# LOWERING case the words
			Key.append(word.lower());
			Value.append(1);

	print("\n GENERATED KEY VALUE PAIRS FROM MAP STAGE:\n");
	for key,value in zip(Key, Value):
		print(" ",key, ":", value);

	return Key, Value;


# PARTITION Function: Takes Key, Value as Input and generate R partitions.

def PARTITION_wordCount(Intermediate_Key, Intermediate_Value):

	global number_of_Partitions;
	#Iterating over Each Partitions 
	list_of_partions = [];
	for partition in range(number_of_Partitions):

		# Creating Temp KEY, VALUE-
		Key = [];
		Value = [];
		# Iteratting over all Keys, values
		for key,value in zip(Intermediate_Key, Intermediate_Value):

			# PARTITION CONDITION
			if len(key)%number_of_Partitions == partition:
				Key.append(key);
				Value.append(value);

		print("\n Content of Intermediate File PARTITION", (partition+1),"\n");
		filename = Write_KeyValues(Key, Value, "IntermediateFile_Partition_"+str(partition+1), "Print");
		list_of_partions.append(filename);

	return list_of_partions;





# Function for WRITTIN KEY VALUES to file - 
def Write_KeyValues(Key, Value, File_name, printData = None): 

	global server_dir;

	Content_for_file = "";
	# Iterating - 
	for key,value in zip(Key, Value):
		Content_for_file += str(key) + " : " + str(value)+"\n";

	# Writting - 
	filename = server_dir + "\\"+ str(File_name) + ".txt";
	with open(filename, "w") as file:
		file.write(Content_for_file);

	if printData is not None:
		print(Content_for_file);

	print("\nWritten Intermediate KEY-VALUE in:\n",filename);
	return filename;



# Checking Condition for Usage of this file - 
if len(sys.argv) != 4:
	print("Usage ERROR: Please ENTER address of the server as argument. Usage: python mapWorker.py [address] [OPERATION] [Number of Partitions]");
	exit();


mapWorker_address = sys.argv[1];
mapWorker_operation = sys.argv[2];
number_of_Partitions = int(sys.argv[3]);


# Creating directories for storing files 
server_dir = os.path.join(os.getcwd(), "Files");

# If Files Directory not exists
if not os.path.exists(server_dir):
	os.mkdir(server_dir);

server_dir = os.path.join(server_dir, "MAP_WORKER_"+mapWorker_address[10:]);
# If Server Directory not exists
if not os.path.exists(server_dir):
	os.mkdir(server_dir);



print("\n WELCOME MapWorker SERVER, Your address:", mapWorker_address,"\n");

# SETTING UP THE mapWorker Servers -
mapWorker_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10));

# Adding Services - 
Master_pb2_grpc.add_MapWorkerServiceServicer_to_server(MapWorkerServiceServicer(), mapWorker_server);

# adding insecure port - 
mapWorker_server.add_insecure_port(mapWorker_address);
mapWorker_server.start();

mapWorker_server.wait_for_termination();
