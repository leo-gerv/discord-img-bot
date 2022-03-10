import socket
import pickle
from gen import generate_code_str

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('discord-img-bot', 4571))
    s.settimeout(None)

    # receives bytes until the connection is closed
    raw_bytes = bytes()
    while True:
        try:
            raw_bytes += s.recv(1024)
        except ConnectionResetError:
            break

    data = pickle.loads(raw_bytes)
    ret_dict = {}

    try:
        user_code = generate_code_str(data['body'], data['argname'], data['global_name'])
        result = eval(user_code, {data['global_name']: data['array']})
        ret_dict = {'status': 'success', 'result': result}
    except Exception as e:
        ret_dict = {'status': 'error', 'error': str(e)}

    s.send(pickle.dumps(ret_dict))
    s.close()
    exit(0)
