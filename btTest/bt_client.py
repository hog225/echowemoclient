from bluetooth import *

# Create the client socket
client_socket=BluetoothSocket( RFCOMM )

#
#client_socket.connect(("20:15:01:30:59:85", 1))
client_socket.connect(("20:14:04:11:22:37", 1))

while True:
    msg = raw_input("Send : ")
    print msg
    client_socket.send(msg)


print "Finished"

client_socket.close()
