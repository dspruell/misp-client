"""A simple MISP API search client wrapper."""

import argparse
import json
import logging
from pathlib import Path

from tabulate import tabulate
from pymisp.exceptions import PyMISPError
from yaml import load as yaml_load
try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from .const import ALL_INSTANCES
from .misp import (
    init_misp, MISPClientConfigError, MISPClientNoSuchInstanceError
)
from .wrappers import *


DEFAULTS = {"config_path": "~/.misp.yml", "instance": ALL_INSTANCES}

LOG_LEVELS = ("critical", "error", "warning", "info", "debug")
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(module)s:%(funcName)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    desc = "Query and interact with MISP instance(s)"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-c",
        "--config",
        default=DEFAULTS["config_path"],
        help="configuration file path (default: %(default)s)",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        choices=LOG_LEVELS,
        default="warning",
        help="set logging level (default: %(default)s)",
    )
    parser.add_argument(
        "-n",
        "--no-abort",
        action="store_true",
        help="do not abort when an instance encounters a failure",
    )
    parser.add_argument(
        "-w",
        "--show-warnings",
        action="store_true",
        help="do not suppress warnings from internal modules",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="enable debug verbosity for all modules",
    )

    subparsers = parser.add_subparsers()

    parser_search_desc = "search for matching events"
    parser_search = subparsers.add_parser(
        "search",
        help=parser_search_desc,
        description=parser_search_desc.capitalize(),
    )
    parser_search.add_argument(
        "-i",
        "--instance",
        default=DEFAULTS["instance"],
        help="instance name to query (default: %(default)s)",
    )
    parser_search.add_argument(
        "-t",
        "--show-terms",
        action="store_true",
        help="include matching search terms in output",
    )
    parser_search.add_argument(
        "-j",
        "--dump-json",
        action="store_true",
        help="output raw search result data as JSON",
    )
    parser_search.add_argument(
        "terms",
        nargs="+",
        metavar="TERM",
        help="term/attribute for which to search",
    )
    parser_search.set_defaults(func=search_events)

    parser_get_event_desc = "retrieve specified event from instance"
    parser_get_event = subparsers.add_parser(
        "get",
        help=parser_get_event_desc,
        description=parser_get_event_desc.capitalize(),
    )
    parser_get_event.add_argument("instance", help="instance name to query")
    parser_get_event.add_argument("event", type=int, help="event ID to fetch")
    parser_get_event.add_argument(
        "-j",
        "--dump-json",
        action="store_true",
        help="output raw result data as JSON",
    )
    parser_get_event.set_defaults(func=get_event)

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(args.log_level.upper())

    # Suppress warnings from SSL cert validation errors in any instances
    if not (args.show_warnings or args.debug):
        import urllib3

        urllib3.disable_warnings()

    with open(Path(args.config).expanduser(), "rb") as f:
        config = yaml_load(f, Loader=SafeLoader)
    logger.debug("configuration object: %s", config)

    try:
        args.func(config, args)
    except MISPClientConfigError as e:
        if args.no_abort:
            logger.warning(e)
        else:
            parser.error(e)
    except MISPClientNoSuchInstanceError as e:
        parser.error(e)
