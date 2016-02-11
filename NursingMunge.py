#ipython NursingMunge.py 'NursingData.csv'
"""
Read in data from csv and convert to useful DataFrame.
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
        
def munge(file):
    df = pd.read_csv(file)
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
    df.loc[:,'leftfeed'] = pd.Series(leftadj, index = df.index)
    df.loc[:,'rightfeed'] = pd.Series(rightadj, index = df.index)

#Total feeding time = left + right if nursing, default 5 min if bottle fed
    botarr = np.array(df['Bottle'])
    bottime = np.where(botarr == ' Bottle-Pump',5.,0.)
    df.loc[:,'botfeed'] = pd.Series(bottime, index = df.index)
    totfeed = leftadj + rightadj + bottime
    df.loc[:,'totalfeed'] = pd.Series(totfeed, index = df.index)

#Time columns
    month = []
    year = []
    timeofday = []
    for time in df['time']:
        month.append(time.strftime('%m'))
        year.append(time.strftime('%Y'))
        if int(time.strftime('%H')) <= 6:
            timeofday.append('Late night')
        elif 6 < int(time.strftime('%H')) <= 12:
            timeofday.append('Morning')
        elif 12 < int(time.strftime('%H')) <= 18:
            timeofday.append('Afternoon')
        elif 18 <= int(time.strftime('%H')):
            timeofday.append('Evening')
    df['Month'] = month
    df['Year'] = year
    df['Time of Day'] = timeofday

#construct feeding DataFrame
    feeddf = pd.DataFrame(df, columns=['time','Year','Month',
                                       'Time of Day','leftfeed',
                                       'rightfeed','Total Feed'])
    feeddf.insert(6,'botfeed',bottime)
    return feeddf
"""
Alternative formulation for a new DataFrame using dict notation.

    feeddf = pd.DataFrame({'time':df.time,'leftfeed':df.leftfeed,
                       'rightfeed':df.rightfeed, 'botfeed': bottime,
                       'totfeed':df['Total Feed'], 'month':df.Month,
                       'ToD':df['Time of Day'], 'year':df.Year})
"""
    


    
#    monthly = df.groupby([df['Year'],df['Month']])
#    ordered = df.sort_values('time')


#still to address:  bottle amounts, sleep time
#bottle amounts are str "#oz" or "#.5oz", need to replace 'oz' w/ '' then convert remaining str to float, default NaN for 
#so sleep times are hh:mm:ss, so will need to do a similar conversion as "Left" etc.

def main():
    args = sys.argv[1:]

    if not args:
        print('usage: ./NursingMunge.py file')
        sys.exit(1)
        munge(ars[0])

if __name__ == '__main__':
  main()
