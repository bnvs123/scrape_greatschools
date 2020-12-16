#!/usr/bin/env python
import os
import traceback

import pandas as pd

dt = '20200818'


def getParentDir():
    cwd = os.getcwd()
    return cwd + '\\' + dt


def getSubDirectory(state):
    return getParentDir() + '\\' + state


def getFileName(state):
    return getSubDirectory(state) + '\\' + state


def main():
    df = pd.read_csv('cities_all.csv', encoding='utf8')
    states = list(df.apply(set)[3])
    for state in states:
        csv_file = getFileName(state) + '.csv'
        csv_no_dup = getFileName(state) + '_1.csv'
        try:
            df1 = pd.read_csv(csv_file, encoding='ISO-8859-1')
            df1.sort_values('gsId_state', inplace=True)
            df1.drop_duplicates(subset='gsId_state', keep='first', inplace=True)
            df1.to_csv(csv_no_dup, index=False, header=True)
        except Exception as e:
            traceback.print_exc()
            print(state)


if __name__ == "__main__":
    main()
