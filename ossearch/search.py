import os
import logging
import socket
from argparse import Namespace
from ossearch.dbio import GraphTree
from ossearch.node import Node
from ossearch.fileio import check_directory, walk_files


log = logging.getLogger('ossearch')


def search_main(args: Namespace) -> bool:
    gt = GraphTree()

    # connect to tinkerpop server
    try:
        gt.connect(args.server)
    except ConnectionRefusedError:
        log.critical(f'Cannot connect to server {args.server}')
        return False
    except socket.gaierror:
        log.critical(f'Cannot parse server string {args.server}')
        return False
    log.info(f'Connected to database {args.server}')

    # check directories exists
    for directory in args.directories:
        path = os.path.realpath(directory)
        if not check_directory(path):
            log.critical('Cannot search database')
            return False

    # resolve directory paths
    # iterate each passed directory
    for directory in args.directories:
        path = os.path.realpath(directory)

        # build node list
        file_nodes = [Node(name=node['name'], path=node['path'], parent=node['parent'], type=node['type'],
                      digest=node['digest'])
                      for node in walk_files(path)]

        # get parents
        parents = gt.get_parents(file_nodes)
        if len(parents) < 1:
            print(f'No candidates for {path} found')
            continue

        # get unique parent of all file nodes
        subroots = gt.get_subroots(parents)

        # get matching files
        for subroot in subroots:
            matches, nonmatches = gt.get_subtree_matches(file_nodes, subroot)
            root_path = gt.get_vertex_properties(subroot)['path'][0]

            # percentage of files from directory found in database
            percentage_file_database = len(matches) / (len(matches) + len(nonmatches)) * 100

            # percentage of nodes in database found in file directory
            percentage_database_file = len(matches) / len(file_nodes) * 100

            if percentage_file_database > args.threshold and percentage_database_file > args.threshold:
                print(f'Found candidate {root_path}')
                print(f'\t{percentage_file_database:.2f}% files found in database')
                print(f'\t{percentage_database_file:.2f}% database nodes found directory')
                print(f'\tReference: {path}')

    return True
