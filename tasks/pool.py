import docker
import os
import time
import runner.net
import socket
import logging
import pickle

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

self_container = client.containers.get(os.environ['HOSTNAME'])
client.networks.prune()
bot_network = client.networks.create('discord-img-bot-net', driver='bridge')
bot_network.connect(self_container, aliases=['discord-img-bot'])

sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.bind(('', 4571))
sock_server.listen(5)
sock_server.settimeout(5)

def create_container():
    # create container from leogervoson/discord-img-bot:runner and connect it to discord-img-bot-net network
    container = client.containers.run('leogervoson/discord-img-bot:runner-19', detach=True, network=bot_network.id, mem_limit='1g', read_only=True)

    return container

class ContainerHandle:
    """ Handle to a container

    Contains a socket and a container object
    """

    def __init__(self, sock):
        self.sock = sock
        container_id = runner.net.receive_bytes(self.sock, 30).decode('utf-8')
        self.container = client.containers.get(container_id)

    def kill(self):
        """ Kill the container
        """

        self.container.kill()

class RunnerHandle(ContainerHandle):
    def __init__(self, sock):
        self.sock = sock
        super().__init__(sock)

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
        self.sock.settimeout(10)

        try:
            result_bytes = runner.net.receive_bytes(self.sock, 10)
        except:
            super().kill()
            return (False, None, 'Runner timed out')

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

def assign_handle():
    """ Create a container and return a handle to it

    Can timeout if the container is not ready

    Return value: (success, handle)
        success: True if a handle was found, False otherwise
        handle: the handle if success is True, None otherwise
    """
    ok,handle = get_handle()

    if ok:
        return (True, handle)

    create_container()

    start_time = time.time()

    while True:
        ok, handle = get_handle()
        if ok:
            return (True, handle)

        if time.time() - start_time > 20:
            return (False, None)
