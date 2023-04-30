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

		print("Request from MASTER: Recieved Following Intermediate File Locations:\n");

		FileLocations = Master_pb2.FileLocations();
		new_location = FileLocations.fileLocation;
		res = False;
		for file in request.fileLocation:
			print(file);
			if res == True:
				new_location.append(file);
			else:
				output_data_location = file;
				res = True;

		# Shuffling and Sorting -

		# GENERATING KEY,VALUE FROM Intermediate File Locations 
		Intermediate_Key, Intermediate_Value = GenerateKeyValue_wordCount(FileLocations);
		# SORTING -
		Intermediate_Key = sorted(Intermediate_Key);
		print("\n KEY VALUE PAIRS After Sorting:\n");
		for key,value in zip(Intermediate_Key, Intermediate_Value):
			print(" ",key, ":", value);
		# Grouping Together - 
		Grouped_Key = [];
		Grouped_Value = [];
		prev_value = "";
		for key,value in zip(Intermediate_Key, Intermediate_Value):
			if prev_value != key:
				Grouped_Key.append(key);
				Grouped_Value.append([int(value)]);
				prev_value = key;
			else:
				Grouped_Value[-1].append(int(value));

		print("\n KEY VALUE PAIRS After GROUPING:\n");
		for key,value in zip(Grouped_Key, Grouped_Value):
			print(" ",key, ":", value);


		# REDUCE STEP - 
		Final_Key, Final_Value = REDUCE_wordCount(Grouped_Key, Grouped_Value);

		# SAVING OUTPUT OF REDUCE -
		global reduceWorker_address;
		print("\n KEY VALUE PAIRS After REDUCE STAGE:\n");
		filename1 = Write_KeyValues(Final_Key, Final_Value, "reducer_"+reduceWorker_address[10:]+"_output", printData ="PRINT");
		filename2 = Write_KeyValues(Final_Key, Final_Value, "reducer_"+reduceWorker_address[10:]+"_output", directory = output_data_location);
		# Sending it to MASTER - 
		FileLocations = Master_pb2.FileLocations();
		new_location = FileLocations.fileLocation;

		new_location.append(filename1);
		new_location.append(filename2);

		return FileLocations;


#-----------------------------------------------------------------------
# WORD COUNT FUNCTION DEFINITIONS - 

# Function for Generating Key-Value Pair from INTERMEDIATE fILES FOR WORD COUNT
def GenerateKeyValue_wordCount(FileLocations):

	Key = [];
	Value = [];

	for input_file_path in FileLocations.fileLocation:

		# Reading files - 
		with open(input_file_path, "r") as file:
			input_file_lines = file.readlines();

		# GENEATING key Value as WORD, occurence
		for line_content in input_file_lines:
			line_content = line_content.strip();
			line_values = line_content.split(" : ");

			Key.append(line_values[0]);
			Value.append(line_values[1]);

	print("\n KEY VALUE PAIRS FROM Intermediate File PARTITIONS:\n");
	for key,value in zip(Key, Value):
		print(" ",key, ":", value);

	return Key,Value;




# REDUCE FUNCTION: Takes Grouped KEY-VALUES as input and returns Key_value for WORD COUNT
def REDUCE_wordCount(Grouped_Key, Grouped_Value):

	Key = [];
	Value = [];

	for key,value in zip(Grouped_Key, Grouped_Value):
		count = 0;
		# Iterating over all values
		for values in value:
			count+=values;
		# Adding in Key ,value
		Key.append(key);
		Value.append(count);

	return Key, Value;



# Function for WRITTIN KEY VALUES to file - 
def Write_KeyValues(Key, Value, File_name, printData = None, directory = None): 

	global server_dir;

	Content_for_file = "";
	# Iterating - 
	for key,value in zip(Key, Value):
		Content_for_file += str(key) + " : " + str(value)+"\n";

	# Writting - 
	if directory is None:
		filename = server_dir + "\\"+ str(File_name) + ".txt";
	else:
		filename = directory + "\\" + str(File_name) + ".txt";

	with open(filename, "w") as file:
		file.write(Content_for_file);

	if printData is not None:
		print(Content_for_file);

	print("\nWritten FINAL KEY-VALUE in:\n",filename);
	return filename;




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