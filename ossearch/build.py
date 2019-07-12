import os
import socket
import logging
from argparse import Namespace
from ossearch.node import Node
from ossearch.dbio import GraphTree
from ossearch.fileio import check_directory, walk_directory


log = logging.getLogger('ossearch')


def build_main(args: Namespace) -> bool:
    gt = GraphTree()

    server = f'{args.address}:{args.port}'
    try:
        gt.connect(server)
    except ConnectionRefusedError:
        log.critical(f'Cannot connect to server {server}')
        return False
    except socket.gaierror:
        log.critical(f'Cannot parse server string {server}')
        return False
    log.info(f'Connected to database {server}')

    # check directory exists
    path = os.path.realpath(args.directory)
    if not check_directory(path):
        log.critical('Cannot build database')
        return False

    # check root node exists
    if gt.set_root(Node(name=path, path=path)):
        log.error(f'Root node {path} already exists in database')
        return False

    # add nodes to database
    print('Creating vertices')
    vertices = {}
    for node in walk_directory(path, args.include_bad):
        n = Node(name=node['name'], path=node['path'], parent=node['parent'], type=node['type'],
                 digest=node['digest'])

        if args.verbose:
            print(f'Adding {n.get_path()}')

        # collect vertices
        vertices[n.get_path()] = (gt.add_node(n), n.get_parent(), n.get_path() == path)

    # add edges
    print('Adding edges')
    gt.add_edges(vertices)

    print(f'Successfully created tree {path}')
    return True
