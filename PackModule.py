import struct

def packData(body):
    ver = 1
    bodySize = body.__len__()
    cmd = 101
    header = [ver, bodySize, cmd]
    headPack = struct.pack('!3I', *header)
    sendData = headPack + body.encode()
    return sendData
