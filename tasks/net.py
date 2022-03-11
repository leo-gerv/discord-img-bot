import logging
from select import select
import socket
import pickle
import time
import runner.net

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

        logging.info(f'Sending data to runner: {str(data)}')
        data_bytes = pickle.dumps(data)
        runner.net.send_bytes(self.sock, data_bytes)
        logging.info('Sent data to runner')
        self.sock.shutdown(socket.SHUT_WR)
        self.sock.settimeout(30)

        result_bytes = runner.net.receive_bytes(self.sock, 30)

        logging.info(f'Loading result [{len(result_bytes)} bytes]')
        try:
            result = pickle.loads(result_bytes)
        except Exception as e:
            logging.info(f'Error: {e}')
            return (False, None, str(e))
        logging.info('Result loaded')

        if result['status'] == 'success':
            logging.info('Success')
            return (True, result['result'], None)
        else:
            logging.info('Error')
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
