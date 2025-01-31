"""MISP client initialization."""

import logging

from pymisp import PyMISP
from pymisp.exceptions import PyMISPError


logger = logging.getLogger(__name__)


class MISPClientConfigError(Exception):
    pass


class MISPClientNoSuchInstanceError(Exception):
    pass


def init_misp(config, instance):
    "Return initialized PyMISP client"

    # Handle invalid instance name
    if not instance in config["instances"].keys():
        raise MISPClientNoSuchInstanceError(
            f"instance name {instance} does not exist in the configuration"
        )

    # Initialize client with instance
    logger.debug("connecting to instance [%s]...", instance)
    try:
        misp = PyMISP(
            config["instances"][instance]["url"],
            config["instances"][instance]["api_key"],
            **config["instances"][instance].get("options", {}),
        )
    except KeyError:
        raise MISPClientConfigError(
            f"problem connecting to [{instance}] "
            "MISP (possible configuration issue)"
        )
    except PyMISPError as e:
        raise MISPClientConfigError(
            f"problem connecting to [{instance}] MISP ({e})"
        )
    else:
        misp_ver = misp.misp_instance_version["version"]
        logger.info(
            "initialized client [%s] - server: MISP %s", instance, misp_ver
        )

    return misp
