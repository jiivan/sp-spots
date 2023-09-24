#!/usr/bin/env python3

import json
import pickle
import sys

CONTINENT_MAPPING = {
    'AF': 'Africa',
    'AN': 'Antarctica',
    'AS': 'Asia',
    'EU': 'Europe',
    'NA': 'North America',
    'OC': 'Oceania',
    'SA': 'South America',
}

def generate(input_) -> dict:
    data = json.load(input_)
    result = {}

    for elem in data['dxcc']:
        prefixes = set(elem['prefix'].split(','))
        for continent_abbrev in elem['continent']:
            continent = CONTINENT_MAPPING[continent_abbrev]
            try:
                c = result[continent]
            except KeyError:
                c = result[continent] = set()
            c |= prefixes

    return result

def main(input_, output) -> None:
    #print(sorted(generate(input_).keys()))
    pickle.dump(generate(input_), output)

if __name__ == '__main__':
    main(sys.stdin, sys.stdout.buffer)
