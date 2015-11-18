#! /usr/bin/env python

import webbrowser, sys

if len(sys.argv) > 1:
    # Get address from command line.
    word = ' '.join(sys.argv[1:])
else:
    #   Get address from clipboard.
    word = raw_input('What word do you want to look up?: ') 
webbrowser.open('http://dictionary.reference.com/browse/'+word)
