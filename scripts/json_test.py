#!/usr/bin/env python

import json
import pprint

with open('locations.json') as json_data:
    stuff = json.load(json_data)

print("using locations file: locations.json")
data = stuff['entrance']['x']
print data
