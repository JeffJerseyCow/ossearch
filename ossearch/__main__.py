import sys
import logging
from ossearch.build import build_main
from ossearch.parser import get_parser
from ossearch.search import search_main
from ossearch.delete import delete_main
from ossearch.utils import load_config, load_database


log = logging.getLogger('ossearch')


def main() -> bool:
    # load config
    config = load_config()

    # create parser
    parser = get_parser(config)
    args = parser.parse_args()

    # load database
    if args.address == 'localhost' and args.port == 8182:
        container, volume = load_database()
        if not container or not volume:
            log.critical('Cannot start ossearch database')
            return False

    try:
        # select action
        if args.command == 'build':
            return build_main(args)
        elif args.command == 'search':
            return search_main(args)
        elif args.command == 'delete':
            return delete_main(args)
        else:
            parser.print_usage()
            return False

    except KeyboardInterrupt:
        if args.command == 'build':
            print('Database MUST be purged')

        print('Exiting')
        return False


if __name__ == "__main__":
    sys.exit(main())
