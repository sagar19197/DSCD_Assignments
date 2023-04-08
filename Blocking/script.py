# GROUP 13 : DSCD ASSIGNMENT
# Script File For Assignment-2

import subprocess
import time

print("\nWELCOME TO PRIMARY BACKUP BLOCKING PROTOCOL :\n");
print("PLEASE SELECT MODE:");
print("1. NORMAL MODE: This mode contains testcases as per the documents.");
print("2. CUSTOM MODE: In this mode Client will have to enter Inputs. ")

mode = int(input("\n Enter MODE option number: "));

if mode != 1 and mode !=2:
    print("PLEASE ENTER VALID INPUT !! ABORTING");
    exit();

# for N replicas
N = int(input("\nEnter Number of Replicas/Servers : "));

commands = ['python registry_server.py'];

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

