import os
import json

# Trying to read the file zoneshow and get all the zoning information automatically
# The file zoneshow comes from the command 'zoneshow' in a brocade switch.

alias = {}
reversealias = {}
zones = {}
zonelines = []

if os.path.exists('zoneshow.txt'):
    zone_conf_file = open('zoneshow.txt', 'r')
zonefile = zone_conf_file.readlines()
zone_conf_file.close()
iseffective = False
# aliases
lineNumber = 0
for line in zonefile:
    currentline = line.strip()
    lineNumber += 1
    if currentline.startswith("alias"):
        alias[currentline.split(" ")[1]] = zonefile[lineNumber].strip()
        reversealias[zonefile[lineNumber].strip()] = currentline.split(" ")[1]
    # Effort to get the current effective zones up to line 35
    elif currentline.startswith("zone"):
        if iseffective:
            zonelines.append(lineNumber)
            print(currentline)
            try:
                print(reversealias[zonefile[lineNumber].strip()])
            except:
                pass
    elif currentline.startswith("Effective configuration"):
        iseffective = True

print(f'The WWPN for initiator CHHPure01_CT0_FC0 is => ', alias['CHHPure01_CT0_FC0'])
print(f'The initiator with WWPN 52:4a:93:72:e5:fb:c5:00 is => ', reversealias['52:4a:93:72:e5:fb:c5:00'])

with open('alias.json', 'w') as fp1:
    json.dump(alias, fp1)
with open('reversealias.json', 'w') as fp2:
    json.dump(reversealias, fp2)

# zones
print(zonelines)
