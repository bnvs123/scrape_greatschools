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


def getParentDir():
    cwd = os.getcwd()
    return cwd + '\\' + dt


def getSubDirectory(state):
    return getParentDir() + '\\' + state


def getFileName(state):
    return getSubDirectory(state) + '\\' + state


def getGsidFileName(state):
    return getSubDirectory(state) + '\\' + state + '_gsidState.csv'


def getGsidFileNameAll():
    return getParentDir() + '\\' + 'GsidState_All.csv'


def main():
    df = pd.read_csv('cities_all.csv', encoding='utf8')
    states = list(df.apply(set)[3])
    gsidFileName = getGsidFileNameAll()
    for state in states:
        csvFile = getFileName(state) + '_1.csv'
        stateGsid = []
        # gsidFileName = getGsidFileName(state)
        fieldNames = ['gsId', 'state']
        try:
            df1 = pd.read_csv(csvFile, encoding='utf8')
            for index, row in df1.iterrows():
                gsid = row['gsId_state'].split('_')
                stateGsid.append({'gsId': gsid[0], 'state': gsid[1]})
            with open(gsidFileName, 'a', newline='') as output_file:
                dw = csv.DictWriter(output_file, fieldNames)
                dw.writerows(stateGsid)
        except:
            traceback.print_exc()
            print(state)


if __name__ == "__main__":
    main()
