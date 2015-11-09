#! /usr/bin/env python
# mapIt.py - Launches a map in the browser using an address from the
# command line or clipboard.

import webbrowser, sys, pyperclip

def start_adress(sysVar,yN):
    if len(sysVar) > 1:
        # Get address from command line.
        address = ' '.join(sysVar[1:])
    else:
      #   Get address from clipboard.
        if yN == 'y' or yN == 'Y':          
            address = raw_input('Where do you want to start?: ')
        else:
            address = raw_input('Where do you want to go?: ')
        return address

directions = raw_input('Do you want directions? (y/n): ')
address = start_adress(sys.argv,directions)
if directions == 'y' or directions == 'Y':
    whereTo = raw_input('Where are you headed?: ')
    webbrowser.open('https://www.google.com/maps/dir/' + address 
                    + '/'+ whereTo + '/')
else:
    webbrowser.open('https://www.google.com/maps/place/' + address)
