import csv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import SmokeAndSleep as sas



#######################################################################################################################
## Functions
#######################################################################################################################


#### Start ####
def customIntervals():

#   dateRanges = [
#     (datetime(2016, 1, 1), datetime(2016, 4, 1)),
#     (datetime(2016, 4, 1), datetime(2016, 7, 1)),
#     (datetime(2016, 7, 1), datetime(2016, 10, 1)),
#     (datetime(2016, 10, 1), datetime(2017, 1, 1)),
# 
#     (datetime(2017, 1, 1), datetime(2017, 4, 1)),
#     (datetime(2017, 4, 1), datetime(2017, 7, 1)),
#     (datetime(2017, 7, 1), datetime(2017, 10, 1)),
#     (datetime(2017, 10, 1), datetime(2018, 1, 1)),
# 
#     (datetime(2018, 1, 1), datetime(2018, 4, 1)),
#     (datetime(2018, 4, 1), datetime(2018, 7, 1)),
#     (datetime(2018, 7, 1), datetime(2018, 10, 1)),
#     (datetime(2018, 10, 1), datetime(2019, 1, 1)),
# 
#     (datetime(2019, 1, 1), datetime(2019, 4, 1)),
#     (datetime(2019, 4, 1), datetime(2019, 7, 1)),
#     (datetime(2019, 7, 1), datetime(2019, 10, 1)),
#     (datetime(2019, 10, 1), datetime(2020, 1, 1)),
# 
#   ]

  dateRanges = [
    (datetime(2017, 10, 8, 2, 22, 29), datetime(2017, 10, 11)),
    (datetime(2016, 9, 28), datetime(2016, 10, 3)),
    (datetime(2016, 10, 24), datetime(2016, 10, 30)),
  ]

  for dateRange in dateRanges:
    yield dateRange

  return
#### End ####

#### Start ####
def monthIntervals_old(start_year=2016, start_month=1, start_day=1, month_step=3, end_date=datetime(2020, 1, 1)):

  year = start_year
  month = start_month
  day = start_day
  start = datetime(year, month, day)
  
  while start < end_date:
    month += month_step
    if month > 12:
      month = 1
      year += 1
      end = datetime(year, month, day)
    end = datetime(year, month, day)
    yield (start, end)
    start = datetime(year, month, day)
    
  return
#### End ####

#### Start ####
def monthIntervals(start_date=datetime(2016, 1, 1), end_date=datetime(2020, 1, 1), month_step = 3):

  start = start_date

  while start < end_date:
    end = start + relativedelta(months=month_step)
    yield (start, end)
    start = end

  return
#### End ####

#### Start ####
def weekIntervals(start_date=datetime(2016, 1, 1), end_date=datetime(2020, 1, 1), week_step = 1):

  start = start_date
  
  while start < end_date:
    end = start + relativedelta(weeks=week_step)
    yield (start, end)
    start = end

  return
#### End ####

#### Start ####
def notableIntervals():

  end = 0
  day = timedelta(1)

  notableDatesPath = sas.plotDir + "/" + sas.notableDatesPathname
#  notableDatesFilename = "{} {}.csv".format(sas.notableDatesHeader, datetime.now().strftime("%Y-%m-%d"))
  notableDatesFilename = "{} {}.csv".format(sas.notableDatesHeader, "2019-10-02")
  with open(notableDatesPath + "/" + notableDatesFilename, "r") as file:
    reader = csv.reader(file)
    
    row = next(reader)
    row = next(reader)
    start = row[0]

    for row in reader:

      if sas.sleeplessIntervalDelim in row[0]:
#        yield (datetime.strptime(start, "%Y-%m-%d %H:%M:%S") - day, datetime.strptime(end, "%Y-%m-%d %H:%M:%S") + day)
        yield (datetime.strptime(start, "%Y-%m-%d %H:%M:%S"), datetime.strptime(end, "%Y-%m-%d %H:%M:%S"))
        start = 0
      else:
        if start == 0:
          start = row[0]
        else:
          end = row[0]

#  yield (datetime.strptime(start, "%Y-%m-%d %H:%M:%S") - day, datetime.strptime(end, "%Y-%m-%d %H:%M:%S") + day)
  yield (datetime.strptime(start, "%Y-%m-%d %H:%M:%S"), datetime.strptime(end, "%Y-%m-%d %H:%M:%S"))
  
  return
#### End ####

#### Start ####

def testCustomIntervals():
  for rng in customIntervals():
    print("date range: ", rng)
#### End ####

#### Start ####
def testMonths():
  for rng in monthIntervals():
    print("month range: ", rng)
#### End ####

#### Start ####
def testWeeks():
  for rng in weekIntervals():
    print("week range: ", rng)
#### End ####

#### Start ####
def testNotableDates():
  for rng in notableIntervals():
    print("notable range: ", rng)
#### End ####


#######################################################################################################################
## End Functions
#######################################################################################################################



#testMonths()
#testWeeks()
#testNotableDates()
#testCustomIntervals()






