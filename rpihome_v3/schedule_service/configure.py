#!/usr/bin/python3
""" configure.py:
    Configuration helper functions used to set up this service
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import configparser
import datetime
import sys
if __name__ == "__main__":
    sys.path.append("..")
import cal_service as service
import helpers


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Config Function Def *********************************************************
def configure_log(filename):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Set up application logging
    log = helpers.setup_log_handlers(
        __file__,
        config_file['LOG FILES']['debug_log_file'],
        config_file['LOG FILES']['info_log_file'])
    # Return configured objects to main program
    return log


# Configure service addresses and ports ***************************************
def configure_servers(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Create dict with all services defined in INI file
    service_addresses = {}
    for option in config_file.options('SERVICES'):
        service_addresses[option] = config_file['SERVICES'][option]
    # Return dict of configured addresses and ports to main program
    return service_addresses


# Configure message types *****************************************************
def configure_message_types(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Create dict with all services defined in INI file
    message_types = {}
    for option in config_file.options('MESSAGE TYPES'):
        message_types[option] = config_file['MESSAGE TYPES'][option]
    # Return dict of configured addresses and ports to main program
    return message_types


# Obtain Credentials **********************************************************
def configure_credentials(filename, log):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Read credential info from file
    try:
        credentials = config_file['CREDENTIALS']['file']
        log.debug('Credentails file found')
    except:
        log.error('No credentials file found')
    # Return configured objects to main program
    return credentials


# Configure service socket server *********************************************
def configure_calendar(filename, credentials, log):
    # Define connection to configuration file
    log.debug('Creating configparser connection to [%s]', filename)
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    log.debug('Creating configparser connection to [%s]', credentials)
    cred_file = configparser.ConfigParser()
    cred_file.read(credentials)
    log.debug('Connections established to [%s] and [%s]', config_file, cred_file)
    # Read credential info from file
    try:
        calId = cred_file['GOOGLE']['cal_id']
        log.debug('Setting calendar ID to: [%s]', calId)
        credentialDir = config_file['CALENDAR']['credential_dir']
        log.debug('Setting credential directory to: [%s]', credentialDir)
        clientSecretFile = config_file['CALENDAR']['client_secret_file']
        log.debug('Setting client secret file to: [%s]', clientSecretFile)
    except:
        calId = credentialDir = clientSecretFile = None
    # Create connection to calendar
    if calId is not None:
        calendar = service.GoogleCalSync(
            cal_id=calId,
            credential_dir=credentialDir,
            client_secret=clientSecretFile,
            log=log)
        log.debug('Created calendar object: [%s]', calendar)
    else:
        log.error('Error creating calendar object')
    # Return configured objects to main program
    return calendar