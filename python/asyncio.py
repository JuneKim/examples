import asyncore
import socket
import time, threading

def checkClient(server):
	print ('checkClient')
	for handler in server.get_handlers():
		handler.add_data("abcd")
		handler.handle_write()
	
	threading.Timer(3, checkClient, args=(server,)).start()
	


class EchoHandler(asyncore.dispatcher_with_send):
	'''
	Event handler to manage s/c communication
	'''
	def __init__(self, sock, address):
		asyncore.dispatcher_with_send.__init__(self, sock)
		self.addr = address
		self.data_to_write = []
	def handle_read(self):
		print ('{}:handle_read'.format(self.addr))
		data = self.recv(8192)
		if data:
			self.data_to_write.insert(0, "result-" + data)
	def handle_write(self):
		print ('handle_write')
		data = self.data_to_write.pop()
		sent = self.send(data[:1024])
	def handle_close(self):
		print ('handle_close')
		self.close()

	def add_data(self, data):
		self.data_to_write.insert(0, data)

class EchoServer(asyncore.dispatcher):
	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(5)
		self.handlers = []

	def handle_accept(self):
	'''
	called when a client requests to connect
	'''
		pair = self.accept()
		if pair is not None:
			sock, addr = pair
			print ('Incomming connection from %s' % repr(addr))
			handler = EchoHandler(sock, addr)
			self.handlers.append(handler)
	
	def add_write_data(self, data):
		for handler in self.handlers:
			handler.add_data(data)
	def get_handlers(self):
		return self.handlers

server = EchoServer('localhost', 11111)
# run a timer to send msg to client
threading.Timer(3, checkClient, args=(server,)).start()
asyncore.loop()
