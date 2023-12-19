"""A simple MISP search client wrapper."""

import json
import logging

from tabulate import tabulate

from .misp import init_misp
from .const import ALL_INSTANCES


__all__ = ["search_events", "get_event"]

logger = logging.getLogger(__name__)


def search_events(config, args):
    "Search specified MISP instances for specified terms"
    instances = (
        config.instances if args.instance == ALL_INSTANCES else [args.instance]
    )

    res_data = []
    for instance in instances:
        # Initialize client with instance
        logger.debug("connecting to instance [%s]...", instance)
        misp = init_misp(config, instance)

        # Store unique matching event IDs and terms for instance
        match_events = {}
        evt_headers = ["Instance", "Date", "ID", "Org", "Attrs", "Event Info"]
        if args.show_terms:
            evt_headers.append("Matches")

        # Search for specified terms
        for t in args.terms:
            logger.debug("querying client [%s] for term %s", instance, t)
            events = misp.search("events", "json", value=t)
            if events:
                if args.dump_json:
                    print(json.dumps(events))
                    continue
                for e in events:
                    evt_data = []
                    event_id = e["Event"]["id"]
                    if not event_id in match_events:
                        evt_data.append(instance)
                        evt_data.append(e["Event"]["date"])
                        evt_data.append(e["Event"]["id"])
                        evt_data.append(e["Event"]["Orgc"]["name"])
                        evt_data.append(e["Event"]["attribute_count"])
                        evt_data.append(e["Event"]["info"])
                        match_events[event_id] = {
                            "event": evt_data,
                            "terms": [],
                        }
                    match_events[event_id]["terms"].append(t)
        for me in match_events:
            evt_row = match_events[me]["event"]
            if args.show_terms:
                evt_row.append(", ".join(match_events[me]["terms"]))
            res_data.append(evt_row)

    if res_data:
        print(tabulate(res_data, headers=evt_headers))


def get_event(config, args):
    "Fetch MISP event from specified instance"

    instance = args.instance
    misp = init_misp(config, instance)

    # Fetch specified event from instance
    event_id = args.event
    logger.debug("querying client [%s] for event %s", instance, event_id)
    event = misp.get_event(event_id)

    if event.get("errors"):
        err = event["errors"]
        msg = (
            f'MISP query returned {err[0]} for {err[1]["name"]} '
            f'({err[1]["message"]})'
        )
        logger.error(msg)
        return

    if args.dump_json:
        print(json.dumps(event))

    # XXX Now process event
    raise NotImplementedError("Plaintext dump is unimplemented, try JSON!")
