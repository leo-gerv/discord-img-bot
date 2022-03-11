import docker
import os
import time

from .net import get_handle

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

self_container = client.containers.get(os.environ['HOSTNAME'])
client.networks.prune()
bot_network = client.networks.create('discord-img-bot-net', driver='bridge')
bot_network.connect(self_container, aliases=['discord-img-bot'])

def create_container():
    # create container from leogervoson/discord-img-bot:runner and connect it to discord-img-bot-net network
    container = client.containers.run('leogervoson/discord-img-bot:runner-14', detach=True, network=bot_network.id, mem_limit='1g', read_only=True)

    return container

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

        if time.time() - start_time > 15:
            return (False, None)
