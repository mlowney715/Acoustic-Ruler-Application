#!/usr/bin/python
'''
config.py
if a preferences.ini file is not found, create one. Otherwise, access
preference info.
'''

from configobj import ConfigObj

def accessconfig():
	config = ConfigObj()
	config.filename = './preferences.ini'

	config['speedsound'] = 400.00
	config['datapath'] = '~/acoustic_ruler/guiapp/'

	config.write()

	return config['speedsound'], config['datapath']
