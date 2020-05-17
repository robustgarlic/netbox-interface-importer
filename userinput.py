import sys
import os
import signal
from getpass import getpass
from colorama import init
from colorama import Fore
import ipaddress


def get_input(prompt=''):
    try:
        line = input(prompt)
    except NameError:
        line = input(prompt)
    return line


def get_credentials():
    """Prompt for and return a username and password."""
    print(Fore.WHITE + '\n' + '*' * 80)
    username = get_input('\n\nEnter Username: ')
    password = None
    while not password:
        password = getpass()
        password_verify = getpass('Retype your password: ')
        if password != password_verify:
            print('Passwords do not match.  Try again.')
            password = None
    return username, password
    
def get_host():
    """Prompt for Hostname to pass on to Netmiko Dictionary"""
    print(Fore.WHITE + '\n' + '*' * 80)
    host_device = input('What is the hostname of the target device?: ')
    host_verify = input('Verify hostname of target device: ')
    if (host_device != host_verify):
        print(Fore.WHITE + '\n' + '*' * 80)
        print('\nHostnames do not match. Rerun Script Again.')
        print(Fore.WHITE + '\n' + '*' * 80)
        sys.exit()
    else:
        return host_device

def get_display_name():
    """
    Prompt for Netbox Device display_name.
    This is super annoying, but this is here because of the nature of how we name
    Master VCs
    """
    print(Fore.WHITE + '\n' + '*' * 80)
    nb_displayname = input('What is the display name for the Netbox Device? : ')
    nb_displayname_v = input('Verify display name for Netbox Device : ')
    if (nb_displayname != nb_displayname_v):
        print(Fore.WHITE + '\n' + '*' * 80)
        print('\nDisplay names do not match. Rerun Script Again.')
        print(Fore.WHITE + '\n' + '*' * 80)
        sys.exit()
    else:
        return nb_displayname


        