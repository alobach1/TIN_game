import network 
import sys
import socket


#remove t from received tcp pakiet to catch id client 

n = network.Network(int(sys.argv[1]))
id = n.connect()
# dodac szyfrowanie id clienta
# n.key = szyfrowanie(id)
# wewnatrz watku tcp wyslac key 
# klucz publiczny ?
n.t1.start()
n.udp_checking(id)
n.t2.start()