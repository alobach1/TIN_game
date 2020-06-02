import struct
import numpy as np



data = b'123'
s = 'cBcB'
p = '1s'
p = s.join(p)
# m = struct.unpack(p+(p)*2,data)
start = 0
n= []
arr = b'Y\x00\x00\xa6\xb8\xe0\xa6\x96\x00'
print(arr[:-4])

'''
while True:
    start = arr.find(b'\x00', start)
    if start == -1:
        break
    n.append(start)
    start += len(b'\x00')
print(n)
print(arr[3:])

for i in range(len(arr)):
    n = arr.find(b'\x00')
    print(n)
    if (n%2)==0 :
        print('chetko')
    else:
        print('niechetki')
print(arr)

print(arr[:-1])
print(str(int(270*255/360)))

splt = arr.decode('utf-8').split('\x00')

print(splt[0].encode())
print(splt[1].encode())


packet = struct.pack('2s',b'-1')
print(packet)
 
#m = struct.unpack('1s B 1s B',packet)
#print(m)


#split
spl = data.split(b'\x00') #xff better 
       
        print(spl)
        print(spl[-1])
        if spl[-1]!=b'':
            o = self.unpack_pr(spl[-1])
        l= len(data) - len(spl[-1])
        print(len(spl[-1]))
        print(len(data))
        print(l)
        print(o)
'''