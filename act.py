#!/usr/bin/env python3

API_URL = "https://api.pota.app"
CONTINENT = "Europe"
CONTINENTS_PATH = "data/continents.pickle5"

import datetime
import logging
import pickle
import requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

def load_continents(path: str) -> dict:
    with open(path, 'rb') as f:
        return pickle.load(f)

def fetch(path: str) -> list:
    response = requests.get(f"{API_URL}/{path}")
    return response.json()

def alerts(filter_):
    log.info("Alerts")
    for item in fetch("activation"):
        if not filter_(item['reference']):
            continue
        print(item['scheduledActivitiesId'])
        start_dt = datetime.datetime.fromisoformat(f"{item['startDate']}T{item['startTime']}:00+00:00")
        end_dt = datetime.datetime.fromisoformat(f"{item['endDate']}T{item['endTime']}:00+00:00")
        delta = end_dt - start_dt
        log.info(f"{item['activator']}@{item['reference']} {item['startDate']} {item['startTime']} -> {delta} ({item['name']}, {item['comments']}, freq: {item['frequencies']})")

def spots(filter_):
    log.info("Spots")
    for item in fetch("spot/activator"):
        if not filter_(item['reference']):
            continue
        log.info(f"{item['activator']}@{item['reference']} cnt:{item['count']} {item['frequency']}-{item['mode']} {item['spotTime']} by:{item['spotter']}({item['source']}) ({item['name']}, {item['comments']})")
        print(f"POTA {item['activator']} AT {item['reference']} = FRQ {item['frequency']} {item['mode']} = CNT {item['count']}")

if __name__ == '__main__':
    continents = load_continents(CONTINENTS_PATH)
    filter_ = lambda ref: ref.split('-')[0] in continents['Europe']
    alerts(filter_)
    spots(filter_)
