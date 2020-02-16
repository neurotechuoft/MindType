import struct 


def get_channel_data(literal_read, scaling, channels, scale_factor):
    cdef double channel_data[8] # 8 channels
    cdef unsigned int c
    cdef int read_value
    # cdef .....
    log_bytes_in = ''

    unpacked = struct.unpack('24B', literal_read)

    for c in range(channels):

        # 3-byte ints
        log_bytes_in = log_bytes_in + '|' + str(literal_read[3*c:3*(c + 1)])

        # 3-byte int in 2's complement
        if unpacked[3*c] > 127:
            pre_fix = b'\xff'
        else:
            pre_fix = b'\x00'

        # unpack little endian(>) signed integer(i) (makes unpacking platform independent)
        read_value = struct.unpack('>i', pre_fix + literal_read[3*c:3*(c + 1)])[0]

        # myInt is data for individual channel -- added to channel_data in channel order
        if scaling:
            channel_data[c] = read_value * scale_factor
        else:
            channel_data[c] = read_value

    return channel_data #, log_bytes_in


def get_aux_data(literal_read, scaling, channels, scale_factor):
    cdef double aux_data[3] # 3 channels
    cdef unsigned int a
    cdef int acc
    log_bytes_in = ''

    for a in range(channels):

        # short = h
        acc = struct.unpack('>h', literal_read[2*a : 2*(a+1)])[0]
        log_bytes_in = log_bytes_in + '|' + str(acc)

        if scaling:
            aux_data[a] = acc * scale_factor
        else:
            aux_data[a] = acc
            
    return aux_data #, log_bytes_in



