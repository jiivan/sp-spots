#!/usr/bin/env python3

import json
import pickle
import sys

PICKLE_PROTOCOL = 5

def generate(input_) -> dict:
    data = json.load(input_)
    result = {}

    for elem in data:
        abbrev = elem['alpha-2']
        continent = elem['region']
        if abbrev == "AQ": # Antarctica exception
            continent = "Antarctica"
        elif abbrev == "TW": # Taiwan
            continent = "Asia"
        try:
            c = result[continent]
        except KeyError:
            c = result[continent] = set()
        c.add(abbrev)

    return result

def main(input_, output) -> None:
    #print(sorted(generate(input_).keys()))
    pickle.dump(generate(input_), output, protocol=PICKLE_PROTOCOL)

if __name__ == '__main__':
    main(sys.stdin, sys.stdout.buffer)
