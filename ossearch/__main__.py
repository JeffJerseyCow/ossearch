import sys
import logging
from ossearch.parser import get_parser
from ossearch.utils import load_config
from ossearch.build import build_main
from ossearch.search import search_main
from ossearch.delete import delete_main


log = logging.getLogger('ossearch')


def main() -> bool:
    # load config
    config = load_config()

    # create parser
    parser = get_parser(config)
    args = parser.parse_args()

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
        print('Exiting')
        return False


if __name__ == "__main__":
    sys.exit(main())
