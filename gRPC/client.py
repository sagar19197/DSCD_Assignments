# GROUP 13 : DSCD ASSIGNMENT
# File for CLIENT Implementation - 

import grpc

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;

# Importing Server proto
import Server_pb2;
import Server_pb2_grpc;

import uuid;

#Generating client id
client_id = str(uuid.uuid1());
print("\nWELCOME CLIENT USER, YOUR UUID:",client_id);



def GetServerList():

	global client_id;
	print("Fetching List of active Servers from Registry SERVER...\n");
	CHANNEL = grpc.insecure_channel("localhost:8000");
	# ClientStub - 
	CLIENT_STUB =  RegistryServer_pb2_grpc.GetServerListServiceStub(CHANNEL);
	registry_server_request = RegistryServer_pb2.ClientRequest(client_id = client_id);
	registry_server_response = CLIENT_STUB.GetServerList(registry_server_request);

	serverList = registry_server_response.serverList.servers;
	# Printing  information abot servers -
	for server in serverList:
		print(server.name,"-",server.address);



def JoinServer(CHANNEL):

	global client_id;
	print("PROCESSING YOUR REQUEST...\n");
	CLIENT_STUB =  Server_pb2_grpc.JoinServerServiceStub(CHANNEL);
	join_request = Server_pb2.ClientId(client_id = client_id);
	join_response = CLIENT_STUB.JoinServer(join_request);
	print(join_response.response);




def LeaveServer():

	global client_id;
	global CHANNEL;
	print("PROCESSING YOUR REQUEST...\n");
	CLIENT_STUB =  Server_pb2_grpc.LeaveServerServiceStub(CHANNEL);
	leave_request = Server_pb2.ClientId(client_id = client_id);
	leave_response = CLIENT_STUB.LeaveServer(leave_request);
	print(leave_response.response);




def PublishArticle():
	global client_id;
	global CHANNEL;
	print("PROCESSING YOUR REQUEST...\n");

	res = False;
	new_article = Server_pb2.Articles();
	type_of_article = input("Enter TYPE of Article (SPORTS,FASHION,POLITICS):");
	if(type_of_article == "SPORTS"):
		new_article.type_of_article = Server_pb2.Category.SPORTS;
	elif(type_of_article == "FASHION"):
		new_article.type_of_article = Server_pb2.Category.FASHION;
	elif(type_of_article == "POLITICS"):
		new_article.type_of_article = Server_pb2.Category.POLITICS;
	else:
		res = True;

	new_article.author_name = input("ENTER AUTHOR NAME:");
	new_article.content = input("ENTER CONTENT [max 200 characters]:");

	if(res == True):
		print("FAILED, Illegal FORMAT");
	else:	
		CLIENT_STUB =  Server_pb2_grpc.PublishArticleServiceStub(CHANNEL);
		clientID = Server_pb2.ClientId(client_id = client_id);
		publishArticleRequest = Server_pb2.PublishArticleRequest(article = new_article, client_id = clientID);
		publishArticleResponse = CLIENT_STUB.PublishArticle(publishArticleRequest);
		print(publishArticleResponse.response);




server_address = "Not connected";
CHANNEL = grpc.insecure_channel("localhost:8000");



while(True):
	print("-------------------------------------");
	print("Please Enter Number of one of the following options:");
	print("1. GetServerList");
	print("2. JoinServer");
	print("3. LeaveServer");
	print("4. GetArticles");
	print("5. PublishArticles");
	print("6. My Connection");
	print("7. EXIT");

	option = input("\n Enter Option Number : ");
	print("----------------------------------------")
	# Case handling - 
	if option == "1":

		GetServerList();

	elif option == "2":

		server_address = input("Enter Server Address to join that server:");
		if server_address == "localhost:8000":
			print("FAILED, Can not connect Registry SERVER");
			server_address = "Not connected";
		else:
			#iNSECURE CHANNEL
			CHANNEL = grpc.insecure_channel(server_address);
			#joIN SERVER
			JoinServer(CHANNEL);

	
	elif option == "3":

		if (server_address =="Not connected"):
			print("Please join to some server to do this operation.");
		else:
			#leave server
			LeaveServer();
			server_address = "Not connected";


	elif option == "4":

		if (server_address =="Not connected"):
			print("Please join to some server to do this operation.");

	elif option == "5":

		if (server_address =="Not connected"):
			print("Please join to some server to do this operation.");
		else:
			#Publish Article - 
			PublishArticle();

	
	elif option == "6":

		print("You are connected to:", server_address);
		print("\nUse JoinServer to change connections");

	elif option == "7":

		break;

	else:
		print("Invalid Input!! Please Enter again.");
