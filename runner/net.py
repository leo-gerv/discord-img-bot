import struct
import time
import socket

def send_bytes(sock: socket.socket, data: bytes) -> None:
    """ Send bytes to the socket

    To be used with receive_bytes
    """
    sock.sendall(struct.pack('!I', len(data)))
    sock.sendall(data)

def receive_bytes(sock: socket.socket, timeout: float) -> bytes:
    """ Receive bytes from the socket

    To be used with send_bytes
    Return value: bytes, None if timed out
    """
    start_time = time.time()

    length = struct.unpack('!I', sock.recv(4))[0]

    received_bytes = bytes()
    while len(received_bytes) < length:
        received_bytes += sock.recv(length - len(received_bytes))
        if time.time() - start_time > timeout:
            return None

    return received_bytes
    
