# Standard library imports
from typing import AnyStr  # https://docs.python.org/3/library/typing.html?highlight=typing#module-typing
from pathlib import Path  # https://docs.python.org/3/library/pathlib.html?highlight=pathlib#module-pathlib
# External imports
import yaml  # https://pypi.org/project/PyYAML/
from dotted_dict import DottedDict  # https://pypi.org/project/dotted-dict/
# Module imports
from src.logger import create_logger  # Custom logging object


class Config(DottedDict):
    """
    Custom dotted dictionary subclass for automatically reading and writing to/from a YAML file
    Example:
        In [1]: config = Config(filename="config_file.yml")

        In [2]: print(config.mist.api_token)
        Out[2]: 'XXX'

        In [3]: print(config.google.api_token)
        Out[3]: 'YYY'
    """

    file: Path

    def __init__(self, filename: AnyStr, *args, **kwargs):
        """ Config object initialization

        :param AnyStr filename: The path of the file the object will read/write as a string (either relative or absolute)
        :params List args: A list of arguments
        :params Dict kwargs: A dictionary of keyword arguments
        """
        # Create an internal logger object
        self.logger = create_logger()
        # Create a pathlib.Path object and assign it to the internal attribute 'file'
        self.file = Path(filename).expanduser().absolute()
        # Initialize the parent class
        super(Config, self).__init__(*args, **kwargs)
        # Check the file exists and load the data from it
        if self.file.is_file():
            # Try to read the file and catch exceptions
            try:
                with self.file.open() as config_stream:
                    super(Config, self).update(yaml.safe_load(config_stream) or {})
            except Exception as e:
                # Handle generic exceptions
                self.logger.error(f"Error opening file: {e}")
                raise e
        else:
            # Filename is not a file
            raise FileExistsError(f"The file '{filename}' could not be opened.")

    def __getattr__(self, item):
        # Suppress exception when reading an unknown attribute
        try:
            return super().__getattr__(item)
        except AttributeError:
            self.logger.error(f"Attempted to read  unknown attribute '{item}' from config.")
            return None

    def __repr__(self):
        # Return a string representation of the object
        return str(self.__dict__)

    def __str__(self):
        # Return a human-readable description of the object
        x = dict(self.__dict__)
        x.pop('logger')
        x.pop('file')
        return f"<{self.__class__.__name__} objects: {', '.join(x.keys())}>"


# def read_config_file(config_file_path: AnyStr) -> Dict:
#     """Read a given YAML config file and return the values as a dictionary
#
#     :param AnyStr config_file_path: The path of the config file as a string (either relative or absolute)
#     :return Dict: A dictionary containing the values from the YAML file
#     """
#     # Open the config file and catch exceptions
#     try:
#         # Open the config file as read-only
#         with open(config_file_path, 'r') as config_stream:
#             # Read the contents of the config file into a dictionary
#             config_data = yaml.safe_load(config_stream)
#     except (FileExistsError, FileNotFoundError) as e:
#         # Handle file existence exceptions
#         logger.error(f"Error opening config file: {e}")
#         # Re-raise the error
#         raise
#     except (yaml.YAMLError, yaml.MarkedYAMLError) as e:
#         # Handle YAML errors
#         logger.error(f"Unable to parse YAML: {e}")
#         # Re-raise the error
#         raise
#     except Exception as e:
#         # Handle generic exceptions
#         logger.error(f"Unable to open file for writing: {e}")
#         # Re-raise the exception
#         raise
#     # Return the config file data as a dictionary
#     return config_data
#
#
# def write_config_file(config_file_path: AnyStr, config_data: Union[Dict, List]) -> bool:
#     """Create and write or update an existing YAML file with the provided data
#
#     :param AnyStr config_file_path: The path of the config file as a string (either relative or absolute)
#     :param Union[Dict, List] config_data: A dictionary or list containing the configuration data
#     :return bool: A Boolean representing success or failure writing the file
#     """
#     # Create an empty dictionary to hold the config data
#     config = dict()
#     # Open the config file and catch exceptions
#     try:
#         # Open the existing file for reading
#         with open(config_file_path, 'r') as config_stream:
#             # Read the contents of the config file into a dictionary
#             existing_config = yaml.safe_load(config_stream)
#             # Merge the existing config into the new configuration dictionary
#             config.update(existing_config)
#     except (FileExistsError, FileNotFoundError) as e:
#         # File not found, just continue to writing data
#         pass
#     except (yaml.YAMLError, yaml.MarkedYAMLError) as e:
#         # Handle YAML errors
#         logger.error(f"Unable to parse YAML from existing file {config_file_path}: {e}")
#         # Re-raise the error
#         raise
#     except Exception as e:
#         # Handle generic exceptions
#         logger.error(f"Unable to open file {config_file_path} for reading: {e}")
#         # Re-raise the exception
#         raise
#
#     # Merge the new config data into the config dictionary
#     config.update(config_data)
#
#     try:
#         # Open the config file for writing
#         with open(config_file_path, 'w') as config_stream:
#             # Write the data to the file
#             d = yaml.dump(data=config, stream=config_stream)
#     except (FileExistsError, FileNotFoundError) as e:
#         # Handle file existence exceptions
#         logger.error(f"Error opening config file: {e}")
#         # Re-raise the exception
#         raise
#     except (yaml.YAMLError, yaml.MarkedYAMLError) as e:
#         # Handle YAML exceptions
#         logger.error(f"Unable to parse YAML: {e}")
#         # Re-raise the exception
#         raise
#     except Exception as e:
#         # Handle generic exceptions
#         logger.error(f"Unable to open file for writing: {e}")
#         # Re-raise the exception
#         raise
#     # Return True (success) or False (failure)
#     return True
