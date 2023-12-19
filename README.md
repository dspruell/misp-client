# misp-client

misp-client is a simple search client for MISP instances implemented using
the PyMISP API client.

## Installation

The app has been tested on Python 3.

It's best to install the program into a Python virtual environment. The
recommended way to install it is using [pipx](https://pypa.github.io/pipx/):

    pipx install misp-client

It can also be installed using `pip` into a target virtualenv.

    python3 -m pip install misp-client

## Usage

A configuration file must be populated with information about one or more
target MISP instances. In the typical case all that is needed is an instance
URL and API key. Options may be passed to the MISP client by listing them in
the `options` dictionary for a given instance.

A sample configuration file can be copied from `config/dot.misp.yml` and
installed at `$HOME/.misp.yml`. Don't forget to set a restrictive mode on the
file (0600).

The client is currently a work in progress. See `-h/--help` output for help.

### Search

Simply pass a search term as a parameter, and the client outputs brief
information about matching events in all configured MISP instances.

