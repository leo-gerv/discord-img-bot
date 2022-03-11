import logging
import socket
import pickle
from select import select
from gen import generate_code_str
import time

import numpy
import scipy
from net import *

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(15)
    s.connect(('discord-img-bot', 4571))
    logging.info('Connected to server')

    # receives bytes until the connection is closed
    raw_bytes = receive_bytes(s, 30)

    data = pickle.loads(raw_bytes)
    ret_dict = {}

    try:
        logging.info('Generating code')
        user_code = generate_code_str(data['body'], data['argname'], data['global_name'])
        logging.info(f'Code generated:\n{user_code}')
        loc = {data['global_name']: data['array']}
        exec(user_code, {'np': numpy, 'sp': scipy}, loc)
        result = loc['output']
        logging.info(f'eval success')
        ret_dict = {'status': 'success', 'result': result}
    except Exception as e:
        logging.info(f'Error: {e}')
        ret_dict = {'status': 'error', 'error': str(e)}

    logging.info(f'Sending result to server: {str(ret_dict)}')
    ret_bytes = pickle.dumps(ret_dict)
    logging.info(f'Sending {len(ret_bytes)} bytes')
    send_bytes(s, ret_bytes)
    s.shutdown(socket.SHUT_WR)
    time.sleep(5)
    exit(0)
