import struct 
import crypt
    # parsing received udp message
def unpackeging(l,data):
    #data = crypt.decrypt_symmetric(data,key)
    data = data[:-4]
    pack = 0
    number_player = 0
    strct = '1s 2s 1s 1s 2s 2s ' 
    s = '1s 1s 2s 2s' 
    o = '1s'
    print(data)
    l = len(data)
    data, l , o , number_pr = searching(data, l , o)
        
    if(l==10):
        s = struct.Struct(strct+o)
            # d ,nr ,i, x, y = s.unpack(data)
            # i = int.from_bytes(i, byteorder='big')
        number_player = 1
        pack = s.unpack(data)
    if(l==16):
        number_player = 2
        s = struct.Struct(strct +s + o) #+o
        pack = s.unpack(data) 
    if(l == 22):
        number_player = 3
        s = struct.Struct(strct + (s)*2 + o) #+o
        pack = s.unpack(data)
    if (l == 28):
        number_player = 4
        s = struct.Struct(strct + (s)*3 + o) #+o
        pack = s.unpack(data)
    if (l == 34):
        number_player = 5
        s = struct.Struct(strct + (s)*4 + o) #+o
        pack = s.unpack(data)
    if (l == 40):
        number_player = 6
        s = struct.Struct(strct + (s)*5 + o) #+o
        pack = s.unpack(data)
    if (l == 46):
        number_player = 7
        s = struct.Struct(strct + (s)*6 + o) #+o
        pack = s.unpack(data)
    if (l == 52):
        number_player = 8
        s = struct.Struct(strct + (s)*7 + o) #+o
        pack = s.unpack(data)
    return pack, number_player, number_pr

    # convert bytes to int    
def b_int(i):
    i = int.from_bytes(i, byteorder='big')
    return i

def unpack_pr(data):
    # print(data)
    l = len(data)/4
    #print(l)
    number_pr = int(l)
    o = ' 2s 2s'
    o = '1s'+ o*int(l)
        #print(o)
    return o , number_pr

def searching(data, l , o):
    start = 0
    n = []
    while True:
        start = data.find(b'\x00', start)
        if start == -1:
            break
        n.append(start)
        start += len(b'\x00')
    print(n)
    number_pl= 0
    for i in n:
        if (i == 9) or (i == 15) or (i== 21) or (i ==27) or (i == 33) or (i == 39) or (i== 45) or (i == 51):
            o , number_pl= unpack_pr(data[i+1:])
            l = i+1
    return data, l, o , number_pl