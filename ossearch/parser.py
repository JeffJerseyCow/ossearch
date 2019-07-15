import argparse
from typing import Dict


def add_build_args(subparser: argparse.ArgumentParser) -> bool:
    buildparser = subparser.add_parser('build')
    buildparser.add_argument('-d', '--directory', type=str, required=True, help='source code directory')
    buildparser.add_argument('-a', '--address', type=str, default='localhost', help='gremlin server address')
    buildparser.add_argument('-p', '--port', type=int, default=8182, help='gremlin server port')
    buildparser.add_argument('--include-bad', action='store_true', help='include bad files such as empty')
    buildparser.add_argument('--verbose', action='store_true', help='increase verbosity')
    return True


def add_search_args(subparser: argparse.ArgumentParser) -> bool:
    searchparser = subparser.add_parser('search')
    searchparser.add_argument('-d', '--directories', nargs='+', type=str, required=True,
                              help='source code directories')
    searchparser.add_argument('-a', '--address', type=str, default='localhost', help='gremlin server address')
    searchparser.add_argument('-p', '--port', type=int, default=8182, help='gremlin server port')
    searchparser.add_argument('-t', '--threshold', type=int, default=10, help='threshold percentage for displaying'
                                                                              'matches')
    searchparser.add_argument('--include-bad', action='store_true', help='include bad files such as empty')
    return True


def add_delete_args(subparser: argparse.ArgumentParser) -> bool:
    deleteparser = subparser.add_parser('delete')
    deleteparser.add_argument('-d', '--directory', type=str, help='source code directories')
    deleteparser.add_argument('-a', '--address', type=str, default='localhost', help='gremlin server address')
    deleteparser.add_argument('-p', '--port', type=int, default=8182, help='gremlin server port')
    deleteparser.add_argument('--purge', action='store_true', help='purge entire database')
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
