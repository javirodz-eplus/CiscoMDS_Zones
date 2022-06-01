# CiscoMDS_Zones
This python script will print the zoning configuration for a Cisco MDS switch to the 'zoning.txt' file.
The script will check if there exists a file with the name inputs.json to get the input. If there is no such file  
then it will prompt the user.

The zone will be done as single-initiator-single-target.

You can copy and paste the content of 'zoning.txt' directly into the switch, but be careful because  
the configuration will overwrite the active zoneset for the vsan.

For the main script to work you'll only need main.py and the optional input.json.
