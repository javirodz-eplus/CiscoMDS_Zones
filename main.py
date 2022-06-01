import PySimpleGUI as sg
import os
import json

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def zone_alias(brand, name, wwpn, vsan_id, zoningFile):
    if brand == "cisco":
        print(f'fcalias name {name} vsan {vsan_id}', file=zoningFile)
        print(f'member pwwn {wwpn}', file=zoningFile)
    elif brand == "brocade":
        print(f'alicreate "{name}","{wwpn}"', file=zoningFile)
    else:
        print("Brand not supported")


def zone_zone(initiator, target, vsan_id, zoningFile):
    for i_element in initiator:
        for t_element in target:
            print(f'zone name {i_element}_{t_element} vsan {vsan_id}', file=zoningFile)
            print(f'member fcalias {i_element}', file=zoningFile)
            print(f'member fcalias {t_element}', file=zoningFile)
            print(f'exit', file=zoningFile)


def zone_zoneset(zonesetname, initiator, target, vsan_id, zoningFile):
    print(f'zoneset name {zonesetname} vsan {vsan_id}', file=zoningFile)
    for i_element in initiator:
        for t_element in target:
            print(f'member {i_element}_{t_element}', file=zoningFile)
    print(f'exit', file=zoningFile)


if __name__ == '__main__':
    brand = "cisco"

    if os.path.exists('input.json'):
        print("INPUT Present, not prompting the user for the values.")
        zone_conf_file = open('input.json', 'r')
        zone = json.load(zone_conf_file)
        zonesetname = zone['zoneset']
        print(f'The zoneset name is {zonesetname}')
        vsan_id = zone['vsan_id']
        print(f'The VSAN ID is {vsan_id}')
        initiator = zone['initiators']
        print(f'The initiators are {initiator}')
        target = zone['targets']
        print(f'The targets are {target}')
        zone_conf_file.close()
    else:
        # Some default values for now
        vsan_id = "1"
        zonesetname = "sw1_config"

        # Initialize local variables
        enter_initiators = True
        enter_targets = True
        initiator = {}
        target = {}

        # Create elements for the initiator inputs
        layout_initiators = [[sg.Text("What's the initiator name?"), sg.InputText()],
                             [sg.Text("What's the WWPN?"), sg.InputText()],
                             [sg.Button('Next'), sg.Button('Done')]
                             ]
        # Create elements for the target inputs
        layout_targets = [[sg.Text("What's the target name?"), sg.InputText()],
                          [sg.Text("What's the WWPN?"), sg.InputText()],
                          [sg.Button('Next'), sg.Button('Done')]
                          ]

        # Create the Initiator Window
        window = sg.Window('Initiators', layout_initiators)

        # Create the event loop for the initiators
        while enter_initiators:
            event, values = window.read()
            if event in (None, 'Done'):
                # User closed the Window or hit the Done button
                enter_initiators = False
            # print(f'Event: {event}')  # Debug
            # print(str(values))  # Debug
            initiator[str(values[0])] = str(values[1])
        # print(initiator)  # Debug
        window.close()

        # Create the Target Window
        window = sg.Window('Targets', layout_targets)

        # Create the event loop for the initiators
        while enter_targets:
            event, values = window.read()
            if event in (None, 'Done'):
                # User closed the Window or hit the Done button
                enter_targets = False
            # print(f'Event: {event}')  # Debug
            # print(str(values))  # Debug
            target[str(values[0])] = str(values[1])
        # print(target)  # Debug
        window.close()

    # Check if a previous zoning file exists and remove it
    if os.path.exists('zoning.txt'):
        os.remove('zoning.txt')
    # Open new zoning configuration file to write the zoning commands
    zoningFile = open('zoning.txt', 'a')

    # Create one fcalias for each initiator
    print("conf t", file=zoningFile)
    for element in initiator:
        # print(f'The host initiator name is {element}, and the WWPN is {initiator[element]}')  # Debug
        zone_alias(brand, element, initiator[element], vsan_id, zoningFile)
        print("exit", file=zoningFile)
    # Create one fcalias for each target
    for element in target:
        # print(f'The host initiator name is {element}, and the WWPN is {initiator[element]}')  # Debug
        zone_alias(brand, element, target[element], vsan_id, zoningFile)
        print("exit", file=zoningFile)

    # Construct the zones
    zone_zone(initiator, target, vsan_id, zoningFile)

    # Construct the zoneset
    zone_zoneset(zonesetname, initiator, target, vsan_id, zoningFile)

    # Activate the zoneset
    print(f'zoneset activate name {zonesetname} vsan {vsan_id}', file=zoningFile)

    # End Configuration
    print("end", file=zoningFile)

    # Close the zoning configuration file
    zoningFile.close()
