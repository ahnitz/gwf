# Copyright (C) 2016 Alex Nitz
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import struct, numpy

class FrVector(object):
    """ Keep track of frame vector information """
    vtypes = {0:numpy.char,
              1:numpy.int16,
              2:numpy.float64,
              3:numpy.float32,
              4:numpy.int32,
              5:numpy.int64,
              6:numpy.complex64,
              7:numpy.complex128,
              8:numpy.str,
              9:numpy.uint16,
             10:numpy.uint32,
             11:numpy.uint64,
             12:numpy.char,
             }

    def __init__(self, f, frame):
        """ Populate using a file pointer starting at the FrVector header """
        self.channel = get_string(f)
        self.compression, = struct.unpack("=H", f.read(2))
        self.frame = frame
        
        vector_class, = struct.unpack("=H", f.read(2))
        self.samples, = struct.unpack("=Q", f.read(8))
        self.nbytes, = struct.unpack("=Q", f.read(8))
        self.read_loc = f.tell()
        
        f.seek(self.nbytes, 1)
        self.ndim, = struct.unpack("=L", f.read(4))
        self.shape = struct.unpack("=" + "Q" * self.ndim, f.read(8 * self.ndim))
        self.dx = struct.unpack("d" * self.ndim, f.read(self.ndim * 8)) 
        self.dtype = FrVector.vtypes[vector_class]
        
class FrFrame(object):
    def __init__(self, f):
        """ Populate frame info from file pointer"""
        name = get_string(f)
        f.seek(12, 1)
        self.sec, self.nsec = struct.unpack('=LL', f.read(8))
        f.seek(2, 1)
        self.duration = int(struct.unpack('d', f.read(8))[0])

def get_string(f):
    """Read string from the file """
    length, = struct.unpack('H', f.read(2)) 
    length = length - 1
    txt = ''.join(struct.unpack('%sc' % length, f.read(length)))
    f.seek(1, 1) # There is a null at the end
    return txt

def index_file(f):
    """ Make an index of where vectors are stored with the file
    """
    record_vec = False
    record_head = False

    # skip the file header
    f.seek(40)
    fmt = "=QBBL"

    previous_cls, cls = 0, 0
    vect_type = head_type = 0

    index = {}

    # Walk through the classes in the file
    # We note only where the frame headers are to get the start time / end time
    # and also where the vectors are for later reading
    while 1:
        next = f.tell()
        previous_cls = cls
        size, _, cls, _ = struct.unpack(fmt, f.read(14))

        if cls == 1:
            txt = get_string(f)
            if txt == 'FrEndOfFile':
                break
            elif txt == 'FrVect':
                record_vec = True 
            elif txt == 'FrameH':
                record_head = True

        if record_head and previous_cls == 2 and cls != 2:
            head_type = cls
            record_head = False
        elif record_vec and previous_cls == 2 and cls != 2:
            vect_type = cls
            record_vec = False

        # We've found a class we understand so pull the metadata
        if cls == vect_type:
            vec_info = FrVector(f, frame_info)

            if vec_info.channel not in index:
                index[vec_info.channel] = []

            index[vec_info.channel].append(vec_info)                

        elif cls == head_type:
            frame_info = FrFrame(f)

        next += size
        f.seek(next)
    return index

class File(object):
    def __init__(self, filename):
        self.f = open(filename, 'rb')
        self.index = index_file(self.f)

    def channels(self):
        return self.index.keys()

    def close(self):
        self.f.close()

