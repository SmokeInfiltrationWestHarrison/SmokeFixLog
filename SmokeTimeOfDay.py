from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

import WorkbookLoaders as wl



#######################################################################################################################
## Functions
#######################################################################################################################

#### Start ####
def makeHistogram(smokeHours, startTime, endTime, show_plot = True):

  timePeriodDays = int((endTime - startTime).total_seconds() / (60 * 60 * 24))
  numBins = int(24 * 60 / 30)
  n, bins, patches = plt.hist(smokeHours, numBins, range=(0, 24 * 60 * 60),
                              facecolor='red', alpha=0.5,
                              edgecolor='k', linewidth=0.5,
                              label="Time of Day of Smoke Fix")

  print("bin size: ", bins[1] - bins[0])

  plt.xlim(xmin=0, xmax=bins[-1])
  plt.xticks(np.arange(0, 24 * 60 * 60, 3 * 60 * 60))

  ax = plt.gca()
  ax.grid(b=True, which=u'both', axis="x", color='k', linestyle='-.')

  plt.suptitle("Times of Day of Nicotine/Cigarette Fixes", fontsize=16)
  plt.title(r"For the $\bf%s$ day period: $\bf%s$ to $\bf%s$" % (timePeriodDays,
             startTime.strftime("%Y-%m-%d"), endTime.strftime("%Y-%m-%d")))

  plt.xlabel("Fix Time of Day")
  plt.ylabel("Count")

  plt.legend()

#  plt.savefig("Fixes %s to %s.png" % (startTime.strftime("%Y-%m-%d"), endTime.strftime("%Y-%m-%d")))

  if show_plot:
    plt.show()

  plt.clf()
  plt.cla()

  return n, bins, patches
#### End ####

#######################################################################################################################
## End Functions
#######################################################################################################################





print("Extracting", datetime.now())
sleepTimes, smokeTimes, smokes, potSmokeTimes, potSmokes = wl.loadWorkbooks(wl.logSet)
print("Done Extracting", datetime.now())


smokeHours = list()
for smoke in smokeTimes:
#  smokeHour.append(time(smoke.hour, smoke.minute, smoke.second, smoke.microsecond))
  smokeHours.append(smoke.time())

print("len(smokeTimes)", len(smokeTimes))
print("len(smokeHour)", len(smokeHours))

print("smokeHours[0]", smokeHours[0])



makeHistogram(smokeHours, smokeTimes[0], smokeTimes[-1], show_plot = True)














