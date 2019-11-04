from datetime import datetime, timedelta
from openpyxl import load_workbook
import matplotlib
import matplotlib.pyplot as plt
#import matplotlib.dates as dates

import WorkbookLoaders as wl

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

print(matplotlib.matplotlib_fname())

#import os

#######################################################################################################################
## Functions
#######################################################################################################################

#### Start ####
def findTimeDiffs(rows, startTime, endTime):
  totalCount = 0
  timeDiffs = list()
  for i in range(0, len(smokes) - 1):
  #  print("row 1: ", smokes[i])
  #  print ("row 2: ", smokes[i+1])
    if rows[i][0] < startTime or rows[i][0] > endTime:
      continue
    timediff = rows[i + 1][0] - rows[i][0]
  #  print("timeOne - timeTwo == timediff: {} - {} == {}".format(smokes[i+1][0], smokes[i][0], timediff))
    if timediff < timedelta(0, hour_limit * 60 * 60):
      timeDiffs.append(timediff.total_seconds() / 60)
    totalCount += 1
    
  print("len(timeDiffs): ", len(timeDiffs))    
  print("totalCount: ", totalCount)    

  return timeDiffs, totalCount
#### End ####


#### Start ####
def makeHistogram(timeDiffs, totalCount, startTime, endTime, hour_limit, show_plot = True):

  timePeriodDays = int((endTime - startTime).total_seconds() / (60 * 60 * 24))
  numBins = int(hour_limit * 60 / 3)
  n, bins, patches = plt.hist(timeDiffs, numBins, range=(0, hour_limit * 60),
                              facecolor='red', alpha=0.5,
                              edgecolor='k', linewidth=0.5,
                              label="Total Fixes: %d (%.1f/day)" % (totalCount, totalCount/timePeriodDays))
  
  print("bin size: ", bins[1] - bins[0])
  
  plt.xlim(xmin=0, xmax=bins[-1])

  ax = plt.gca()
  ax.grid(b=True, which=u'both', axis="x", color='k', linestyle='-.')
  
  plt.suptitle("Times Between Nicotine/Cigarette Fixes (< {} hours apart)".format(hour_limit), fontsize=16)
  plt.title(r"For the $\bf%s$ day period: $\bf%s$ to $\bf%s$" % (timePeriodDays,
             startTime.strftime("%Y-%m-%d"), endTime.strftime("%Y-%m-%d")))
  
  plt.xlabel("Time Between Fixes (minutes)")
  plt.ylabel("Count")
  
  plt.legend()

  plt.savefig("Fixes %s to %s.png" % (startTime.strftime("%Y-%m-%d"), endTime.strftime("%Y-%m-%d")))

  if show_plot:
    plt.show()

  plt.clf()
  plt.cla()
  
  return n, bins, patches
#### End ####

#######################################################################################################################
## End Functions
#######################################################################################################################


###
## Parameters
###
# don't add time diffs if the difference is larger than this in hours
hour_limit = 4

sleepTimes, smokeTimes, smokes, potSmokeTimes, potSmokes = wl.loadWorkbooks(wl.logSet)

print("Done Extracting", datetime.now())


# make plots from the start of the current file's data
#startTime = datetime.strptime("2017-05-17 00:00:00", "%Y-%m-%d %H:%M:%S")


firstSmoke = smokes[0][0]
firstSmoke = datetime(firstSmoke.year, firstSmoke.month, firstSmoke.day)
lastSmoke = smokes[-1][0]

# Number of days to put in each plot
dayRange = 90
startTime = firstSmoke
endTime = startTime + timedelta(dayRange) # add 90 days

# Every dayRange days through the whole file
while endTime <= lastSmoke:
  timeDiffs, totalCount = findTimeDiffs(smokes, startTime, endTime)
  makeHistogram(timeDiffs, totalCount, startTime, endTime, hour_limit, show_plot=False)

  startTime = endTime
  endTime += timedelta(dayRange)
  
  print("startTime: ", startTime)
  print("endTime: ", endTime)


# Most recent 90 days
dayRange = 90  # days
endTime = datetime.now()
startTime = endTime - timedelta(dayRange)

timeDiffs, totalCount = findTimeDiffs(smokes, startTime, endTime)
makeHistogram(timeDiffs, totalCount, startTime, endTime, hour_limit, show_plot=False)

# Most recent 365 days
dayRange = 365  # days
endTime = datetime.now()
startTime = endTime - timedelta(dayRange)

timeDiffs, totalCount = findTimeDiffs(smokes, startTime, endTime)
makeHistogram(timeDiffs, totalCount, startTime, endTime, hour_limit, show_plot=False)

# previous recent 365 days
dayRange = 365  # days
endTime = datetime.now() - timedelta(dayRange) 
startTime = endTime - timedelta(dayRange)

timeDiffs, totalCount = findTimeDiffs(smokes, startTime, endTime)
makeHistogram(timeDiffs, totalCount, startTime, endTime, hour_limit, show_plot=False)

# all data in file
startTime = smokes[0][0]
endTime = smokes[-1][0]

timeDiffs, totalCount = findTimeDiffs(smokes, startTime, endTime)
makeHistogram(timeDiffs, totalCount, startTime, endTime, hour_limit, show_plot=False)






























































