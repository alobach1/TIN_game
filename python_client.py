import network 
import sys
import socket


#remove t from received tcp pakiet to catch id client 

n = network.Network(int(sys.argv[1]))
id = n.connect()
n.t1.start()
n.udp_checking(id)
n.t2.start()