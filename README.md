## Netbox Interface Importer

<em>Tested on Netbox Version v2.8.6</em>

Netbox Interface Importer is a python script that utilizes the popular [netmiko](https://github.com/ktbyers/netmiko) along with [ntc-templates](https://github.com/networktocode/ntc-templates) to import interfaces and their descriptions in bulk, directly from the device to [Netbox](https://github.com/netbox-community/netbox). Like many, a source of truth for IPAM/DCIM has been implemented long after the establishment of a network. This script helps take away the pain of manually going through interfaces and adding them and their descriptions one-by-one on each device in Netbox. Currently there is no way to do this in bulk without utilizing the API. 

Currently this gathers Interface and Description on the following OS's:

 - Nokia/Alcatel SROS
 - Cisco IOS
 - Juniper Junos


These are defined based on the JSON object 'device_type' associated with the user inputted hostname.

### What it does

Netbox interface importer logs into a host and gathers information based on "show interfaces" for Cisco IOS and Junos, or "show port description" for Nokia SROS. This information is then passed along a Text-FSM template which is then passed along pynetbox to post, put, and or patch interfaces and their descriptions for device objects that already exist in netbox. 

This script will:

 - create all new interfaces and their descriptions in netbox for an existing device object that has no interfaces created.
 - create missing interfaces and their descriptions in netbox and/or update existing interface descriptions in netbox for and existing device object.


## Requirements
Devices must already be created in netbox.
Python 3.8 was used for this script. Netmiko, [pynetbox](https://github.com/digitalocean/pynetbox), and ntc-templates are required to use this script, besides the obvious platforms this is interacting with. I recommend just installing the required libraries via `pip3 install -r requirements.txt`. You will also need to install ntc-templates.
I would also recommend using your favorite python virtual environment prior to using this.

## Installation

For those who would like some guidance on setting on an environment for this just do the following.

 1. Start your favorite virtual environment, I used virtualenv:
> `source venv/bin/activate`
 2. Install requirements:
> `pip3 install -r requirements.txt`
 3. Install networktocode/ntc-templates in your projectfolder i.e:
> `host: ~/your/project/directory/here/netbox-interface-importer/$ git clone https://github.com/networktocode/ntc-templates.git`
 4. Tell environment where ntc-templates is:
>`export NET_TEXTFSM="~/netbox-interface-importer/ntc-templates/templates"`
>`echo $NET_TEXTFSM`
 5. Change the environment variables in the python script themselves, this is your json inventory file location, and pynetbox api variables.
 6. Run the script and follow the prompts:
> python3.8 nb_int_importer.py

## Other things
I edited the existing "show interfaces" text-fsm template for the juniper_junos command, I added interfaces to it. I also created a new template for alcatel_sros "show interfaces descriptions".  This are not included in the ntc-templates git clone, so just copy those over from the templates in this repository into the correct locations per their readme.md on their github. 
All interfaces are inputted as 1G, whether it is or not, much more simpler to just edit it in netbox after its added.

Due to the nature of how we do virtual chassis's and their naming conventions, a separate input is gathered from the host to match the netbox device name. This can allows you to take the output of the host you logged into and place that info in a different device on netbox, not an intended feature but it can be done.  It also causes an issue where it will put all the interfaces into the master(usually) you decide too. Virtual Chassis's will collapse all interfaces into the master and number them accordingly based on the other nodes, so each device should be numbered according to the Virtual Chassis and then all can be viewed from the Master. 


## TODO

 - Add/create/update devices if they are not found.
 - Add/create/update vrfs, prefixes, ip addresses to interfaces if they are not found.
 - Potentially connect devices based on CDP/LLDP - pending internal use case.
 - Add separate feature to update device interfaces that are in a virtual chassis accordingly.
 - ~~- Do not patch existing interfaces, but create and add interfaces if they do not exist on the device in netbox.~~ Done
