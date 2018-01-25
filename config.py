#!/usr/bin/env python3

import json

CONFIG_FILENAME='config.json'

def load():
    with open(CONFIG_FILENAME, 'r') as configfile:
        return json.loads(configfile.read())
