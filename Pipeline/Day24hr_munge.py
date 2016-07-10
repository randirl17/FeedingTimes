#ipython ../Pipeline/Day24hr_munge.py '../Datafiles/NursingData_6-3_clean.csv'
"""
Convert clean nursing data into dummy table in order to plot daily,monthly % per time
"""
import sys
import pandas as pd
import numpy as np
import datetime as dt

def munge(file):
    df = pd.read_csv(file)
    df['time'] = pd.to_datetime(df['time'])

#create hours array for index
    timeind = pd.date_range("00:00", "23:59", freq='min').time
#create date, eat/sleep arrays for multiIndex
    totarr = pd.Series(d.date() for d in df.time)
    datearr = totarr.unique()
    dateind = []
    for d in datearr:
        dateind.append(d)
        dateind.append(d)
    esarr = ['Eat','Sleep']*len(datearr)
    arrays = [dateind,esarr]

    ts = pd.DataFrame(np.zeros((len(timeind),len(dateind))),index=timeind,columns=arrays)

    #for each entry in original data, either an eat or a sleep
    for i,dtinfo in enumerate(df.time):
        print(dtinfo)
        eatsleep = ''
        if df.TotalFeed[i] > 0:
            eatsleep = 'e'
            intmin = int(df.TotalFeed[i])#don't care about seconds
            endtime = dtinfo + dt.timedelta(minutes = intmin)
        if df.Sleep[i] > 0:
            eatsleep = 's'
            inthrs = int(df.Sleep[i])
            intmin = int((df.Sleep[i]-inthrs)*60)
            endtime = dtinfo + dt.timedelta(hours = inthrs, minutes = intmin)
        endtime = endtime
        dtinfo = dtinfo
        
        for dates in datearr:
            #find matching date
            if dtinfo.date() == dates:            
                #go through times on that date, set appropriate toggles
                for timebymin in ts.index:
                    if dtinfo < dt.datetime.combine(dtinfo.date(),timebymin) <= endtime:
                        if eatsleep == 'e':
                            ts.loc[timebymin,(dates,'Eat')]=1
                        if eatsleep == 's':
                            ts.loc[timebymin,(dates,'Sleep')]=1
                    if dt.datetime.combine(dtinfo.date(),timebymin) > endtime:
                        break
#previous for loop goes through 0-24 hours, but what about events that pass through midnight?
#2016-02-06 23:20:26, 2016-02-07 11:51:26
#previous loop will get the part from 23:20:26 - 24:00
#need to get the part from 00:00-11:51 on the next day

                if endtime.date() > dates:
                    for timebymin in ts.index:
                        if dtinfo < dt.datetime.combine(endtime.date(),timebymin) <= endtime:
                            if eatsleep == 'e':
                                ts.loc[timebymin,(endtime.date(),'Eat')]=1
                            if eatsleep == 's':
                                ts.loc[timebymin,(endtime.date(),'Sleep')]=1
                        if dt.datetime.combine(endtime.date(),timebymin) > endtime:
                            break
        
    eats = ts.xs('Eat',level=1,axis=1)
    sleeps = ts.xs('Sleep',level=1,axis=1)
    return ts, eats, sleeps

def main():
    args = sys.argv[1:]

    if not args:
        print('usage: ./Day24hr_munge.py file')
        sys.exit(1)

    filefront = args[0][:-4]
    filets = filefront + '_tsmid.csv'
    fileeat = filefront + '_tsEmid.csv'
    filesleep = filefront + '_tsSmid.csv'
    
    cleants, cleaneat, cleansleep  = munge(args[0])

    cleants.to_csv(filets,float_format='%.2f',index=True,date_format='%Y-%m-%d')
    cleaneat.to_csv(fileeat,float_format='%.2f',index=True)
    cleansleep.to_csv(filesleep,float_format='%.2f',index=True)

if __name__ == '__main__':
  main()
