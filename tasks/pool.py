import struct
from types import coroutine
import docker
import os
import runner.net
import socket
import logging
import pickle
import asyncio
from .utils import js_settimeout

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

self_container = client.containers.get(os.environ['HOSTNAME'])
max_runners = int(os.environ['RUNNERS'])
available_runner_handles = []
in_use_runner_handles = []
loading_containers = int(0)
client.networks.prune()
bot_network = client.networks.create('discord-img-bot-net', driver='bridge')
bot_network.connect(self_container, aliases=['discord-img-bot'])

def create_container():
    # create container from leogervoson/discord-img-bot:runner and connect it to discord-img-bot-net network
    container = client.containers.run('leogervoson/discord-img-bot:runner-20', detach=True, network=bot_network.id, mem_limit='1g', read_only=True)

    return container

class ContainerHandle:
    """ Handle to a container

    Contains a socket and a container object
    """

    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def init(self):
        """ Initialize the handle
        """
        in_bytes = await self.recv_bytes()
        self.container = client.containers.get(in_bytes.decode('utf-8'))

    async def recv_bytes(self):
        """ Receive bytes from the socket
        """

        length = struct.unpack('!I', await self.reader.readexactly(4))[0]
        received_bytes = bytes()

        while len(received_bytes) < length:
            received_bytes += await self.reader.readexactly(length - len(received_bytes))

        return received_bytes

    async def send_bytes(self, data):
        """ Send bytes to the socket
        """

        self.writer.write(struct.pack('!I', len(data)))
        self.writer.write(data)
        await self.writer.drain()

    def kill(self):
        """ Kill the container
        """

        self.container.kill()

class RunnerHandle(ContainerHandle):
    def __init__(self, rd, wr):
        super().__init__(rd, wr)

    async def process(self, data):
        """ Runs the code in the runner

        Return value: (success, result, errmsg)
            success: True if the code was found, False otherwise
            result: the result if success is True, None otherwise
            errmsg: the error message if success is False, None otherwise
        """
        global in_use_runner_handles
        self.running = True

        logging.info(f'Sending data to runner: {str(data)}')
        data_bytes = pickle.dumps(data)
        await super().send_bytes(data_bytes)
        logging.info('Sent data to runner')

        asyncio.get_event_loop().create_task(js_settimeout(10, self.end))

        try:
            result_bytes = await super().recv_bytes()
        except:
            return (False, None, 'Runner timed out')

        asyncio.get_event_loop().create_task(js_settimeout(1, self.end)) # to avoid clogging discord response with blocking docker api calls

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

    async def end(self):
        """ End the runner
        """
        global in_use_runner_handles
        if self.running:
            super().kill()
            self.running = False
            in_use_runner_handles.remove(self)
            await refill_handles()


async def accept_client_cb(reader, writer):
    """ Asyncio callback

    Adds the client to the available_runner_handles list
    """
    global loading_containers
    global available_runner_handles
    global in_use_runner_handles
    logging.info('Accepting runner')
    handle = RunnerHandle(reader, writer)
    await handle.init()
    available_runner_handles.append(handle)
    logging.info('Runner accepted')
    loading_containers -= 1
    

async def refill_handles():
    """ Refill available_runner_handles with handles to containers
    """
    global loading_containers
    global available_runner_handles
    global in_use_runner_handles
    global max_runners
    logging.info('Refilling runner handles')
    logging.info(f'Max runners: {max_runners}, Loading containers: {loading_containers}, Available handles: {len(available_runner_handles)}, In use handles: {len(in_use_runner_handles)}')
    while len(available_runner_handles) + len(in_use_runner_handles) + loading_containers < max_runners:
        logging.info('Creating container')
        create_container()
        loading_containers += 1

def get_handle():
    """ Get a handle to a runner

    Returns:
        handle: a handle to a runner
    """
    global available_runner_handles
    global in_use_runner_handles
    if len(available_runner_handles) == 0:
        return None

    handle = available_runner_handles.pop()
    in_use_runner_handles.append(handle)

    return handle

async def init_container_pool():
    """ Initialize the container pool	
    """
    logging.info('Initializing container pool')
    await asyncio.start_server(accept_client_cb, port=4571, backlog=max_runners)
    await refill_handles()
