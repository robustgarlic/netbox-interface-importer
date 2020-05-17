
#quick test  ntc templates and json output 



# Netmiko is the same as ConnectHandler
import json
from netmiko import Netmiko
from netmiko import ConnectHandler

my_device = {
    "host": "10.6.6.155",
    "username": "username",
    "password": "password",
    "device_type": "alcatel_sros",
}

net_connect = Netmiko(**my_device)
# Requires ntc-templates to be installed in ~/ntc-templates/templates
output = net_connect.send_command("show port description", use_textfsm=True)

#json_output = (json.dumps(output, indent=2))

#data = json_output
print(output)