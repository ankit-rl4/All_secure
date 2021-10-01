import socket
host = 'local host'
port = 5000
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('', port))
s.listen(1)
c, addr = s.accept()
print("CONNECTION FROM:", str(addr))
msg=''
while(msg !="close"):
	msg=input("Enter Message :- ")
	c.send(b"{msg}")	 
	msg = "Bye.............."
	c.send(msg.encode())
  
# disconnect the server
c.close()