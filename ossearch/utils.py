import logging
import ossearch
import docker
import time
from docker.client import DockerClient
from docker.models.volumes import Volume
from docker.models.containers import Container
from typing import Dict, Union


log = logging.getLogger('ossearch')


def load_config() -> Dict[str, str]:
    return {'version': ossearch.VERSION}


def load_database() -> Union[bool, Volume, Container]:
    client = docker.from_env()

    volume = get_volume(client)
    if not volume:
        return False

    container = get_container(client)
    if not container:
        return False

    wait_server(container)

    return container, volume


def get_volume(client: DockerClient) -> Union[bool, Volume]:
    # get volume
    try:
        volume = client.volumes.get('ossearch-data')
        log.info(f'Using volume ossearch-data')
    except docker.errors.NotFound:
        volume = client.volumes.create('ossearch-data', driver='local')
        log.info(f'Created new volume ossearch-data')
    except docker.errors.APIError:
        log.critical('Problem with docker API')
        return False

    return volume


def get_container(client: DockerClient) -> Union[bool, Container]:
    # get container
    try:
        container = client.containers.get('ossearch')
        log.info(f'Database ossearch found')
    except docker.errors.NotFound:
        print(f'Creating ossearch database')
        container = client.containers.run('jeffjerseycow/tinkerpop:3.4.2',
                                          name='ossearch',
                                          mounts=[
                                              docker.types.Mount(target='/data', source='ossearch-data')
                                          ],
                                          detach=True,
                                          ports={'8182/tcp': 8182})
    except docker.errors.APIError:
        log.critical('Problem with docker API')
        return False

    return container


def wait_server(container: Container) -> None:
    # check running
    if container.status != 'running':
        print(f'Starting ossearch database')
        container.start()
        print('Waiting 5 seconds for server to start')
        time.sleep(5)

    return
