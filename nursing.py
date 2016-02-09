"""
Read in data from csv and determine patterns for each month.
"""

import sys
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime

def convmmss(mmss):
# converts column of ['mm','ss'] lists to array of mm.mm data points
    minlist = []
    for value in mmss:
        if len(value) == 1:
            value = [float('NaN'),float('NaN')]
        else:
            if int(value[1]) < 10:
                value[1] = value[1] + '0'
        minutes = float(value[0]) + float(value[1])/60.
        minlist.append(minutes)
    minarr = np.array(minlist)
    return minarr
        
def munge():
    df = pd.read_csv('NursingData.csv')
#Nursing app returns data by tab in the app, i.e. nursing data first, then diapers, sleep, and pumping are appended, rather than inserting data into the correct columns.  Need to consolidate data by date first.

#Column headers need to be unpadded.
    headers = list(df.columns.values)
    newhead = []
    for name in headers:
        newhead.append(name.strip())
    df.columns = newhead
    
    df['time'] = pd.to_datetime(df['time'])
    del df['#']

#Need to convert mm:ss entries to mm.mm
#replace data where timer was left running (>45 min), default 15 min
    leftmin = convmmss(df['Left'].str.split(':'))
    rightmin = convmmss(df['Right'].str.split(':'))
    leftadj = np.where(leftmin > 45, 15., leftmin)
    rightadj = np.where(rightmin > 45, 15., rightmin)

#Total feeding time = left + right if nursing, default 5 min if bottle fed
    botarr = np.array(df['Bottle'])
    bottime = np.where(botarr == ' Bottle-Pump',5.,0.)
    totfeed = leftadj + rightadj + bottime
    df.loc[:,'Total Feed'] = pd.Series(totfeed, index = df.index)


    
    ordered = df.sort_values('time')
    
return

"""
Ideas for data investigation/plots:
L/R counts bar graph for time of day (sleep, afternoon, evening)
mean daily feeding per week
Stacked bar for L/R/bottle counts per month
Stacked bar for hrs slept, night + nap(s) per month
Time sleeping in one day vs time eating in one day (correlated?)
Do naps that immediately follow nursing last longer than ones that don't? (Time since last nurse vs. length of nap)

make keys of month (0,1,2...) and week to .groupby() and perform summary stats on 
"""


def main():
    img_urls = routine()


if __name__ == '__main__':
  main()
