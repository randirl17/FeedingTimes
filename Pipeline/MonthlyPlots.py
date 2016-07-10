#ipython ./Pipeline/MonthlyPlots.py './DataFiles/NursingData_clean_ts.csv' plot_extension
"""
Create one plot per calendar month of eat/sleep patterns.
Turn into animated gif using http://ezgif.com/maker
"""
import sys
import pandas as pd
import numpy as np
import datetime as dt
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.nonparametric.smoothers_lowess import lowess

def plotting(file,ext):
    ts = pd.read_csv(file, header=[0,1],index_col=[0])
    ts.index = [dt.datetime.strptime(x, "%H:%M:%S").time() for x in ts.index]
    ts.columns.set_levels([dt.datetime.strptime(x, "%Y-%m-%d").date() for x in ts.columns.levels[0].values], 0, inplace=True)

    #gets used in the smoothing
    xtime = [int(x.hour)+int(x.minute)/60 for x in ts.index]
    timeind = pd.date_range("00:00", "23:59", freq='min').to_pydatetime()###Very important!

#for each month in the data, construct a df of just that month
    for mo in set([x.month for x in ts.columns.levels[0]]):
        monthnum = mo
        motxt = time.strftime('%B',time.strptime(str(monthnum),'%m'))
        mocheck = [x.month == monthnum for x in ts.columns.levels[0]]
        moflag = []
        for ans in mocheck:
            moflag.append(ans)
            moflag.append(ans)

        onemo = ts.loc[:,moflag]

        sleepy = onemo.xs('Sleep',level=1,axis=1).sum(axis=1)/(len(onemo.columns)/2)
        eaty = onemo.xs('Eat',level=1,axis=1).sum(axis=1)/(len(onemo.columns)/2)

#begin plotting
        fig = plt.figure(figsize=(18,6))
        ax = fig.add_subplot(111)

        ####Plot Sleep
        filtereds = lowess(sleepy, xtime, is_sorted=True, frac=0.025, it=0)
        ax.plot(timeind, filtereds[:,1], 'b',linewidth=2,label='Sleeping')
        ax.fill_between(timeind, 0, filtereds[:,1],alpha=0.3,facecolor='b')
        #ax.plot(ts.index,sleepy,'b',linewidth=2,label='Sleeping')#raw data, not smoothed
        #ax.fill_between(ts.index, 0, sleepy,alpha=0.3,facecolor='b')

        ####Plot Eat
        filterede = lowess(eaty, xtime, is_sorted=True, frac=0.025, it=0)
        ax.plot(timeind, filterede[:,1], 'orange',linewidth=2,label='Eating')
        ax.fill_between(timeind, 0, filterede[:,1],alpha=0.3,facecolor='orange')
        #ax.plot(ts.index,eaty,'orange',linewidth=2,label='Eating')
        #ax.fill_between(ts.index, 0, eaty,alpha=0.3,facecolor='orange')

        ####Axis formatting
        xax = ax.get_xaxis()
        xax.set_major_locator(mdates.HourLocator(byhour=range(0,24,2)))
        xax.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.set_title('Activity Fraction at a Given Time of Day',fontsize='xx-large')
        ax.text('16:00',0.9,motxt,fontsize='xx-large',color='k',fontweight='bold')
        ax.legend(fontsize='x-large')
        ax.set_ylim(0,1.1)
        fig.autofmt_xdate()
        filename = 'b2_TimeSeries/Activity_' + str(monthnum) + '.' + ext
        fig.savefig(filename)
    return 


def main():
    args = sys.argv[1:]

    if not args:
        print('usage: ./MonthlyPlots.py file plot_ext')
        sys.exit(1)
    
    plotting(args[0],args[1])

if __name__ == '__main__':
  main()
