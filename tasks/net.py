import socket
import pickle
import time

sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.bind(('', 4571))
sock_server.listen(5)
sock_server.settimeout(5)

class RunnerHandle:
    def __init__(self, sock):
        self.sock = sock

    def process(self, data):
        """ Runs the code in the runner

        Return value: (success, result, errmsg)
            success: True if the code was found, False otherwise
            result: the result if success is True, None otherwise
            errmsg: the error message if success is False, None otherwise
        """

        data_bytes = pickle.dumps(data)
        self.sock.send(data_bytes)
        self.sock.settimeout(10)

        start_time = time.time()

        result_bytes = bytes()

        while True:
            try:
                result_bytes += self.sock.recv(1024)
            except ConnectionResetError:
                break
            except socket.timeout:
                if time.time() - start_time > 10:
                    # TODO: find a way to kill the container
                    return (False, None, 'Runner timeout')

        result = pickle.loads(result_bytes)

        if result['status'] == 'success':
            return (True, result['result'], None)
        else:
            return (False, None, result['error'])

def get_handle():
    """ Try to get a runner handle

    Return value: (success, handle)
        success: True if a handle was found, False otherwise
        handle: the handle if success is True, None otherwise
    """
    
    try:
        sock, _ = sock_server.accept()
        return (True, RunnerHandle(sock))
    except:
        return (False, None)
