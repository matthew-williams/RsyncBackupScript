#!/usr/bin/env python3
# Title:    Python 3 Backup
# Author:   Matthew Williams
# Date:     9/7/2017
# Latest Update:   9/7/2017
#
# Description: Python script to make backups to /home, /etc, and other directories using rsync in a more user friendly and human readable fashion
#
# ToDo:
# 1. Add runtime flags
# 2. Add menu options to chose what directories to add to backup list
# 3. Add a man page for this command
# 4. Add use section
#
#
# Use:
#
import re # imported for future use
import fileinput # imported for future use
import os
import sys
import platform
import shutil
import subprocess # imported for future use
import logging
import time
import argparse
#
# VARIABLE DEFINITION
#
current_time = time.strftime("%H:%M:%S") # time variable
current_date = time.strftime("%d-%m-%Y") # date variable
script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
dist_name = platform.linux_distribution()[0] # For Linux Distro's store the distribution name
dist_version = platform.linux_distribution()[1] # For Linux Distro's store the version number
current_hostname = platform.node() # get hostname from machine script is ran from
working_dir = script_path + "/linux-backups/" + current_hostname + "_" + current_date + "_backups/"
exclude_path = "'" + script_path + "/exclude'" # exclusion list for rsyc
log_file_path = current_hostname + '_backups_' + dist_name + dist_version + '_' + current_date + '_' + current_time + '.log' # Where the log is being saved
intro_text = """
##################################################################
# Title:    Python 3 Backup
# Author:   Matthew Williams
# Date:     9/7/2017
# Latest Update:   9/7/2017
#
# Description: Python script to make backups to /home, /etc, and other directories using rsync
#
# This script is to be used on the following OS's:
# CentOS 7+
# Ubuntu 16.04+
# OpenSuse Leap 42.2+
# Mint 18.3+
# RHEL 7.3+
# Oracle 7.3
#
# If you are utilizing this script on any other OS you
# accept all risks and responsibilities for any data lost
# or misconfiguration that may occur.
"""
outro_text = "Backups complete. Saved here: " + working_dir
backup_command = "sudo rsync -avz --exclude-from=" + exclude_path + " /home/backups" + working_dir
debug_flag = '' # variable to call when you need to debug
#
# END OF VARIABLE DEFINITION
#

#
# LOGGING DEFINITION
#
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create file handler and set level to debug
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# create stream handler and set level to info then print that stream to console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
formatterstream = logging.Formatter("%(levelname)s - %(message)s")
stream_handler.setFormatter(formatterstream)

# add Handlers to logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
#
# END OF LOGGING DEFINITION
#

#
# ARG PARSE
#
parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('-d', action="store_true", default=False, dest='debug_flag', help='Turn Debugging On - Defaults to false')
parser.add_argument('-b', action="store", dest="b")
parser.add_argument('-c', action="store", dest="c", type=int)
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
#
# END ARG PARSE
#

#
# FUNCTIONS DEFINITION
#
def arguments():
    results = parser.parse_args() #setup pulling results from command line Arguments
    debug_flag = results.debug_flag #pull debug_flag argument from cli
    print parser.parse_args() #print out the arguments from the argparse

def debug():
    global debug_flag
    if debug_flag is True:
        print(intro_text)
        print(working_dir)
        print(debug_flag)
        logger.debug(current_date)
        logger.error(current_time)
        print(exclude_path)
        print(outro_text)
        print("***  " + backup_command + "  ***")
        exit_script(0)
    else:
        print("debug_flag was not True")
        print(debug_flag)
        exit_script(0)

def backup():
    global debug_flag
    if debug_flag is False:
        print(intro_text)
        ### Perform Backups using rsync
        logger.debug("***Backup Started***")
        if os.path.exists('/usr/bin/rsync'): # verify rsync is installed first
            if not os.path.exists(working_dir):
                os.system("sudo mkdir '" + working_dir + "'") # attempt to create directory
            os.system(backup_command)
            print(outro_text)
        else:
            logger.error("***rsync is not available on this OS***") # if it cannot find the QAS install.sh file
        ### Done performing backups

def exit_script(exit_code): # Function to exit script, will build exception handling in the future
    logger.debug("Exiting script.")
    sys.exit(exit_code)

#
# END OF FUNCTIONS DEFINITION
#

#
# PROGRAM DEFINITION
#
arguments()
debug()
#backup()
exit_script(0)
#
# END OF PROGRAM DEFINITION
#
