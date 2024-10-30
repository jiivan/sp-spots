#!/usr/bin/env python3

API_URL = "https://api.pota.app"
CONTINENT = "Europe"
CONTINENTS_PATH = "data/continents-iso.pickle5"
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

def _format_delta(td: relativedelta) -> str:
    if td.months:
        days = f"{td.months} mnth "
    elif td.days:
        days = f"{td.days} days "
    else:
        days = ""
    return f"{days}{td.hours:02}:{td.minutes:02}"

def alerts(filter_):
    log.debug("Alerts")
    now = datetime.datetime.now(datetime.timezone.utc)
    t = prettytable.PrettyTable()
    t.field_names = ["activator", "ref", "start", "time to start", "duration (left)", "info"]
    t.align = "r"
    t.align["info"] = "l"
    for item in fetch("activation"):
        if not filter_(item['reference']):
            continue
        end_dt = datetime.datetime.fromisoformat(f"{item['endDate']}T{item['endTime']}:00+00:00")
        if end_dt < now:
            continue
        start_dt = datetime.datetime.fromisoformat(f"{item['startDate']}T{item['startTime']}:00+00:00")
        if (end_dt - start_dt).days > 1:
            log.info(f"Filtering out spammy alert by {item['activator']}@{item['reference']}")
            continue
        delta = _format_delta(relativedelta(end_dt, max(start_dt, now)))
        tts = _format_delta(relativedelta(max(start_dt, now), now))
        log.debug(f"id:{item['scheduledActivitiesId']} {item['activator']}@{item['reference']} {item['startDate']} {item['startTime']} -> {delta} ({item['name']}, {item['comments']}, freq: {item['frequencies']})")
        t.add_row([item['activator'], item['reference'], start_dt.strftime("%y-%m-%d %H:%MZ"), tts, delta, f"{item['name']}, {item['comments']}, freq: {item['frequencies']}"[:80]])
    print(t)

def spots(filter_):
    log.debug("Spots")
    t = prettytable.PrettyTable()
    t.field_names = ["activator", "ref", "freq", "mode", "cnt", "age"]
    now = datetime.datetime.now(datetime.timezone.utc)
    for item in sorted(fetch("spot/activator"), key=lambda i: i['spotTime'], reverse= True):
        if not filter_(item['reference']):
            continue
        log.debug(f"{item['activator']}@{item['reference']} cnt:{item['count']} {item['frequency']}-{item['mode']} {item['spotTime']} by:{item['spotter']}({item['source']}) ({item['name']}, {item['comments']})")
        spot_dt = datetime.datetime.fromisoformat(f"{item['spotTime']}+00:00")
        spot_delta = relativedelta(now, spot_dt)
        t.add_row([item['activator'], item['reference'], f"{float(item['frequency']):.2f}", item['mode'], item['count'], f"{spot_delta.minutes} minutes {spot_delta.seconds} seconds"])
    if t.rowcount:
        print(t)

if __name__ == '__main__':
    continents = load_continents(CONTINENTS_PATH)
    filter_ = lambda ref: ref.split('-')[0] in continents[CONTINENT] | continents["Antarctica"]
    spots(filter_)
    alerts(filter_)
