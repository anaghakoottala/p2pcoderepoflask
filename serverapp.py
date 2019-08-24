import socket                   # Import socket module

'''def pushf(mainpath,filename):
	
	port = 6000             # Reserve a port for your service.
	s = socket.socket()             # Create a socket object
	host = "10.0.9.53"       # Get local machine name

	s.bind((host, port))            # Bind to the port
	s.listen(2) 
         
	while True:
         
		for f in mainpath:
	
			if f==filename:
				
				conn, addr = s.accept() 
				data = conn.recv(1024)
				conn.send(filename)
				f = open(filename,'rb')
				l = f.read(1024)
				while (l):
					conn.send(l)
					l = f.read(1024)
				f.close()

        	
				conn.close()

'''

def pushf(mainpath,filename):
	port = 6000             # Reserve a port for your service.
	s = socket.socket()             # Create a socket object
	host = "10.0.9.53  "        # Get local machine name
	s.bind((host, port))            # Bind to the port
	s.listen(2)                     # Now wait for client connection.

	print('Server listening....')

	while True:
		conn, addr = s.accept()     # Establish connection with client.
		print ('Got connection from', addr)
		data = conn.recv(1024)
		x=bytes(filename,'utf-8')
		conn.send(x)
		print('Server received', repr(data))
		
		f = open(mainpath+'/'+filename,'rb')
		l = f.read(1024)
		while (l):
			conn.send(l)
			print('Sent ',repr(l))
			l = f.read(1024)
		f.close()

		print('Done sending')
		conn.close()




