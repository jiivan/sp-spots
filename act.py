#!/usr/bin/env python3

API_URL = "https://api.pota.app"
CONTINENT = "Europe"
CONTINENTS_PATH = "data/continents.pickle5"
ALERTS_PATH = "data/alerts.db"

import datetime
from dateutil.relativedelta import relativedelta
import logging
import pickle
import prettytable
import requests
import sqlite3

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
    now = datetime.datetime.now(datetime.timezone.utc)
    t = prettytable.PrettyTable()
    t.field_names = ["activator", "ref", "start", "duration (left)", "info"]
    for item in fetch("activation"):
        if not filter_(item['reference']):
            continue
        end_dt = datetime.datetime.fromisoformat(f"{item['endDate']}T{item['endTime']}:00+00:00")
        if end_dt < now:
            continue
        start_dt = datetime.datetime.fromisoformat(f"{item['startDate']}T{item['startTime']}:00+00:00")
        delta = end_dt - max(start_dt, now)
        log.debug(f"id:{item['scheduledActivitiesId']} {item['activator']}@{item['reference']} {item['startDate']} {item['startTime']} -> {delta} ({item['name']}, {item['comments']}, freq: {item['frequencies']})")
        t.add_row([item['activator'], item['reference'], start_dt, delta, f"{item['name']}, {item['comments']}, freq: {item['frequencies']}"[:80]])
    print(t)

def spots(filter_):
    log.info("Spots")
    t = prettytable.PrettyTable()
    t.field_names = ["activator", "ref", "freq", "mode", "cnt", "age"]
    now = datetime.datetime.now(datetime.timezone.utc)
    for item in fetch("spot/activator"):
        if not filter_(item['reference']):
            continue
        log.debug(f"{item['activator']}@{item['reference']} cnt:{item['count']} {item['frequency']}-{item['mode']} {item['spotTime']} by:{item['spotter']}({item['source']}) ({item['name']}, {item['comments']})")
        spot_dt = datetime.datetime.fromisoformat(f"{item['spotTime']}+00:00")
        spot_delta = relativedelta(now, spot_dt)
        t.add_row([item['activator'], item['reference'], f"{float(item['frequency']):.2f}", item['mode'], item['count'], f"{spot_delta.minutes} minutes {spot_delta.seconds} seconds"])
    print(t)

if __name__ == '__main__':
    continents = load_continents(CONTINENTS_PATH)
    filter_ = lambda ref: ref.split('-')[0] in continents['Europe']
    alerts(filter_)
    spots(filter_)
