###
# Make a plot of sleep intervals and smoke times up to the current time
###

from datetime import datetime, timedelta
import WorkbookLoaders as wl
import SmokeAndSleep as sas

###
## Parameters
###

## How far into the future we project moving averages
projectionTime = 24 * 60 * 60  # seconds
#projectionTime = 0 # seconds
#projectionTime = 0 * 60 * 60  # seconds
## How much past time to include in the sleep moving average
sleepAvgDuration = 2 * 24 * 60 * 60  # seconds
## time step between moving average points/calculations
timeStep = 180  # seconds
## For graphs that end at the present, how far back they should go
dayRange = 7  # days

###
## Define when the graph will start and end
###
#currTime = datetime.now() + timedelta(1, 6 * 60 * 60)
currTime = datetime.now()
startTime = currTime - timedelta(dayRange)
endTime = currTime + timedelta(0, projectionTime)

# startTime = datetime.strptime("2019-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
# endTime = datetime.strptime("2019-01-31 00:00:00", "%Y-%m-%d %H:%M:%S")
# #endTime = datetime.now()
# currTime = endTime

# todo: eliminate overlap in the data files
#startTime = datetime.strptime("2017-05-25 03:47:49", "%Y-%m-%d %H:%M:%S")
#endTime = datetime.strptime("2017-05-27 20:11:44", "%Y-%m-%d %H:%M:%S")
#currTime = endTime

# # rows 48 to 69 in MedLog_201706_ForGampopa.xlsm
# # (has duplicate data from previous spreadsheet)
#startTime = datetime.strptime("2017-05-25 00:00:00", "%Y-%m-%d %H:%M:%S")
#endTime = datetime.strptime("2017-05-28 00:00:00", "%Y-%m-%d %H:%M:%S")
#currTime = endTime

# # (has duplicate data from previous spreadsheet)
#startTime = datetime.strptime("2017-05-17 00:00:00", "%Y-%m-%d %H:%M:%S")
#endTime = datetime.strptime("2017-06-06 00:00:00", "%Y-%m-%d %H:%M:%S")
#currTime = endTime

#startTime = datetime.strptime("2017-03-28 00:00:00", "%Y-%m-%d %H:%M:%S")
#endTime = datetime.strptime("2017-06-26 00:00:00", "%Y-%m-%d %H:%M:%S")
#currTime = endTime

#startTime = datetime.strptime("2016-03-18 00:00:00", "%Y-%m-%d %H:%M:%S")
#endTime = datetime.strptime("2016-03-25 00:00:00", "%Y-%m-%d %H:%M:%S")
#currTime = endTime

# # rows 935 to 955 in MedLog_201706_ForGampopa.xlsm
# startTime = datetime.strptime("2017-10-10 00:00:00", "%Y-%m-%d %H:%M:%S")
# endTime = datetime.strptime("2017-10-15 00:00:00", "%Y-%m-%d %H:%M:%S")
# currTime = endTime

# # rows 1053 to 1088 in MedLog_201706_ForGampopa.xlsm
# # row 1079: 2017-11-10 19:49:10  Smoke    Pot Smoke, on and off all night
# startTime = datetime.strptime("2017-11-05 00:00:00", "%Y-%m-%d %H:%M:%S")
# endTime = datetime.strptime("2017-11-13 00:00:00", "%Y-%m-%d %H:%M:%S")
# currTime = endTime



print("startTime: ", startTime)
print("endTime: ", endTime)
print("currTime: ", currTime)




### Extract Sleep Times
print("Extracting", datetime.now())
#sleepTimes, smokeTimes, smokes, potSmokeTimes, potSmokes = wl.loadWorkbooksAsDicts(logSet, sleepKey, wakeKey, smokeKey, potSmokeKey)
#sleepTimes, smokeTimes, smokes, potSmokeTimes, potSmokes = wl.loadWorkbooks(wl.logSet, sas.sleepKey, sas.wakeKey, sas.smokeKey, sas.potSmokeKey)
sleepTimes, smokeTimes, smokes, potSmokeTimes, potSmokes = wl.loadWorkbooks(wl.logSet)
print("Done Extracting", datetime.now())

finishedPlt = sas.makeSleepSmokePlot(startTime, currTime, endTime,
                                     smokeTimes, potSmokeTimes, sleepTimes, 
                                     timeStep, sleepAvgDuration,
                                     maxLim = 24, show_plot = True)

































