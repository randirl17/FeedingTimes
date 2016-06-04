#ipython Day24hr_munge.py 'NursingData_clean.csv'
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

        for dates in datearr:
            #find matching date
            if dtinfo.date() == dates:            
                #go through times on that date, set appropriate toggles
                for timebymin in ts.index:
                    if dtinfo.time() < timebymin and timebymin <= endtime.time():
                        if eatsleep == 'e':
                            ts.loc[timebymin,(dates,'Eat')]=1
                        if eatsleep == 's':
                            ts.loc[timebymin,(dates,'Sleep')]=1

    eats = ts.xs('Eat',level=1,axis=1)
    sleeps = ts.xs('Sleep',level=1,axis=1)
    return ts, eats, sleeps, ts.index, ts.columns

def main():
    args = sys.argv[1:]

    if not args:
        print('usage: ./Day24hr_munge.py file')
        sys.exit(1)

    filefront,fileend = args[0].split('.')
    filets = filefront + '_ts.csv'
    fileeat = filefront + '_tsE.csv'
    filesleep = filefront + '_tsS.csv'
    
    cleants, cleaneat, cleansleep, rownames, colnames  = munge(args[0])
####
####need to modify to_csv for multiindex on cleants!!!    
####,index_label=colnames
    ts.to_csv(filets,float_format='%.2f',index=True,date_format='%Y-%m-%d')
    cleaneat.to_csv(fileeat,float_format='%.2f',index=True)
    cleansleep.to_csv(filesleep,float_format='%.2f',index=True)

if __name__ == '__main__':
  main()
