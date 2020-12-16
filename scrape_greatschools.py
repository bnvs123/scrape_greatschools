#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import os
import time
import pandas as pd

gs_apiKey = 'cab758959b578488f15595c45c3e2316'

dt = time.strftime("%Y%m%d")


def get_dated_dir():
    dt_dir = os.getcwd() + '\\' + dt
    return dt_dir


def createParentDir():
    dt_dir = get_dated_dir()
    if not os.path.exists(dt_dir):
        os.makedirs(dt_dir)


def createSubDirectories(states=None):
    if states is None:
        states = []
    dt_dir = get_dated_dir()
    for state in states:
        state_dir = dt_dir + '\\' + state
        if not os.path.exists(state_dir):
            os.makedirs(state_dir)


def getFileName(city, state):
    dt_dir = get_dated_dir()
    state_dir = dt_dir + '\\' + state
    return state_dir + '\\' + state + '.csv'


def generateRequest(lat, long, state):
    return 'https://api.greatschools.org/schools/nearby?key={}&state={}&lat={}&lon={}&radius=20&schoolType=public'.format(
        gs_apiKey, state, lat, long)


def convertAndWriteCsv(res, city, state):
    soup = BeautifulSoup(res.content, 'xml')
    csvFile = getFileName(city, state)
    schools = []
    for sc in soup.findAll('school'):
        row = {}
        for i in sc.findAll():
            if i.name and i.name.lower() == 'gsid':
                row[i.name + '_state'] = i.text + '_' + state
            row[i.name] = i.text
        schools.append(row)

    # keys= schools[0].keys()
    fieldNames = ['gsId_state', 'gsId', 'name', 'type', 'gradeRange', 'enrollment', 'gsRating', 'parentRating', 'city',
                  'state', 'districtId', 'district', 'districtNCESId', 'address', 'phone', 'fax', 'website', 'ncesId',
                  'lat', 'lon', 'overviewLink', 'ratingsLink', 'reviewsLink', 'distance', 'schoolStatsLink']
    with open(csvFile, 'a', newline='') as output_file:
        dw = csv.DictWriter(output_file, fieldNames)
        dw.writeheader()
        dw.writerows(schools)


def main():
    df = pd.read_csv('cities_all.csv')
    states = list(df.apply(set)[3])
    createParentDir()
    createSubDirectories(states)

    for index, row in df.iterrows():
        url = generateRequest(row[0], row[1], row[3])  # Lat, Long and State
        res = requests.get(url)
        if res.status_code == 200:
            convertAndWriteCsv(res, row[2], row[3])  # Pass city name to be saved for file name row[2] is City
        time.sleep(.10)


if __name__ == "__main__":
    main()
