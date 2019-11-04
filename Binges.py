from datetime import datetime, timedelta
import numpy as np
from openpyxl import load_workbook
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
#import matplotlib.dates as dates

import WorkbookLoaders as wl
import SmokeAndSleep as sas

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

print(matplotlib.matplotlib_fname())


# max time between smokes to break a binge (seconds)
#time_limit = timedelta(0, 240 * 60)
time_limit = timedelta(0, 120 * 60)
# The number of consecutive smokes in the time limit to count as a binge
min_binge_length = 3

sleepTimes, smokeTimes, smokes, potSmokeTimes, potSmokes = wl.loadWorkbooks(wl.logSet)

# Smoke logging started in earnest 2017-03-25  22:27:18
for i in range(0, len(smokeTimes)):
  if smokeTimes[i] > datetime(2017, 3, 25):
    lastSmoke = smokeTimes[i]
    i_start = i
    break

#lastSmoke = smokeTimes[0]
currBinge = list()
binges = list()
bingeDurations= list()
smokeIntervalsWithinBinge = list()
smokeCountsWithinBinge = list()
for i in range(i_start, len(smokeTimes)):
#for i in range(0, 10):
  if smokeTimes[i] - lastSmoke < time_limit:
    currBinge.append(smokeTimes[i])
    lastSmoke = smokeTimes[i]
  else:
    if len(currBinge) >= min_binge_length:
      binges.append(currBinge)
      bingeDurations.append((currBinge[-1] - currBinge[0]).total_seconds() / (60 * 60))
      for i in range(1, len(currBinge)):
        smokeIntervalsWithinBinge.append((currBinge[i] - currBinge[i - 1]).total_seconds() / 60)
      smokeCountsWithinBinge.append(len(currBinge))
    currBinge = list()
    currBinge.append(smokeTimes[i])
    lastSmoke = smokeTimes[i]

print("Binges: ", len(binges))

# for binge in binges:
#   print("binge: ", binge)

bingeMedian = np.median(bingeDurations)
bingeMean = np.mean(bingeDurations)
print("len(bingeDurations): ", len(bingeDurations))
print("binge duration median (hours)", bingeMedian)
print("binge duration mean (hours)", bingeMean)

intervalMean = np.mean(smokeIntervalsWithinBinge)
print("intervalMean (minutes)", intervalMean)

countMean = np.mean(smokeCountsWithinBinge)
print("countMean", countMean)


# for bingeDuration in bingeDurations:
#   print("binge duration: ", bingeDuration)

n, bins, patches = plt.hist(bingeDurations, 200,
            label=
            "{} Total Binges ({}+ fixes with < {} min between)\nMean binge duration: {} hours \nMean time between Fixes: {} minutes \nMean # of Fixes/Binge: {}".
              format(len(bingeDurations), min_binge_length, int(time_limit.total_seconds()/60),
                    round(bingeMean, 1), round(intervalMean, 1), round(countMean, 1)))

print("bin size: ", bins[1] - bins[0])

#plt.xlim(xmin=0, xmax=bins[-1])
plt.xlim(xmin=0)

ax = plt.gca()
#ax.grid(b=True, which=u'both', axis="x", color='k', linestyle='-.')

majorLocator = MultipleLocator(1)
ax.xaxis.set_major_locator(majorLocator)


plt.suptitle("Binge Durations ({} total binges)".format(len(bingeDurations)), fontsize=16)
plt.title(r"For the $\bf%s$ day period: $\bf%s$ to $\bf%s$" % ((int((smokeTimes[-1] - smokeTimes[i_start]).total_seconds() / (60 * 60 * 24))),
           smokeTimes[i_start].strftime("%Y-%m-%d"), smokeTimes[-1].strftime("%Y-%m-%d")))

plt.xlabel("Binge Duration (hours)")
plt.ylabel("Count")

plt.legend()

plt.savefig("Binges %s to %s.png" % (smokeTimes[0].strftime("%Y-%m-%d"), smokeTimes[-1].strftime("%Y-%m-%d")))

plt.show()


































