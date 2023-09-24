#!/usr/bin/env python3

API_URL = "https://api.pota.app"

import datetime
import logging
import requests

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

def fetch(path: str) -> list:
    response = requests.get(f"{API_URL}/{path}")
    return response.json()

def alerts():
    log.info("Alerts")
    for item in fetch("activation"):
        if not item['reference'].startswith("SP-"):
            continue
        print(item['scheduledActivitiesId'])
        start_dt = datetime.datetime.fromisoformat(f"{item['startDate']}T{item['startTime']}:00+00:00")
        end_dt = datetime.datetime.fromisoformat(f"{item['endDate']}T{item['endTime']}:00+00:00")
        delta = end_dt - start_dt
        log.info(f"{item['activator']}@{item['reference']} {item['startDate']} {item['startTime']} -> {delta} ({item['name']}, {item['comments']}, freq: {item['frequencies']})")

def spots():
    log.info("Spots")
    for item in fetch("spot/activator"):
        if not item['reference'].startswith("SP-"):
            continue
        log.info(f"{item['activator']}@{item['reference']} cnt:{item['count']} {item['frequency']}-{item['mode']} {item['spotTime']} by:{item['spotter']}({item['source']}) ({item['name']}, {item['comments']})")
        print(f"POTA {item['activator']} AT {item['reference']} = FRQ {item['frequency']} {item['mode']} = CNT {item['count']}")

if __name__ == '__main__':
    alerts()
    spots()
