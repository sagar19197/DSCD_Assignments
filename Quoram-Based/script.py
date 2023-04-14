# GROUP 13 : DSCD ASSIGNMENT
# Script File For Assignment-2

import subprocess
import time

print("\nWELCOME TO QUORAM-BASED PROTOCOL :\n");

print("PLEASE SELECT MODE:");
print("1. NORMAL MODE: This mode contains testcases as per the documents.");
print("2. CUSTOM MODE: In this mode Client will have to enter Inputs. ")


mode = int(input("\n Enter MODE option number: "));

if mode != 1 and mode !=2:
	print("PLEASE ENTER VALID INPUT !! ABORTING");
	exit();


# Taking Input for NR, NW and N
N = 0;
N_r = 0;
N_w = 0;
while(True):
	N = int(input("\nEnter Total Servers (N) : "));
	N_r = int(input("Enter Number of Read Quorams (N_r) : "));
	N_w = int(input("Enter Number of Write Quorams (N_w) : "));
	# Checking Conditions - 
	if (N_w > (N/2)) and ((N_r + N_w) > N):
		break;
	else:
		print("\nERROR : Please Enter Valid set of values for N, N_r and N_w ");



commands = ['python registry_server.py '+str(N)+' '+str(N_r)+' '+str(N_w)];

# Starting N replicas from 5000 ports
for i in range(N):
	port = 5000 + i;
	address = "localhost:" + str(port);
	commands.append('python server.py '+address);


# Get the path of the cmd.exe executable
cmd_path = subprocess.check_output('where cmd.exe').decode().split()[0]

# Open a new command prompt window for each Server and Registry Server
for command in commands:
	process = subprocess.Popen([cmd_path, '/c', 'start', 'cmd', '/k', command]);
	time.sleep(0.1);



# for M Clients -
M = int(input("\nEnter Number of Clients to generate : "));

commands = [];
for i in range(M):
	if mode == 1:
		commands.append('python client.py NORMAL');
	else:
		commands.append('python client.py');
	time.sleep(0.1);

# Open a new command prompt window for each Client
for command in commands:
	process = subprocess.Popen([cmd_path, '/c', 'start', 'cmd', '/k', command]);