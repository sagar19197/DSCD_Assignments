# GROUP 13 : DSCD ASSIGNMENT
# File for SERVER Implementation - 

import grpc
from concurrent import futures;

# Importing Registry server proto -
import RegistryServer_pb2;
import RegistryServer_pb2_grpc;

# Importing Server proto
import Server_pb2;
import Server_pb2_grpc;

# FOR DATETIME - 
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp


print("\nWELCOME SERVER, PLEASE ENTER -");
server_name = input("SERVER NAME: ");
server_address = input("SERVER ADDRESS: ");

print("Initiating Connection with Registry SERVER");
channel = grpc.insecure_channel("localhost:8000");
# ServerStub - 
server_stub =  RegistryServer_pb2_grpc.RegisterServiceStub(channel);
registry_server_request = RegistryServer_pb2.ServerRequest(name = server_name, address =server_address);
registry_server_response = server_stub.Register(registry_server_request);
print(registry_server_response.response);



# JOIN SERVER 
class JoinServerServiceServicer(Server_pb2_grpc.JoinServerServiceServicer):
	def JoinServer(self, request, context):
		global MAXCLIENTS;
		global CLIENTELE;

		# Checking condition for joining server - 
		if (len(CLIENTELE) >= MAXCLIENTS):
			return Server_pb2.ServerResponse(response = "FAILED");

		for clients in CLIENTELE:
			if(clients.client_id == request.client_id):
				return Server_pb2.ServerResponse(response = "You have already joined this Server");

		server_msg = f"JOIN REQUEST FROM {request.client_id}";
		print(server_msg);

		new_client = CLIENTELE.add();
		new_client.client_id = request.client_id;
		return Server_pb2.ServerResponse(response = "SUCCESS");



# LEAVE SERVER - 
class LeaveServerServiceServicer(Server_pb2_grpc.LeaveServerServiceServicer):
	def LeaveServer(self, request, context):
		global CLIENTELE;
		res = False;
		i = 0;
		for clients in CLIENTELE:
			if(clients.client_id == request.client_id):
				res = True;
				break;
			else:
				i = i+1;
		if (res):
			del CLIENTELE[i];
			server_msg = f"LEAVE REQUEST FROM {request.client_id}";
			print(server_msg);
			return Server_pb2.ServerResponse(response = "SUCCESS");
		else:
			return Server_pb2.ServerResponse(response = "FAILED");



# PUBLISH ARTICLES - 
class PublishArticleServiceServicer(Server_pb2_grpc.PublishArticleServiceServicer):
	def PublishArticle(self, request, context):
		global CLIENTELE;
		global All_Articles;
		#Checking for EXISTENCE in CLIENTELE
		res = False;
		for clients in CLIENTELE:
			if(clients.client_id == request.client_id.client_id):
				res = True;
				break;
		
		if(res == False):
			return Server_pb2.ServerResponse(response = "FAILED");
		else:
			if (request.article.author_name == "") or (request.article.content=="") or (len(request.article.content) > 200):
				return Server_pb2.ServerResponse(response = "FAILED, Illegal Format");
			else:
				new_article = All_Articles.add();
				new_article.type_of_article = request.article.type_of_article;
				new_article.author_name = request.article.author_name;
				new_article.content = request.article.content;
				timestamp = Timestamp();
				timestamp.FromDatetime(datetime.now());
				new_article.time_of_publish.CopyFrom(timestamp);
				server_msg = f"ARTICLE PUBLISHED FROM {request.client_id.client_id}";
				print(server_msg);
				return Server_pb2.ServerResponse(response = "SUCCESS");







# Setting MAX_CLIENTS 
MAXCLIENTS = 10;
# CLIENTELE 
CLIENTELE = Server_pb2.CLIENTELE().clients;
# ALL ARTICLES LIST - 
All_Articles = Server_pb2.All_Articles().articleList;


if (registry_server_response.response == "SUCCESS"):
	
	# Server info  -
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10));
	
	# Adding services -
	Server_pb2_grpc.add_JoinServerServiceServicer_to_server(JoinServerServiceServicer(), server);
	Server_pb2_grpc.add_LeaveServerServiceServicer_to_server(LeaveServerServiceServicer(), server);
	Server_pb2_grpc.add_PublishArticleServiceServicer_to_server(PublishArticleServiceServicer(), server);

	# Adding insecure port - 
	server.add_insecure_port(server_address);
	server.start();
	print("\nSERVER STARTED SUCCESSFULLY !!");
	server.wait_for_termination();


