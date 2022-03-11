import logging
from select import select
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

        logging.info(f'Sending data to runner: {str(data)}')
        data_bytes = pickle.dumps(data)
        self.sock.sendall(data_bytes)
        logging.info('Sent data to runner')
        self.sock.shutdown(socket.SHUT_WR)
        self.sock.settimeout(15)

        time.sleep(10)

        result_bytes = bytes()
        idle_start = None

        while True:
            try:
                ready_rd, _, _ = select([self.sock], [], [], 5)
                if len(ready_rd) > 0 and self.sock.recv(1024, socket.MSG_PEEK):
                    result_bytes += self.sock.recv(1024)
                    logging.info('Received result from runner')
                    idle_start = None
                else:
                    if not idle_start:
                        idle_start = time.time()
                        logging.info('No data from runner - starting timeout')
                    elif time.time() - idle_start > 5:
                        logging.info('Runner timed out')
                        break
            except:
                logging.info('Runner connection closed/timeout')
                break

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
