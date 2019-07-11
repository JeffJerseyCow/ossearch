import os
import argparse
from typing import Dict


def add_build_args(subparser: argparse.ArgumentParser) -> bool:
    buildparser = subparser.add_parser('build')
    buildparser.add_argument('-d', '--directory', type=str, required=True, help='source code directory')
    buildparser.add_argument('-s', '--server', type=str, required=True, help='gremlin server string')
    return True


def add_search_args(subparser: argparse.ArgumentParser) -> bool:
    searchparser = subparser.add_parser('search')
    searchparser.add_argument('-d', '--directories', nargs='+', type=str, required=True,
                              help='source code directories')
    searchparser.add_argument('-s', '--server', type=str, required=True, help='gremlin server string')
    searchparser.add_argument('-t', '--threshold', type=int, default=10, help='threshold percentage for displaying'
                                                                              'matches')
    return True


def add_delete_args(subparser: argparse.ArgumentParser) -> bool:
    delete = subparser.add_parser('delete')
    delete.add_argument('-d', '--directory', type=str, help='source code directories')
    delete.add_argument('-s', '--server', required=True, type=str, help='gremlin server string')
    delete.add_argument('--purge', action='store_true', help='purge entire database')
    return True


def get_parser(config: Dict[str, str]) -> argparse.ArgumentParser:
    # create parser
    parser = argparse.ArgumentParser('ossearch')
    parser.add_argument('--version', action='version', version=f'ossearch {config["version"]}')
    subparser = parser.add_subparsers(dest='command')

    # additional arguments
    add_build_args(subparser)
    add_search_args(subparser)
    add_delete_args(subparser)

    return parser
