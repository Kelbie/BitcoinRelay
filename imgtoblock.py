#!/usr/bin/env python3
# Distributed under the MIT software license
import binascii, struct, sys
from PIL import Image

img = Image.open(sys.argv[1])
outfilename = sys.argv[2]
assert(img.format == 'PNG' and img.mode == 'RGBA')
imgdata = img.tobytes()

metaheader = imgdata[0:8]
(blocksize,crc) = struct.unpack('>II', metaheader)
print('size {:d}×{:d}'.format(img.width, img.height))
print('metaheader:')
print('  size  : {:d}'.format(blocksize))
print('  CRC32 : {:x}'.format(crc))

assert(8+blocksize <= len(imgdata))
blockdata = imgdata[8:8+blocksize]

assert(binascii.crc32(blockdata) == crc)

with open(outfilename, 'w') as f:
    f.write(binascii.b2a_hex(blockdata).decode())
    f.write('\n')
