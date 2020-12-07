from scipy.io import wavfile
import wave
import numpy as np
import sys
import struct
import os


def getfile():
    filepath = './wav_file'
    name = os.listdir(filepath)
    return name

def wav_binary(wav_path,cfile):
    bfsize = os.path.getsize(cfile)
    fo = open(cfile,'ab+')
    f = open(wav_path, "rb")
    f.seek(0)
    f.read(44)
    data = np.fromfile(f, dtype=np.uint16)
    newdata=[]
    hextxt = "0x{0:x}"
    for dat in data:
        b = (np.uint8) (dat & 0xff)
        txt = hextxt.format(b)
        newdata.append(txt)


    this = [i for i,x in enumerate(newdata) if x=='0x4c']

    for i in this:
        if newdata[i+1] == '0x53':
            num = i-1
            for c in newdata[:num]:
                d = c.split('0x',1)[1]
                y = int(d,16)
                fo.write(struct.pack('B',y))
        else:
            pass   
        
    fo.close()
    f.close()
    
    size = os.path.getsize(cfile)

    if size%4 == 3:
        fo = open(cfile, "ab+")
        a="80"
        b=bytes.fromhex(a)
        c=int(a,16)
        fo.write(struct.pack('B',c))
        fo.close()
        print("start:%d    end:%d" %(bfsize,os.path.getsize(cfile)))
    
    elif size%4 == 2:
        fo = open(cfile, "ab+")
        a="80"
        a1="80"
        b=bytes.fromhex(a)
        b1=bytes.fromhex(a1)
        c=int(a,16)
        c1=int(a1,16)
        fo.write(struct.pack('B',c))
        fo.write(struct.pack('B',c1))
        fo.close()
        print("start:%d    end:%d" %(bfsize,os.path.getsize(cfile)))
    
    elif size%4 == 1:
        fo = open(cfile, "ab+")
        a="80"
        a1="80"
        a2="80"
        b=bytes.fromhex(a)
        b1=bytes.fromhex(a1)
        b2=bytes.fromhex(a2)
        c=int(a,16)
        c1=int(a1,16)
        c2=int(a2,16)
        fo.write(struct.pack('B',c))
        fo.write(struct.pack('B',c1))
        fo.write(struct.pack('B',c2))
        fo.close()
        print("start:%d    end:%d" %(bfsize,os.path.getsize(cfile)))
    elif size%4 == 0:
        print("start:%d    end:%d" %(bfsize,os.path.getsize(cfile)))

if __name__ == "__main__":
    cfile = 'test.bin'
    name = getfile()
    for f in name:
        print(f)
        wav_file = './wav_file/' + f
        wav_binary(wav_file,cfile)
