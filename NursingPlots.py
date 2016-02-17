"""
Read in data from csv and determine patterns for each month.
"""

import sys
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import NursingMunge



def routine(file):
    plotdf = NursingMunge(file)

return

"""
Ideas for data investigation/plots:
L/R counts bar graph for time of day (sleep, afternoon, evening)
mean daily feeding per week
Stacked bar for L/R/bottle counts per month
Stacked bar for hrs slept, night + nap(s) per month
Time sleeping in one day vs time eating in one day (correlated?)
Do naps that immediately follow nursing last longer than ones that don't? (Time since last nurse vs. length of nap)
Frequency of bottle feedings per month (have bottle feedings become more rare with age?)

make keys of month (0,1,2...) and week to .groupby() and perform summary stats on 
"""

def main():
    args = sys.argv[1:]

  if not args:
    print('usage: ./NursingPlots.py file')
    sys.exit(1)
    munge(args[0])


if __name__ == '__main__':
  main()
