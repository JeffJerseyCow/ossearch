import logging
import ossearch
from typing import Dict


log = logging.getLogger('ossearch')


def load_config() -> Dict[str, str]:
    return {'version': ossearch.VERSION}


def pretty_print(node: Dict[str, str]) -> None:
    for k, v in node.items():
        print(f'{k}: {v}')
