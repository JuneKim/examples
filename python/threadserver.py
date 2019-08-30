import socket
import threading
import SocketServer
import time
import sys

clients = []

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		#[M6] Need to check whether client's ip is vaild

		data = str(self.request.recv(1024))
		cur_thread = threading.current_thread()
		response = bytes("{}:{}".format(cur_thread.name, data))
		print ("{}:{}".format(cur_thread.name, threading.active_count()))
		self.request.sendall(response)
		print (self.client_address)
		clients.append(self.client_address)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	def __init__(self, server_address, RequestHandlerClass):
		self.clients = []
		self.requests = []
		print ('....init....')
		SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
	def process_request(self, request, client_address):
		print ("clientip:{}".format(client_address))
		self.clients.append(client_address)
		self.requests.append(request)
		SocketServer.TCPServer.process_request(self, request, client_address)
		print (self.clients)
		print (self.requests)

	def send_msg(self, msg):
		self.requests[0].sendall(msg)


class MTDController:
	"""
	MTDController class: forks the thread to run a server which communicates with the trusted hosts.

	"""
	def __init__(self, ip = '127.0.0.1', port = '9999'):
		print ("ip:{},port{}".format(ip, port))
		self.serverip = ip
		self.serverport = port
	
	def run(self):
		self.server = ThreadedTCPServer ((self.serverip, self.serverport), ThreadedTCPRequestHandler)
		ip, port = self.server.server_address
		print ('ip:{}, port:{}'.format(ip, port))
				
		self.server_thread = threading.Thread(target = self.server.serve_forever)
		#thread should be terminated when its parent is closed.
		self.server_thread.daemon = False 
		self.server_thread.start()
	
	def stop(self):
		self.server.shutdown()
		self.server.server_close()

if __name__ == "__main__":
	
	if len(sys.argv) is not 3:
		HOST, PORT = 'localhost', 9999
	else:
		HOST, PORT = sys.argv[1], sys.argv[2]
	
	mtdController = MTDController(HOST, PORT)

	mtdController.run()
	print ('the end')
