
## quick test API with pynetbox and netbox


import pynetbox
import json
import os
import sys
import signal

#Device Display Name, call from userinput function

#nb_dn = userinput.get_display_name()


## API TOKEN GOES HERE ##
# generate API token at https://netbox.mydomain.com/user/api-tokens
nb = pynetbox.api(url='http://10.6.6.104:80', token='your token here')

device="test-device"

nb_device = nb.dcim.devices.get(name=device)
print(nb_device)

