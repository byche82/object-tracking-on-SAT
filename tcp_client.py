import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msg = str(input("Your message"))
#msg = str(msg)
print(msg)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 5)
#server_address = ('192.168.100.36', 5)
print('connecting to %s port %s' % server_address, file=sys.stderr)
sock.connect(server_address)
try:

    # Send data
    #message = 'This is the message.  It will be repeated.\n'
    #print >>sys.stderr, 'sending "%s"' % message
    #sock.sendall(message)
    data = sock.recv(100)
    while len(data) > 0:
        data = sock.recv(100)
        #print >>sys.stderr, 'received "%s"' % data
        print('received "%s"' % data, file=sys.stderr)
        message = 'An applge a day, keeps doctors away.\n'
        #print >>sys.stderr, 'sending "%s"' % message
        print('sending "%s"' % message, file=sys.stderr)
        sock.sendall(message)

finally:
    print('closing socket', file=sys.stderr)
    sock.close()
