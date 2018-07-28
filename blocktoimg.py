#!/usr/bin/env python3
# Distributed under the MIT software license
import binascii, struct, sys
from PIL import Image

def div_roundup(x,y):
    return (x+y-1)//y

f = open(sys.argv[1], 'r')
outfilename = sys.argv[2]
blockdata = binascii.a2b_hex(f.read().strip())

metaheader = struct.pack('>II', len(blockdata), binascii.crc32(blockdata))

data = metaheader + blockdata

pixels=div_roundup(len(data), 4)
width=512 # could be made adaptive...
height=div_roundup(pixels, width)

print('exporting %d×%d to %s' % (width,height,outfilename))

padding_len = width*height*4 - len(data)
data += b'\x00' * padding_len

img = Image.frombytes("RGBA", (width, height), data)
img.save(outfilename)
