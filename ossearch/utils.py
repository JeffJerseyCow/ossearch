import logging
import ossearch
from typing import Dict


log = logging.getLogger('ossearch')


def load_config() -> Dict[str, str]:
    return {'version': ossearch.VERSION}
