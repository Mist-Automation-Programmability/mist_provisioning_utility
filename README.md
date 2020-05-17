# Mist Provisioning Utility
### Fast and easy provisioning of sites and devices from CSV files.
This repository is meant to serve as an example of rapid site and device provisioning/deployment with the Mist API and a starting point for those interested in implementing programmatic workflows. If you choose to use this utility in production, be sure to test thoroughly.

## Installation

1. Clone this repo
2. Install the required libraries using: `pip install -U -r requirements.txt`
3. Create your CSV files based on the examples
4. Get your Mist API token from [https://api.mist.com/api/v1/self/apitokens](https://api.mist.com/api/v1/self/apitokens) (ensure you are already logged in before visiting)
5. Visit the [Google API Console](https://console.developers.google.com) and obtain an API key with rights to the `Geocoding API` and the `Time Zone API`
6. Fill in the required fields in `config.yml`
7. ***COMING SOON*** Build your configuration file interactively using the `config build` arguments
8. ***COMING SOON*** Test your configuration file using the `config test` arguments

## Usage
This script has multiple functions and will continue to grow. Currently only the `provision` command is fully implemented.

### CSV File Format

The CSV files containing sites and devices must be configured appropriately and follow the formats laid out in the examples files (and below). The example files `sites.csv.example` and `devices.csv.example` are shown below.

##### Sites
The sites CSV file requires a name and address, the RF template and site groups are optional. If you do provide either of those items, ensure they match the name in the Mist dashboard exactly. If assigning multiple site groups to a site, enclose them in quotes and separate them with a comma. 
```csv
name,address,rftemplate,sitegroups
SoCal HQ,"23702 Via Lupona, Santa Clarita, CA 91355",US Warehouse,
AMBLER - MAIN OFFICE,"9998 AMBLER AVE, AMBLER AK, 99786",US Office,"US Office,US Warehouse"
ANAKTUVUK PASS - MAIN OFFICE BLDG,"1104 SUMMER ST, ANAKTUVUK PASS AK, 99721",,US Office
ANCHORAGE - EASTCHESTER STATION,"800 INGRA ST, ANCHORAGE AK, 99501",US Office,US Office
```
##### Devices
The devices CSV file requires a hostname, site name, mac address, and serial number. If the device is already claimed to the organization, no claim code is neccessary.
```csv
hostname,site_name,mac,serial,claim_code
SoCal-01,SoCal HQ,5c5b358a960b,100381713023E,
SoCal-02,SoCal HQ,5c5b358a9746,100381713025D,2FYD2PBRKXBB5HL
```
```bash
usage: mist_provisioning.py [-h] [--config CONFIG_FILE] {config,provision} ...

positional arguments:
  {config,provision}    Available actions
    config              Configuration utilities
    provision           Site provisioning options

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG_FILE  Path to the YAML config file (default: ./config.yml)

```

#### `config` Action
***NOT YET IMPLEMENTED***

```bash
usage: mist_provisioning.py [--config CONFIG_FILE] config [-h] [{test,build}]

positional arguments:
  {test,build}  Test or build the configuration file (default: test)

optional arguments:
  -h, --help    show this help message and exit
```

##### `config test` Action
***NOT YET IMPLEMENTED***

```bash
usage: mist_provisioning.py [--config CONFIG_FILE] config [-h] [{test,build}]

positional arguments:
  {test,build}  Test or build the configuration file (default: test)

optional arguments:
  -h, --help    show this help message and exit
```

##### `config build` Action
***NOT YET IMPLEMENTED***

```bash
usage: mist_provisioning.py [--config CONFIG_FILE] config [-h] [{test,build}]

positional arguments:
  {test,build}  Test or build the configuration file (default: test)

optional arguments:
  -h, --help    show this help message and exit
```

#### `provision` Action
Create your CSV files and ensure your configuration file is properly setup before running. If you are loading your configuration and CSV files from another location or name other than the default, use the flag arguments `--config`, `--sites`, and `--devices` to specify their respective locations. 
```bash
usage: mist_provisioning.py [--config CONFIG_FILE] provision [-h] [--sites CSV file] [--devices CSV file]

optional arguments:
  -h, --help          show this help message and exit
  --sites CSV file    Path to the CSV file of sites (default: ./sites.csv)
  --devices CSV file  Path to the CSV file of devices (default: ./devices.csv)

```

## TODO

- Implement `config` actions
    - `test`: Test the existing configuration
    - `build`: Interactively build the configuration file
- Test additional device types (switches) when provisioning
- Implement additional site and device configuration options when provisioning
- Bulk site configuration changes
- Bulk device configuration changes

## License
Licensed under [MIT](LICENSE)

© 2020 Ryan M. Adzima & [Mist, A Juniper Company](https://mist.com)