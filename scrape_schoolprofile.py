#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import os
import time
import pandas as pd
import traceback

dt = '20200818'
gs_apiKey = 'cab758959b578488f15595c45c3e2316'


def getParentDir():
    cwd = os.getcwd()
    return cwd + '\\' + dt


def getSubDirectory(state):
    return getParentDir() + '\\' + state


def getFileName(state):
    return getSubDirectory(state) + '\\' + state + '_2.csv'


def getGsidFileNameAll():
    return getParentDir() + '\\' + 'GsidState_All.csv'


def generateRequest(gsid, state):
    return 'https://api.greatschools.org/school/census/{}/{}?key={}'.format(state, gsid, gs_apiKey)


def convertAndWriteCsv(res, gsid, state):
    soup = BeautifulSoup(res.content, 'xml')
    csvFile = getFileName(state)
    schools = []
    # keys= schools[0].keys()
    fieldNames = ['gsid', 'state', 'schoolName', 'address', 'latitude', 'longitude', 'phone', 'type', 'district',
                  'headOfficialName', 'headOfficialEmail', 'enrollment', 'freeAndReducedPriceLunch',
                  'White, non-Hispanic', 'Black, non-Hispanic', 'Hispanic', 'Multiracial', 'Asian',
                  'Native American or Native Alaskan', 'Native Hawaiian or Other Pacific Islander', 'year', 'idea',
                  'plan504', 'percentTeachersInFirstSecondYear']

    for sc in soup.findAll('census-data'):
        row = {'gsid': gsid, 'state': state}
        for i in sc.findAll():
            if i.name and i.name.lower() == 'ethnicities':
                for eth in i.findAll('ethnicity'):
                    if eth.find('name').text in fieldNames:
                        row[eth.find('name').text] = eth.find('value').text
            elif i.name in fieldNames:
                row[i.name] = i.text
        schools.append(row)

    with open(csvFile, 'a', newline='') as output_file:
        dw = csv.DictWriter(output_file, fieldNames)
        dw.writerows(schools)


def main():
    df = pd.read_csv(getGsidFileNameAll(), encoding='utf8')
    for index, row in df.iterrows():
        url = generateRequest(row[0], row[1])  # Gsid, State
        res = requests.get(url)
        if res.status_code == 200:
            convertAndWriteCsv(res, row[0], row[1])  # Pass result , Gsid and state
        time.sleep(.10)


if __name__ == "__main__":
    main()
