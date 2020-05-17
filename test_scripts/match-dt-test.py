

from __future__ import absolute_import, division, print_function


import json #used for inventory file
import userinput    #customer additional inputs
from colorama import init 
from colorama import Fore
import netmiko.ssh_exception
from netmiko import Netmiko
from netmiko import ConnectHandler
from datetime import datetime
import pynetbox
import os
import sys
import signal

#start time for script
start_time = datetime.now()
print(Fore.CYAN + '\nnetbox interface importer initiating....')


##exception stuff
signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


#resets colorama colors#
init(autoreset=True)


netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

## variables called from custom script ##
username, password = userinput.get_credentials()
hostname = userinput.get_host()
nb_dn = userinput.get_display_name()


## reads json dictionary of nodes ##
with open('/home/kerwbstomp/Documents/networkautomationscripts/venv/netbox-interface-importer/inventory.json') as node_file:
    nodes = json.load(node_file)


## function to run commands ##
def command_runner():
    for node in nodes:
        node['username'] = username
        node['password'] = password
        if node['host'] == hostname:
            if node['device_type'] =='juniper_junos':
                print('juniper')
                break
            elif node['device_type'] =='cisco_ios':
                print('cisco')
                break
            elif node['device_type'] =='nokia_sros':
                print('nokia')
                break
            else:
                print(Fore.RED + '\nFAILED TO CONNECT TO: ', node['host'], error)
                print(Fore.RED + '\nNO DEVICE TYPE FOUND FOR: ', node['host'], error)

command_runner()
