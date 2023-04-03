# GROUP 13 : DSCD ASSIGNMENT
# Script File For Assignment-2

import subprocess

# for N replicas
N = int(input("Enter Number of Replicas/Servers : "));

# Starting Registry Server
commands = ['python registry_server.py'];

# Starting N replicas from 5000 ports
for i in range(N):
    port = 5000 + i;
    address = "localhost:" + str(port);
    commands.append('python server.py '+address);


# For client
# Client contains cases for handling
commands.append('python client.py');



# Get the path of the cmd.exe executable
cmd_path = subprocess.check_output('where cmd.exe').decode().split()[0]

# Open a new command prompt window for each command and run it
for command in commands:
    subprocess.Popen([cmd_path, '/c', 'start', 'cmd', '/k', command])