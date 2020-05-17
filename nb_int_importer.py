

from __future__ import absolute_import, division, print_function


import json #used for inventory file
import userinput    #customer additional inputs
from colorama import init #make TUI pretty
from colorama import Fore #make TUI pretty
import netmiko.ssh_exception
from netmiko import Netmiko
from netmiko import ConnectHandler
from datetime import datetime
import pynetbox #netbox api libray 
import os
import sys
import signal

#header
script_header = '''

# ┌───────────────────────────────────────────────────────────────────┐
# │                     netbox interface importer                     |          
# ├───────────────────────────────────────────────────────────────────┤
# │ Python script to utilizing netmiko and ntc-templates(Text-FSM) to │
# │ pull interface data and import into netbox via the pynetbox       |
# │ library. Check requirements.txt for all libraries.                |                     
# └───────────────────────────────────────────────────────────────────┘

'''


#start time for script
start_time = datetime.now()

#intializing....
print(Fore.WHITE + script_header)
print(Fore.CYAN + '\nnetbox interface importer initiating....')
print(Fore.CYAN + '\nKeyboardInterrupt: Ctrl-C')

##exception stuff
signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


#resets colorama colors#
init(autoreset=True)


netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

## variables called from custom script - userinput.py ##
username, password = userinput.get_credentials()
hostname = userinput.get_host()
nb_dn = userinput.get_display_name()


## reads json dictionary file for nodes ##
with open('/YOUR/DIRECTORY/HERE/netbox-interface-importer/inventory.json') as node_file:
    nodes = json.load(node_file)


## function to run commands ##
def command_runner():
    for node in nodes:
        node['username'] = username
        node['password'] = password
        if node['host'] == hostname:                    #matches userinput host with JSON object, then matches device_type object to run specific commands for the OS
            if node['device_type'] =='juniper_junos':   
                try:
                    print(Fore.WHITE + '\n' + '=' * 80)
                    print(Fore.CYAN + 'CONNECTING TO DEVICE:' + Fore.WHITE+ node['host'])
                    net_connect = Netmiko(**node)
                    command = 'show interfaces'
                    interfaces = net_connect.send_command(command, use_textfsm=True)    #text-fsm template must exist for command 
                    user_message = (Fore.MAGENTA + "\nRUNNING COMMANDS: " + Fore.WHITE + command.strip())
                    print('\n' + user_message)
                    int_data = (json.dumps(interfaces, indent=2))   #turns command output string into JSON
                    print(Fore.MAGENTA + '\nRETURNED INTERFACE DATA IN JSON FORMAT SUCCESFULLY FOR: ')
                    print(Fore.WHITE + hostname)
                    return int_data
                    net_connect.disconnect()
                except netmiko_exceptions as error:
                    print('\n' * 2)
                    print(Fore.RED +'Failed to ', node['host'], error)
                    print('\n' * 2)
                    sys.exit()
            elif node['device_type'] =='cisco_ios':
                try:
                    print(Fore.WHITE + '\n' + '=' * 80)
                    print(Fore.CYAN + 'CONNECTING TO DEVICE:' + Fore.WHITE+ node['host'])
                    net_connect = Netmiko(**node)
                    command = 'show interfaces'
                    interfaces = net_connect.send_command(command, use_textfsm=True)    #text-fsm template must exist for command
                    user_message = (Fore.MAGENTA + "\nRUNNING COMMANDS: " + Fore.WHITE + command.strip())
                    print('\n' + user_message)
                    int_data = (json.dumps(interfaces, indent=2))   #turns command output string into JSON 
                    print(Fore.MAGENTA + '\nRETURNED INTERFACE DATA IN JSON FORMAT SUCCESFULLY FOR: ')
                    print(Fore.WHITE + hostname)
                    return int_data
                    net_connect.disconnect()
                except netmiko_exceptions as error:
                    print('\n' * 2)
                    print(Fore.RED +'Failed to ', node['host'], error)
                    print('\n' * 2)
                    sys.exit()
            elif node['device_type'] =='alcatel_sros':
                try:
                    print(Fore.WHITE + '\n' + '=' * 80)
                    print(Fore.CYAN + 'CONNECTING TO DEVICE:' + Fore.WHITE+ node['host'])
                    net_connect = Netmiko(**node)
                    command = 'show port description' #working on this text-fsm template - please hold on
                    interfaces = net_connect.send_command(command, use_textfsm=True) #text-fsm template must exist for command
                    print(Fore.MAGENTA + "\nRUNNING COMMANDS: " + Fore.WHITE + command.strip())
                    print('\n')
                    int_data = (json.dumps(interfaces, indent=2))   #turns command output string into JSON
                    print(Fore.MAGENTA + '\nRETURNED INTERFACE DATA IN JSON FORMAT SUCCESFULLY FOR: ')
                    print(Fore.WHITE + hostname)
                    return int_data
                    net_connect.disconnect()
                except netmiko_exceptions as error:
                    print('\n' * 2)
                    print(Fore.RED +'Failed to ', node['host'], error)
                    print('\n' * 2)
                    sys.exit()
            else:
                print(Fore.RED + '\nFAILED TO CONNECT TO: ', node['host'])
                print(Fore.RED + '\nNO DEVICE TYPE FOUND OR INCORRECT FOR: ', node['host'])

        

### NETBOX FUNCTIONS BELOW ###

# generate API token at https://netbox.mydomain.com/user/api-tokens
nb = pynetbox.api(url='http://10.6.6.104:80', token='YOUR TOKEN HERE')



# Checks if device already exists in netbox, device must already be created.
def netbox_device():
    # Perform GET to get device name
    # See if device exists based on userinput,  if not error out. The Try and If statement seems redundant - will circle back on this
    try:
        nb_device = nb.dcim.devices.get(name=nb_dn)
    except Exception as error:
        print(Fore.RED + '\nSOMETHING WENT WRONG, THE DEVICE NAME WAS NOT FOUND IN NETBOX, YOU ENTERED: ' + Fore.WHITE + '{}'.format(nb_dn))
        print(Fore.RED + "\nSEE ERROR: ")
        print(error)
        sys.exit()    
    while True:
        if nb_device.name == nb_dn:
            print(Fore.CYAN + '\nDEVICE NAME FOUND IN NETBOX: ' + Fore.WHITE + '{}'.format(nb_device))
            return nb_device #returns device name for next function
        else:
            print(Fore.RED +'\nNO DEVICE NAME FOUND, CHECK NETBOX AND TRY AGAIN.')
            sys.exit()

#function checks for existing interfaces
def netbox_interface_chk(int_data, nb_device):
    print(Fore.CYAN + '\nCHECKING ' + Fore.WHITE + 'FOR INTERFACES IN NETBOX FOR: ' + Fore.WHITE + '{}'.format(nb_device))
    jdata = json.loads(int_data) #converts JSON array back to object for python
    for data in jdata:
        try:
            nb_interface = nb.dcim.interfaces.filter(
            device=nb_device.name)
            return nb_interface       #loops dictionary object to see if interfaces exist for the device, ~/api/dcim/interfaces for reference
        except Exception as error:
                print(Fore.RED + '\nSOMETHING WENT WRONG, WHEN CHECKING FOR INTERFACES IN NETBOX')
                print(error)
                sys.exit()

#adds ability to overwrite interfaces if one choses to do so.
def netbox_intf_overwrite(nb_interface):
    jdata = json.loads(int_data) #converts JSON array back to object for python
    try:
        if len(nb_interface) == 0:  # checks for no interfaces, passes to next function to create them.
            pass
        elif len(nb_interface) >= 1:  # double checks to see if interfaces exist
            print(Fore.RED + '\nINTERFACES ALREADY EXIST FOR THIS DEVICE IN NETBOX... ' + Fore.WHITE + '{}'.format(nb_device))
            proceed = input(Fore.WHITE + 'WOULD YOU LIKE TO PROCEED? y/n:  ').lower()
            if proceed == 'y':
                print(Fore.RED + '\nCREATING INTERFACES WITH THEIR DESCRIPTIONS THAT DO NOT EXIST' + Fore.WHITE + ' IN NETBOX FOR: ' + Fore.WHITE + '{}'.format(nb_device))
                overwrite = input(Fore.RED + 'OVERWRITE ' + Fore.WHITE + 'EXISTING DESCRIPTIONS FOR EXISTING INTERFACES? y/n:  ').lower()
                for data in jdata:
                    try:
                        nb_interface = nb.dcim.interfaces.get(
                        device=nb_device.name, name=data['interface'])
                        if nb_interface is None or len(nb_interface) == 0:
                            nb_intf_create = nb.dcim.interfaces.create(
                            device=nb_device.id,
                            name=data['interface'],
                            type=1000,
                            enabled=True,
                            description=data['description'],
                            )
                    except:
                        pass
                    try:
                        if overwrite == 'y':
                            nb_interface.description = (data['description'])
                            nb_interface.save()
                        elif overwrite == 'n':
                            print(Fore.RED + '\nYOU HAVE CHOSEN *NO* - ' + Fore.WHITE + 'SKIPPING OVERWRITING FOR EXISTING DESCRIPTIONS.')
                        else:
                            print(Fore.RED + '\nINVALID INPUT: ' + Fore.WHITE + 'Try again.')
                            sys.exit()
                    except:
                        pass
            elif proceed == 'n':                               #exits script if user decides too
                print(Fore.RED + '\nYOU HAVE CHOSEN *NO* - ' + Fore.WHITE + 'CHECK NETBOX FOR EXISTING INTERFACE INFORMATION.')
                sys.exit()
            else:                                                       
                print(Fore.RED + '\nINVALID INPUT: ' + Fore.WHITE + 'Try again.')
                sys.exit()

    except Exception as error:
        print(Fore.RED + '\nSOMETHING WENT WRONG, WHEN TRYING TO OVERWRITE EXISTING INTERFACES IN NETBOX')
        print(error)
        sys.exit()


#create new netbox interfaces
def netbox_intf_create(nb_interface_ow, int_data, nb_device):
    jdata = json.loads(int_data) #converts JSON array back to object for python
    try:
        # Create Interface if no interfaces found for device, loops through all found interfaces based on netmiko sent command.
        if nb_interface is None or len(nb_interface) == 0:  # another check just in case I break something above
            print(Fore.GREEN + '\n**NO EXISTING INTERFACES FOUND** ' + Fore.WHITE + ' IN NETBOX FOR: ' + Fore.WHITE + '{}'.format(nb_device))
            print(Fore.GREEN + 'CREATING ' + Fore.WHITE + 'INTERFACES IN NETBOX FOR: ' + Fore.WHITE + '{}'.format(nb_device))
            for data in jdata:
                nb_intf_create = nb.dcim.interfaces.create(
                device=nb_device.id,
                name=data['interface'],
                type=1000,
                enabled=True,
                description=data['description'],
                )
        else:
            #print(Fore.RED + '\nSOMETHING WENT WRONG') # lets me know if I messed a function up above.
            pass
    except Exception as error:
            print(Fore.RED + '\nSOMETHING WENT WRONG, WHEN CREATING NEW INTERFACES IN NETBOX')
            print(error)
            sys.exit()




#main
if __name__ == "__main__":
    int_data = command_runner()
    nb_device = netbox_device()
    nb_interface = netbox_interface_chk(int_data, nb_device)
    nb_interface_ow = netbox_intf_overwrite(nb_interface)
    netbox_intf_create(nb_interface_ow, int_data, nb_device)
    print(Fore.WHITE + '\n..')
    print(Fore.WHITE + '\n.....')
    print(Fore.WHITE + '\n........')
    print(Fore.WHITE + "\nScript completed successfully, please go to netbox and ensure that infomation is correct.")
    print(Fore.WHITE + "\nTotal Elapsed time: " + str(datetime.now() - start_time))




