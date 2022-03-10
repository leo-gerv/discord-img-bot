import docker
import time

from .net import get_handle

client = docker.from_env()

def create_container():
    # create container from leogervoson/discord-img-bot:runner and connect it to discord-img-bot-net network
    container = client.containers.run('leogervoson/discord-img-bot:runner', detach=True, network='discord-img-bot-net')

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

        if time.time() - start_time > 10:
            return (False, None)
