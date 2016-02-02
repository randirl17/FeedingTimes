"""
Read in data from csv and determine patterns for each month.
"""

import sys
import pandas as pd

def munge():
    df = pd.read_csv('NursingData.csv')
#Nursing app returns data by tab in the app, i.e. nursing data first, then diapers, sleep, and pumping are appended, rather than inserting data into the correct columns.  Need to consolidate data by date first.
    headers = list(df.columns.values)
    newhead = []
    for name in headers:
        newhead.append(name.strip())
    
    
return



def main():
    img_urls = routine()


if __name__ == '__main__':
  main()
