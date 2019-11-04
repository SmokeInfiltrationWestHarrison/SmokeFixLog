###
# Make and save images to disk of plots of sleep intervals and smoke times for all data, 3 months at a time
###

from datetime import datetime, timedelta
import WorkbookLoaders as wl
import SmokeAndSleep as sas
import dateRanges as dr

###
## Parameters
###
 
## How much past time to include in the sleep moving average
sleepAvgDuration = 2 * 24 * 60 * 60  # seconds
## time step between moving average points/calculations
timeStep = 180  # seconds


#######################################################################################################################
## Functions
#######################################################################################################################


#### Start ####
def plotThreeMonthCharts(smokeTimes, potSmokeTimes, sleepTimes, rel_save_dir="Sleep-Wake-Smoke 3Monthly"):
  for rng in dr.monthIntervals(month_step = 3):
    print("\nPlotting Range: ", rng)
    startTime = rng[0]
    currTime = endTime = rng[1]
    finishedPlt = sas.makeSleepSmokePlot(startTime, currTime, endTime, smokeTimes, potSmokeTimes, sleepTimes, 
                                         timeStep, sleepAvgDuration, maxLim = 24, show_plot = False, rel_save_dir=rel_save_dir)
  print("DONE")
  return finishedPlt
#### End ####

#### Start ####
def plotMonthlyCharts(smokeTimes, potSmokeTimes, sleepTimes, rel_save_dir="Sleep-Wake-Smoke Monthly"):
  for rng in dr.monthIntervals(month_step = 1):
    print("\nPlotting Range: ", rng)
    startTime = rng[0]
    currTime = endTime = rng[1]
    finishedPlt = sas.makeSleepSmokePlot(startTime, currTime, endTime, smokeTimes, potSmokeTimes, sleepTimes, 
                                         timeStep, sleepAvgDuration, maxLim = 24, show_plot = False, rel_save_dir=rel_save_dir)
  print("DONE")
  return finishedPlt
#### End ####

#### Start ####
def plotWeeklyCharts(smokeTimes, potSmokeTimes, sleepTimes, rel_save_dir="Sleep-Wake-Smoke Weekly"):
  for rng in dr.weekIntervals():
    print("\nPlotting Range: ", rng)
    startTime = rng[0]
    currTime = endTime = rng[1]
    finishedPlt = sas.makeSleepSmokePlot(startTime, currTime, endTime, smokeTimes, potSmokeTimes, sleepTimes, 
                                         timeStep, sleepAvgDuration, maxLim = 24, show_plot = False, rel_save_dir=rel_save_dir)
  print("DONE")
  return finishedPlt
#### End ####

#### Start ####
def plotAllData(smokeTimes, potSmokeTimes, sleepTimes, rel_save_dir="Sleep-Wake-Smoke All Data"):

  startTime = smokeTimes[0]
  if startTime > potSmokeTimes[0]: startTime = potSmokeTimes[0]
  if startTime > sleepTimes[0][0]: startTime = sleepTimes[0][0]

  endTime = smokeTimes[-1]
  if endTime < potSmokeTimes[-1]: endTime = potSmokeTimes[-1]
  if endTime < sleepTimes[-1][0]: endTime = sleepTimes[-1][0]

  currTime = endTime 

  finishedPlt = sas.makeSleepSmokePlot(startTime, currTime, endTime, smokeTimes, potSmokeTimes, sleepTimes, 
                                       timeStep, sleepAvgDuration, maxLim = 24, show_plot = False, rel_save_dir=rel_save_dir)
  print("DONE")
  return finishedPlt
#### End ####

#### Start ####
def plotNotableDates(smokeTimes, potSmokeTimes, sleepTimes, rel_save_dir="Sleep-Wake-Smoke Notable Dates"):
  day = timedelta(1)
  for rng in dr.notableIntervals():
    print("\nPlotting Range: ", rng)
#    startTime = datetime(rng[0].year, rng[0].month, rng[0].day) - day
    startTime = datetime(rng[0].year, rng[0].month, rng[0].day)
    currTime = endTime = datetime(rng[1].year, rng[1].month, rng[1].day) + day
    print("Plotting Rounded Range: ", (startTime, endTime))
    finishedPlt = sas.makeSleepSmokePlot(startTime, currTime, endTime, smokeTimes, potSmokeTimes, sleepTimes, 
                                         timeStep, sleepAvgDuration, maxLim = 24, show_plot = False, rel_save_dir=rel_save_dir)
  print("DONE")
  return finishedPlt
#### End ####

#### Start ####
def plotCustomRanges(smokeTimes, potSmokeTimes, sleepTimes, rel_save_dir="Sleep-Wake-Smoke Custom Intervals"):
  for rng in dr.customIntervals():
    print("\nPlotting Range: ", rng)
    startTime = rng[0]
    currTime = endTime = rng[1]
    finishedPlt = sas.makeSleepSmokePlot(startTime, currTime, endTime, smokeTimes, potSmokeTimes, sleepTimes, 
                                         timeStep, sleepAvgDuration, maxLim = 24, show_plot = False, rel_save_dir=rel_save_dir)
  print("DONE")
  return finishedPlt
#### End ####


#######################################################################################################################
## End Functions
#######################################################################################################################

### Extract Sleep Times
print("Extracting", datetime.now())
sleepTimes, smokeTimes, smokes, potSmokeTimes, potSmokes = wl.loadWorkbooks(wl.logSet)
print("Done Extracting", datetime.now())

# Do the plotting

#plotThreeMonthCharts(smokeTimes, potSmokeTimes, sleepTimes)

#plotMonthlyCharts(smokeTimes, potSmokeTimes, sleepTimes)

#plotWeeklyCharts(smokeTimes, potSmokeTimes, sleepTimes)

#plotAllData(smokeTimes, potSmokeTimes, sleepTimes)

plotNotableDates(smokeTimes, potSmokeTimes, sleepTimes)

#plotCustomRanges(smokeTimes, potSmokeTimes, sleepTimes)




















