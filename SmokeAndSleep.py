from datetime import datetime, timedelta
import os
import csv
#import random
#from openpyxl import load_workbook
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.collections import LineCollection
#import numpy as np
#from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.ticker import MultipleLocator
import numpy as np

#import WorkbookLoaders as wl

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

print(matplotlib.matplotlib_fname())

#import os
 
###
## Parameters
###
 
## How far into the future we project moving averages
projectionTime = 24 * 60 * 60  # seconds
#projectionTime = 0 * 60 * 60  # seconds
## How much past time to include in the sleep moving average
sleepAvgDuration = 2 * 24 * 60 * 60  # seconds
## time step between moving average points/calculations
timeStep = 180  # seconds
## For graphs that end at the present, how far back they should go
dayRange = 7  # days
# only add time labels to sleep bars and time intervals if the plot is fewer than this many days
#maxDaysForTimeLables = 35
maxDaysForTimeLables = 10000 # for writing sleepless intervals to file
# Directory to put saved plots in
plotDir = "plots"
# delimits sections of notable date ranges in the written csv files
sleeplessIntervalDelim = "Sleepless Interval"
# subdir pathname for the notable dates csv
notableDatesPathname = "Notable Dates"
# filename for notable date intervals csv (time will be added as well)
notableDatesHeader = "Notable Dates"
# filename for low sleep intervals derived from the moving average sleep
lowSleepHeader = "Low Sleep"
# Have to turn this on to write "notable dates" or low sleep intervals to a file
writeNotableDates = True
# average sleep limit considered "low" in hours
lowSleepLimit = 7
# colors to use on the moving average line for sleep below or above the low sleep limit
lowSleepColor = "r--"
normalSleepColor = "k--"

# Yellow for smoke that interferes with sleep
smokeSleepBorderColor = "y"
# Red for smoke fixes
tabaccoSmokeColor = "r"
# Shit brown for both pot smoke fixes and sleep/wake interference
potSmokeColor = "saddlebrown"

###
## Event keys from log
###
#medKey = "Trileptal"
medKey = "Lamictal"
sleepKey = ("Sleep (crosseyed)", "Sleep (med-tired)", "Sleep (normal)")
wakePoor = "Wake (poor)"
wakeMedium = "Wake (medium)"
wakeSound = "Wake (sound)"
#wakeKey = ("Wake (medium)", "Wake (poor)", "Wake (sound)")
wakeKey = (wakePoor, wakeMedium, wakeSound)
smokeKey = "Smoke"
potSmokeKey = "Pot Smoke"
# seizureKey = "Seizure"



#######################################################################################################################
## Functions
#######################################################################################################################

#### Start ####
def calculateSleepData(sleepTimes, startTime, currTime, endTime, projectionTime, timeStep, sleepAvgDuration):
  # startTime -- (datetime) the time our calculation period starts
  # currTime -- (datetime) delineates past and future periods within our calculation period.
  #             For only past data and no future projection, currTime == endTime  
  # endTime -- (datetime) the time our calculation period ends
  # projectionTime -- (seconds) how far into the future to project (seconds)
  # timeStep -- (seconds) time step between moving average points/calculations
  # sleepAvgDuration -- (seconds) How much past time to include in the sleep moving average
    
    # make a time-index list for sleep moving averages
  mvAvgCurveTimes = list()
  timeTicks = int(((currTime - startTime).total_seconds() + sleepAvgDuration) / timeStep) * timeStep
  for sec in range(0, timeTicks, timeStep):
    time = startTime - timedelta(0, sleepAvgDuration) + timedelta(0, sec)
    mvAvgCurveTimes.append(time)

  # Project into the future
  timeTicks = int(projectionTime / timeStep) * timeStep
  for sec in range(0, timeTicks, timeStep):
    time = currTime + timedelta(0, sec)
    mvAvgCurveTimes.append(time)
  
  
  # Calculate moving averages of sleep times
  sleepDurationTicks = int(sleepAvgDuration / timeStep)
  sleepDurations = list()
  # The most recent sleep log before the start of our averaging interval
  lastStartIdx = 0
  # The most recent sleep log before the end of our averaging interval
  lastEndIdx = 0
  # The time we've slept in the current averaging interval
  sleepDur = 0
  
  for i in range(0, len(sleepTimes)):
    if sleepTimes[i][0] > startTime - timedelta(0, sleepAvgDuration):
      # We initialize the start and end indices at the same index, then we
      # don't advance the start index until the end index is a full interval away.
      lastStartIdx = i - 1
      lastEndIdx = i - 1
      break
  
  #print("Sleep moving average start, end index", lastStartIdx, lastEndIdx)
  
  lowSleepRanges = list()
  lowSleepStart = 0
  #print("len(sleepTimes):", len(sleepTimes))
  #print("len(mvAvgCurveTimes):", len(mvAvgCurveTimes))
  for i in range(0, len(mvAvgCurveTimes)):
    if lastEndIdx + 1 < len(sleepTimes) and mvAvgCurveTimes[i] > sleepTimes[lastEndIdx + 1][0]:
      lastEndIdx += 1
    if lastStartIdx + 1 < len(sleepTimes) and \
            i - sleepDurationTicks >= 0 and \
            mvAvgCurveTimes[i - sleepDurationTicks] > sleepTimes[lastStartIdx + 1][0]:
      lastStartIdx += 1
    # If the last end index is even, we're in a sleep period
    if lastEndIdx / 2.0 == int(lastEndIdx / 2) and sleepTimes[lastEndIdx + 1][1] != wakePoor:
      sleepDur += timeStep
    if i >= sleepDurationTicks:
      if lastStartIdx / 2.0 == int(lastStartIdx / 2) and sleepTimes[lastStartIdx + 1][1] != wakePoor:
        sleepDur -= timeStep
    sleepDurMovAvgTime = 24 * sleepDur / sleepAvgDuration
    sleepDurations.append(sleepDurMovAvgTime)
    if sleepDurMovAvgTime <= lowSleepLimit and lowSleepStart == 0:
      lowSleepStart = mvAvgCurveTimes[i]
    if sleepDurMovAvgTime > lowSleepLimit and lowSleepStart != 0:
      lowSleepRanges.append([lowSleepStart.replace(microsecond=0), mvAvgCurveTimes[i].replace(microsecond=0)])
#      lowSleepRanges.append([lowSleepStart, mvAvgCurveTimes[i]])
      lowSleepStart = 0
  
  #for i in range(0, len(mvAvgCurveTimes), 100):
  #  print("t, v", mvAvgCurveTimes[i], sleepDurations[i])
  
  return mvAvgCurveTimes, sleepDurations, lowSleepRanges
#### End ####


#### Start ####
def plotSleepWakeBars(plt, sleepTimes, startTime, endTime, maxLim):
  print("Plotting sleep/wake intervals", datetime.now())

  if writeNotableDates:
    notableDatesPath = plotDir + "/" + notableDatesPathname
    if not os.path.isdir(notableDatesPath):
      os.makedirs(notableDatesPath)
    notableDatesFilename = "{} {}.csv".format(notableDatesHeader, datetime.now().strftime("%Y-%m-%d"))
  #  notableDatesFilename = "Notable Dates {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    notableDates = open(notableDatesPath + "/" + notableDatesFilename, "a+")
    notableDatesWriter = csv.writer(notableDates, lineterminator="\n")

  plt.ylim([0, maxLim])

  startIndex = -1
  endIndex = len(sleepTimes)
  for i in range(0, len(sleepTimes), 2):
    if sleepTimes[i][0] >= startTime:
      startIndex = i
      break
  if startIndex == -1:
    print("plotSleepWakeBars: no data after: ", startTime)
    return
  # Should start on an even numbered row (starting at 0)
  if int(startIndex / 2) != startIndex / 2:
    startIndex -= 1
  # If the previous sleep/wake interval straddles the start time, back up to that interval
  if startIndex >= 2 and sleepTimes[startIndex - 2][0] <= startTime and sleepTimes[startIndex - 1][0] >= startTime:
    startIndex -= 2

  for i in range(startIndex, len(sleepTimes), 2):
    if sleepTimes[i][0] > endTime:
      endIndex = i
      break
  # Should end on an odd numbered row
  if endIndex > 2 and int(endIndex / 2) == endIndex / 2:
    endIndex -= 1 

  print("Sleep startIndex, endIndex", startIndex, endIndex)
  
  sleepTimeStartIdx = startIndex
  sleepTimeEndIdx = startIndex + 1
  wakeTimeStartIdx = startIndex + 1
  wakeTimeEndIdx = startIndex + 2

#   sleepTimeStart = sleepTimes[startIndex][0]
#   sleepTimeEnd = sleepTimes[startIndex + 1][0]
#   wakeTimeStart = sleepTimes[startIndex + 1][0]
#   wakeTimeEnd = sleepTimes[startIndex + 2][0]

  ax = plt.gca()
  
  containsPoorInterval = False

  for i in range(startIndex, endIndex, 2):
    color = ()
    if len(sleepTimes) <= i + 1:
      print("Probably forgot to log a \"wake\", index: ", i)
      print("exiting....")
      exit(1)
    if wakePoor == sleepTimes[i + 1][1]:
      color = (0.25, 0.25, 0.25, 0.20)
#      color = (0.25, 0.25, 0.25, 0.50)
    elif wakeMedium == sleepTimes[i + 1][1]:
      # "sound" and "medium" are effectively the same now
      color = (0.25, 0.25, 0.25, 0.50)
#      color = (0.25, 0.25, 0.25, 0.75)
    elif wakeSound == sleepTimes[i + 1][1]:
      color = (0.25, 0.25, 0.25, 0.75)
    plotSleepBar(plt, sleepTimes, i, color, 1)
    if (endTime - startTime).total_seconds() / (24 * 60 * 60) <= maxDaysForTimeLables:
    ##  plt.xticks(list(plt.xticks()[0]) + [sleepTimes[i].value, sleepTimes[i + 1].value])
    ##  plt.text(sleepTimes[i], 0, sleepTimes[i], fontsize="small", horizontalalignment="center", verticalalignment="top")
    #  plt.text(sleepTimes[i][0], 0, sleepTimes[i][0].strftime("%m-%d %H:%M"),
      if sleepTimes[i][0] > startTime:
        plt.text(sleepTimes[i][0], 0, sleepTimes[i][0].strftime("%H:%M"),
                 fontdict={"size": "small"}, horizontalalignment="center", verticalalignment="center", rotation=60)
        if sleepTimes[i][3] == None:
          logStr = ""
        else:
          logStr = sleepTimes[i][3]
        plt.text(0.005, 0.96 - 0.015 * (i - startIndex),
                 "{:%m-%d %H:%M}  {}".format(sleepTimes[i][0], sleepTimes[i][1]),
                  fontdict={"size": "small", "fontweight": "bold"}, transform=ax.transAxes)
        plt.text(0.095, 0.96 - 0.015 * (i - startIndex),
                 "{}".format(logStr),
                  fontdict={"size": "small", "fontweight": "bold"}, transform=ax.transAxes)

      if i < len(sleepTimes) - 1 and sleepTimes[i + 1][0] <= endTime:
        plt.text(sleepTimes[i + 1][0], maxLim, sleepTimes[i + 1][0].strftime("%H:%M"),
                 fontsize="small", horizontalalignment="center", verticalalignment="center", rotation=60)
        if sleepTimes[i + 1][3] == None:
          logStr = ""
        else:
          logStr = sleepTimes[i + 1][3]
        plt.text(0.005, 0.945 - 0.015 * (i - startIndex),
                 "{:%m-%d %H:%M}  {}".format(sleepTimes[i + 1][0], sleepTimes[i + 1][1]),
                  fontdict={"size": "small", "fontweight": "bold"}, transform=ax.transAxes)
        plt.text(0.095, 0.945 - 0.015 * (i - startIndex),
                 "{}".format(logStr),
                  fontdict={"size": "small", "fontweight": "bold"}, transform=ax.transAxes)
        
        # Only plot time interval values for medium sleep intervals
        if wakeMedium == sleepTimes[i + 1][1]:
          sleepTimeStartIdx = i
          sleepTimeEndIdx = i + 1
          sleepDuration = round((sleepTimes[sleepTimeEndIdx][0] - sleepTimes[sleepTimeStartIdx][0]).total_seconds() / 3600, 1)
          loc = sleepTimes[sleepTimeStartIdx][0] + (sleepTimes[sleepTimeEndIdx][0] - sleepTimes[sleepTimeStartIdx][0])/2
          if loc > startTime and loc < endTime:
            plt.text(loc, plt.ylim()[1]/8, sleepDuration,
                     fontsize="medium", horizontalalignment="center", verticalalignment="center", fontweight="normal")

      if i < len(sleepTimes) - 3:

        # If we don't have a poor sleep interval coming up after the current interval, then plot it
        # If we do have a poor sleep interval coming up next, then don't plot anything, and the sleep interval plot
        # block will set the proper start time, but not reseting it on the poor sleep interval 
        if wakePoor != sleepTimes[i + 3][1]:
          wakeTimeStartIdx = sleepTimeEndIdx
          wakeTimeEndIdx = i + 2
          wakeDuration = round((sleepTimes[wakeTimeEndIdx][0] - sleepTimes[wakeTimeStartIdx][0]).total_seconds() / 3600, 1)
          loc = sleepTimes[wakeTimeStartIdx][0] + (sleepTimes[wakeTimeEndIdx][0] - sleepTimes[wakeTimeStartIdx][0])/2
          fontWeight = "normal"
          color = "k"
          if containsPoorInterval:

            dxLeft = md.date2num(loc) - md.date2num(sleepTimes[wakeTimeStartIdx][0])
#            startLocationLeft = loc - md.num2timedelta(dxLeft * 0.15)
            startLocationLeft = loc

            dxRight = md.date2num(sleepTimes[wakeTimeEndIdx][0]) - md.date2num(loc)
#            startLocationRight = loc + md.num2timedelta(dxRight * 0.15)
            startLocationRight = loc

            plt.arrow(startLocationLeft, plt.ylim()[1]/7.25, -dxLeft * 0.95, 0,
                      length_includes_head=True, head_width=0.25, head_length=0.035)
            plt.arrow(startLocationRight, plt.ylim()[1]/7.25, dxRight * 0.95, 0,
                      length_includes_head=True, head_width=0.25, head_length=0.035)

            if writeNotableDates and wakeDuration > 18:
              notableDates.write("{}: {}\n".format(sleeplessIntervalDelim, wakeDuration))
              for j in range(sleepTimeStartIdx, i + 3):
                notableDatesWriter.writerow(sleepTimes[j])

            # for the time text, out side of this "if"            
            fontWeight = "bold"
            color = "r"

          plt.text(loc, plt.ylim()[1]/8, wakeDuration,
                   fontsize="medium", horizontalalignment="center", verticalalignment="center", fontweight=fontWeight, color=color)
          
          containsPoorInterval = False
        else:
          containsPoorInterval = True

  sleepDuration = round((datetime.now() - sleepTimes[-1][0]).total_seconds() / 3600, 1)
  loc = sleepTimes[-1][0] + (datetime.now() - sleepTimes[-1][0])/2
  if loc < endTime:
    plt.text(loc, plt.ylim()[1]/8, sleepDuration,
             fontsize="medium", horizontalalignment="center", verticalalignment="center", fontweight="normal")
  print("Done Plotting sleep/wake intervals", datetime.now())
  
  if writeNotableDates:
    notableDates.close()
  
  return
#### End ####

#### Start ####
def plotSleepBar(plt, sleepTimes, i, color, alpha):
  start_1 = sleepTimes[i][0]
  start_2 = start_1
  end_1 = sleepTimes[i+1][0]
  end_2 = end_1

  print("plotting sleep bar from: {} to {}".format(sleepTimes[i][0], sleepTimes[i+1][0]))

  if end_2 - start_1 < timedelta(0, 90 * 60):
    width = (end_2 - start_1) / 3
  else:
    width = timedelta(0, 30 * 60)
  if smokeKey.lower() in str(sleepTimes[i][3]).lower() or potSmokeKey.lower() in str(sleepTimes[i][3]).lower():
      start_2 = start_1 + width
  if smokeKey.lower() in str(sleepTimes[i + 1][3]).lower() or potSmokeKey.lower() in str(sleepTimes[i + 1][3]).lower():
      end_1 = end_2 - width
 
  if start_1 != start_2:
    if potSmokeKey.lower() in str(sleepTimes[i][3]).lower():
      boarderColor = potSmokeColor
    else:
      boarderColor = smokeSleepBorderColor
    plt.fill_between([start_1, start_2], plt.ylim()[1], color=boarderColor, alpha=alpha)
  if end_2 != end_1:
    if potSmokeKey.lower() in str(sleepTimes[i + 1][3]).lower():
      boarderColor = potSmokeColor
    else:
      boarderColor = smokeSleepBorderColor
    plt.fill_between([end_1, end_2], plt.ylim()[1], color=boarderColor, alpha=alpha)

  plt.fill_between([start_2, end_1], plt.ylim()[1], color=color)
#  plt.fill_between([sleepTimes[i][0], sleepTimes[i+1][0]], plt.ylim()[1], color=color)

  return
#### End ####

#### Start ####
def plotSmokeTimes(plt, smokeTimes, startTime, endTime, color):
  startIndex = 0
  endIndex = len(smokeTimes)
  for i in range(0, len(smokeTimes)):
    if smokeTimes[i] > startTime:
      startIndex = i
      break
  for i in range(startIndex, len(smokeTimes)):
    if smokeTimes[i] > endTime:
      endIndex = i
      break

  print("Smokes startIndex, endIndex", startIndex, endIndex)

  print("Plotting Smoke lines", datetime.now())
  for smokeTime in smokeTimes[slice(startIndex, endIndex)]:
    plt.axvline(smokeTime, color=color)
  print("Done Plotting Smoke lines", datetime.now())

  return
#### End ####

#### Start ####
def writeLowSleepRanges(lowSleepRanges):
  if not writeNotableDates:
    return

  notableDatesPath = plotDir + "/" + notableDatesPathname
  if not os.path.isdir(notableDatesPath):
    os.makedirs(notableDatesPath)
  notableDatesFilename = "{} {}.csv".format(lowSleepHeader, datetime.now().strftime("%Y-%m-%d"))
#  notableDatesFilename = "Notable Dates {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
  notableDates = open(notableDatesPath + "/" + notableDatesFilename, "a+")
  notableDatesWriter = csv.writer(notableDates, lineterminator="\n")

  for lowSleepRange in lowSleepRanges:
    notableDatesWriter.writerow(lowSleepRange)


# #               notableDates.write("{}: {}\n".format(sleeplessIntervalDelim, wakeDuration))
#               for j in range(sleepTimeStartIdx, i + 3):
#                 notableDatesWriter.writerow(sleepTimes[j])

  notableDates.close()

#### End ####


#### Start ####
def calculateDayMarkers(startTime, currTime, endTime, maxLim):
  dayMarkerTimes = list()
  markerLoc = list()
  timeTicks = int((endTime - startTime).total_seconds() / timeStep) * timeStep
  for sec in range(0, timeTicks, timeStep):
    time = startTime + timedelta(0, sec)
    if time.time().hour <= 18 and time.time().hour >= 6:
      continue
    dayMarkerTimes.append(time)
    markerLoc.append(maxLim * 0.98)

  return dayMarkerTimes, markerLoc
#### End ####

#### Start ####
def makeSleepPlot(startTime, currTime, endTime, sleepTimes, maxLim = 24, show_plot = True, rel_save_dir="."):

  print("Calculating Sleep Moving Averages", datetime.now())

  projectionTime = (endTime - currTime).total_seconds()

  # make a time-index list for sleep moving averages
  mvAvgCurveTimes, sleepDurations, lowSleepRanges = \
      calculateSleepData(sleepTimes, startTime, currTime, endTime, projectionTime, timeStep, sleepAvgDuration)
  
  print("Done Calculating Sleep Moving Averages", datetime.now())

  writeLowSleepRanges(lowSleepRanges)

#   for lowSleepRange in lowSleepRanges:
#     print(lowSleepRange)


  dayMarkerTimes, markerLoc = calculateDayMarkers(startTime, currTime, endTime, maxLim)

  # Now
  plt.axvline(currTime, color="k")

  # Sleep/wake intervals
  plotSleepWakeBars(plt, sleepTimes, startTime, endTime, maxLim)

  #  maxLim -- (float) the upper limit of the vertical (y) axis
  maxLimLeft = maxLim
  maxLimRight = maxLim
  plt.ylim([0, maxLimLeft])
  #print("maxLim ==", maxLim)
  #print("plt.ylim()[1]", plt.ylim()[1])

  # set the size of the plot in the plot window
#  plt.subplots_adjust(left=0.02, right=0.98, top=0.96, bottom=0.04)
  plt.subplots_adjust(left=0.03, right=0.97, top=0.94, bottom=0.07)
  ## For printing
  #fig = plt.figure(num=1, figsize=((1920 - 5) / 80 / 2.3, 10))
  #plt.subplots_adjust(left=0.05, right=0.96)

#  plt.ylabel("{} Day Average Sleep".format(int(sleepAvgDuration / (24 * 60 * 60))))

  # Fix up the axes
  ax = plt.gca()
#  ax.set_ylim(0, maxLimLeft)

#  axSleep.plot(mvAvgCurveTimes, sleepDurations, "k--")
  
  # Plot the moving average curve, coloring the line by whether or not sleep is below the low limit
  currColor = normalSleepColor if sleepDurations[0] > lowSleepLimit else lowSleepColor
  colorChangeIdx = list()
  colorChangeIdx.append(0)
  lastVal = sleepDurations[0]

  for i in range(0, len(mvAvgCurveTimes)):
    if sleepDurations[i] > lowSleepLimit and lastVal > lowSleepLimit:
      continue
    elif sleepDurations[i] > lowSleepLimit and lastVal <= lowSleepLimit:
      colorChangeIdx.append(i)
    elif sleepDurations[i] <= lowSleepLimit and lastVal <= lowSleepLimit:
      continue
    elif sleepDurations[i] <= lowSleepLimit and lastVal > lowSleepLimit:
      colorChangeIdx.append(i)
    lastVal = sleepDurations[i]
  colorChangeIdx.append(len(mvAvgCurveTimes))

  # Create an axis for sleep times
  axSleep = ax.twinx() # right side axis annotation

  firstIdx = colorChangeIdx[0]
  for i in colorChangeIdx[1:]:
    axSleep.plot(mvAvgCurveTimes[firstIdx : i], sleepDurations[firstIdx : i], currColor)
    if currColor == normalSleepColor:
      currColor = lowSleepColor
    else:
      currColor = normalSleepColor
    firstIdx = i
  
  axSleep.plot(dayMarkerTimes, markerLoc, ".b")
  axSleep.set_ylim(0, maxLimRight)
  sleepMajorLocator = MultipleLocator(4)
  sleepMinorLocator = MultipleLocator(2)
  axSleep.yaxis.set_major_locator(sleepMajorLocator)
  axSleep.yaxis.set_minor_locator(sleepMinorLocator)
  ax.yaxis.set_major_locator(sleepMajorLocator)
  ax.yaxis.set_minor_locator(sleepMinorLocator)
  #axSleep.set_yticks([0, 8, 16, 24])
  #axSleep.grid(b=True, which=u'both', axis='y', color='k', linestyle='--')
  axSleep.grid(b=True, which=u'both', axis='y', color='k')
#  ax.grid(b=True, which=u'both', axis='y', color='k')

#  plt.xlim(xmin=startTime)
  plt.xlim(startTime, endTime)
  #plt.ylim(ymax=650)

  # Set the max dose axis value
  #plt.minorticks_on()

  timePeriodDays = int((currTime - startTime).total_seconds() / (60 * 60 * 24))

  plt.suptitle("170 Lake St. Nicotine/Cigarette Fixes and Sleep", fontsize=16, y=1.0)
#  plt.title(r"For the $\bf%s$ day period: $\bf%s$ to $\bf%s$" % (timePeriodDays,
#             startTime.strftime("%Y-%m-%d"), endTime.strftime("%Y-%m-%d")), y=1.0)
  plt.title(r"For the $\bf%s$ day period: $\bf%s$ to $\bf%s$" % (timePeriodDays,
             startTime.strftime("%Y-%m-%d"), endTime.strftime("%Y-%m-%d")), y=1.015)

#  plt.xlabel("Date and Sleep/Wake Times")
  ax.set_xlabel("Fix Date/Time and Sleep/Wake Intervals")
  # have to do this to get the label on the left hand side, after mucking with both sides above
  ax.set_ylabel(("{} Day Average Sleep".format(int(sleepAvgDuration / (24 * 60 * 60)))))

  ax.relim()
  ax.autoscale_view(True, True, True)
  #ax.tick_params(axis='x', which='minor', bottom='off')
  #ax.tick_params(axis='y', which='minor', bottom='on')
  ax.grid(b=True, which=u'both', color='b', linestyle='-.')

  if show_plot:
    plt.show()
  else:
    plotPath = plotDir + "/" + rel_save_dir
    if not os.path.isdir(plotPath):
      os.makedirs(plotPath)
    # must happen before plt.show()
    plt.savefig("%s/SleepAndSmoke %s to %s.png" % (plotPath, startTime.strftime("%Y-%m-%d"), endTime.strftime("%Y-%m-%d")), dpi=300)

# to make jpgs:
# import Image
# Image.open('testplot.png').save('testplot.jpg','JPEG')
# or
# pip install pillow
 
  plt.clf()
  plt.cla()

  return plt
#### End ####


#### Start ####
def makeSleepSmokePlot(startTime, currTime, endTime, smokeTimes, potSmokeTimes, sleepTimes, timeStep, sleepAvgDuration, maxLim = 24,
                       show_plot = True, rel_save_dir="."):

  if startTime > smokeTimes[-1] and startTime > potSmokeTimes[-1] and startTime > sleepTimes[-1][0]:
    print("makeSleepSmokePlot: no data after: ", startTime)
    return

  # todo: figure out how to set window location
  # Set the size and location of the plot window (must happen before any actuall plotting, apparently)
  fig = plt.figure(num=1, figsize=((1920 - 5) / 80, 10))
  # set the size of the plot in the plot window
#  plt.subplots_adjust(left=0.02, right=0.98, top=0.96, bottom=0.04)
  ## For printing
  #fig = plt.figure(num=1, figsize=((1920 - 5) / 80 / 2.3, 10))
  #plt.subplots_adjust(left=0.05, right=0.96)

  ### Smokes
  plotSmokeTimes(plt, smokeTimes, startTime, endTime, color=tabaccoSmokeColor)
# 
#   #### Pot Smokes
  plotSmokeTimes(plt, potSmokeTimes, startTime, endTime, color=potSmokeColor)

  finishedPlt = makeSleepPlot(startTime, currTime, endTime, sleepTimes, maxLim, show_plot, rel_save_dir)

  return finishedPlt
#### End ####


#######################################################################################################################
## End Functions
#######################################################################################################################





