#!/usr/bin/python3
""" configure.py:
    Configuration process for the RPiHome application.
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
import asyncio
import copy
import configparser
import datetime
import typing
import mysql.connector
import mysql.connector.errorcode as errorcode
from .log_support import setup_log_handlers
import rpihome_v3


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
def configure_logger(filename):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Set up application logging
    logger = setup_log_handlers(
        __file__,
        config_file['LOG FILES']['debug_log_file'],
        config_file['LOG FILES']['info_log_file'])
    # Return configured objects to main program
    return logger


# Config Database Connection Function *****************************************
def configure_database(filename, logger):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Set up database connection
    try:
        database = mysql.connector.connect(
            host=config_file['DATABASE']['host'],
            port=config_file['DATABASE']['port'],
            database=config_file['DATABASE']['schema'],
            user=config_file['DATABASE']['user'],
            password=config_file['DATABASE']['password'])
        logger.debug("Successfully connected to database")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            database = None
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            database = None
        else:
            database = None
        pass
        logger.debug("Could not connect to database")
    # Return configured objects to main program
    return database


# Config Automation Device List Function **************************************
def configure_device(filename, logger):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Create list of automation devices defined in config.ini file
    devices = []
    logger.debug('Begining search for device configuration in config file')
    for i in range(1, 50, 1):
        try:
            if len(str(i)) == 1:
                device_id = 'device0' + str(i)
            elif len(str(i)) == 2:
                device_id = 'device' + str(i)
            devices.append(rpihome_v3.Device(
                config_file['DEVICES'][device_id + '_name'],
                config_file['DEVICES'][device_id + '_devtype'],
                config_file['DEVICES'][device_id + '_address'],
                'None',
                '',
                str(datetime.datetime.now())
                ))
            print('got this far')
            logger.debug(
                'Device %s added to automation device list',
                (config_file['DEVICES'][device_id + '_name']))
        except:
            pass
    logger.debug('Completed automation device list: %s', str(devices))
    # Return configured objects to main program
    return devices


# Config Google Calendar Connection *******************************************
def configure_calendar(filename, logger):
    # Define connection to configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filename)
    # Read credential info from file
    credentials = rpihome_v3.Credentials(
        config_file['CALENDAR']['username'],
        config_file['CALENDAR']['password'])
    logger.debug('Credentails obtained from INI file')
    # Return configured objects to main program
    return credentials


# Run all configuration functions in-turn *************************************
def configure_all(filename):
    """ Gather application configuration data from config.ini file """
    logger = configure_logger(filename)
    database = configure_database(filename, logger)
    devices = configure_device(filename, logger)
    credentials = configure_calendar(filename, logger)
    logger.debug('Finished call to configuration function')
    # Return results to main program
    return (logger, database, devices, credentials)
