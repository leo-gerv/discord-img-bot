import docker

client = docker.from_env()

def create_container():
    # create container from leogervoson/discord-img-bot:runner and connect it to discord-img-bot-net network
    container = client.containers.run('leogervoson/discord-img-bot:runner', detach=True, network='discord-img-bot-net')

    return container

