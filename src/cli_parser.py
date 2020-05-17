# Standard library imports
import argparse  # https://docs.python.org/3/library/argparse.html
from pathlib import Path  # https://docs.python.org/3/library/pathlib.html?highlight=pathlib#module-pathlib
# Module imports
from src import logger
from src.config import Config

__version__ = "v0.1a"


# Build the cli flags/options
def cli_parser() -> argparse.Namespace:
    """ Parse the command-line arguments and return the values.

    :return argparse.Namespace: Namespace object containing the CLI arguments
    """
    # Create the cli parser
    cli = argparse.ArgumentParser(prog="Mist Provisioning Utility",
                                  description="Fast and easy provisioning of sites and devices from CSV files",
                                  epilog="This utility is a work in progress, please visit https://github.com/Mist-Automation-Programmability/mist_provisioning_utility to submit issues.")
    cli.add_argument('-V', '--version',
                     action='version',
                     version=f"%(prog)s {__version__}")
    # Add flag argument for the YAML file containing your Mist API details and store it in the variable 'config_file'
    # If the file does not exist, it will be created
    # Default is "./config.yml"
    cli.add_argument('--config',
                     type=argparse.FileType('r'),
                     default="./config.yml",
                     dest="config_file",
                     help="Path to the YAML config file (default: %(default)s)")
    # Create a subparser for main positional arguments
    subparser = cli.add_subparsers(help="Available actions", dest='action')
    # Create a positional argument for configuration options
    config = subparser.add_parser(name="config",
                                  help="Configuration utilities")
    # Create a positional argument with choices to test or build the configuration file
    # Default is 'test'
    config.add_argument('config_command',
                        const="test",
                        default="test",
                        choices=['test', 'build'],
                        nargs="?",
                        help="Test or build the configuration file (default: %(default)s)")
    # Create a positional argument for site provisioning options
    provision = subparser.add_parser(name="provision",
                                     help="Site provisioning options")
    # Add flag argument to the sites positional argument for the sites csv file
    # Default to "./sites.csv"
    provision.add_argument('--sites',
                           type=argparse.FileType('r'),
                           # default="./sites.csv",
                           metavar="CSV file",
                           required=False,
                           help="Path to the CSV file of sites (default: %(default)s)")
    # Add flag argument to the sites positional argument for the devices csv file
    # Default to "./devices.csv"
    provision.add_argument('--devices',
                           type=argparse.FileType('r'),
                           # default="./devices.csv",
                           metavar="CSV file",
                           required=False,
                           help="Path to the CSV file of devices (default: %(default)s)")
    # Parse the cli arguments into a namespace object and return it
    arguments = cli.parse_args()

    # Convert sites TextIOWrapper file object to pathlib.Path object
    if hasattr(arguments, 'sites') and arguments.sites:
        logger.debug(f"Creating sites CSV path object...")
        sites = Path(arguments.sites.name).expanduser().absolute()
        if sites.is_file() and sites.exists():
            arguments.sites = sites

    # Convert devices TextIOWrapper file object to pathlib.Path object
    if hasattr(arguments, 'devices') and arguments.devices:
        logger.debug(f"Creating devices CSV path object...")
        devices = Path(arguments.devices.name).expanduser().absolute()
        if devices.is_file() and devices.exists():
            arguments.devices = devices

    # Retrieve the configuration and catch exceptions
    try:
        # Create a config object using the config_file argument
        config = Config(filename=arguments.config_file.name)
        # Add the config object to the arguments namespace object
        arguments.config = config
    except Exception as e:
        # Handle generic exceptions
        logger.error(f"Unable to create config object: {e}")
        raise e
    # Return the arguments Namespace object
    return arguments
