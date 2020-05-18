#!/usr/bin/env python3
#
# Example script to create sites from a CSV file.
# Required:
#   - Mist API Token: https://api.mist.com/api/v1/self/apitokens
#   - Google API Token w/ access to the Geocoding and Time Zone APIs: https://console.developers.google.com
#
#

# Standard library imports
import sys
# Module imports
from mist import Mist  # Mist object
from src import logger  # Custom logging object
from src import cli_parser  # Function to parse command-line options
from src.provision import provision_sites, provision_devices  # Site and device provisioning functions


# Main function
def main():
    """ Main script orchestration function """
    args = cli_parser()
    if args.action == "config":
        if hasattr(args, 'config_command') and args.config_command == 'test':
            # TODO: Build config test
            logger.warning("Config tester not yet implemented, exiting.")
            return
        elif hasattr(args, 'config_command') and args.config_command == 'build':
            # TODO: Build config builder
            logger.warning("Config builder not yet implemented, exiting.")
            return
    elif args.action == 'provision':
        # Create a Mist object
        try:
            mist = Mist(config=args.config)
        except Exception as exception:
            logger.error(f"Exception: {exception}")
            raise exception

        # Parse sites CSV and create sites if sites CSV file is specified
        if args.sites:
            sites = provision_sites(csv_file=args.sites, mist=mist)
            logger.debug(f"Provisioned sit(s)e: {', '.join([s.name for s in sites])}")

        # Parse devices and create devices if devices CSV file is specified
        if args.devices:
            devices = provision_devices(csv_file=args.devices, mist=mist)
            logger.debug(f"Provisioned device(s): {', '.join([d.name for d in devices])}")


# Only run this section if being run as a script, not imported.
if __name__ == '__main__':
    # Run the main function and catch exceptions
    try:
        logger.info("Starting Mist Provisioning Utility...")
        main()
    except KeyboardInterrupt:
        # Exit cleanly on Ctrl-C
        sys.exit("User cancelled, exiting.")
    except Exception as e:
        # Handle general exceptions
        logger.error(f"Exception caught: {e}")
        logger.error("Exiting due to exception...")
