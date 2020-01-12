import datetime

REM_DURATION = 90
SLEEP_OFFSET = 1

def getMinutestoNormal(mins):
	minutes = mins % 60
	hours = mins // 60
	return hours, minutes

def normalToMinutes(hours, minutes):
	return hours * 60 + minutes

#returns datetime object, input minute time
def getWakeUpDate(alarmtime):
	hour, minute = getMinutestoNormal(alarmtime)
	currdate = datetime.datetime.today()
	dayoffset = 0 if currdate.hour < 12 else 1
	return datetime.datetime(currdate.year, currdate.month, currdate.day + dayoffset, 
							 hour = hour, minute = minute)

#returns time delta object, input datetimes
def getDateDifference(initialdate, currdate=None, reverse=False):
	if currdate == None:
		currdate = datetime.datetime.now()
	return currdate - initialdate if not reverse else initialdate - currdate

#return datetime object, input datetimes
def calculateREMwake(alarmtime, currdate=None):
	if currdate == None:
		currdate = datetime.datetime.now()
	timeDiff = currdate - alarmtime
	print(timeDiff)
	minutesDiff = normalToMinutes(0, timeDiff.seconds // 60)
	numREMcycles = minutesDiff // REM_DURATION
	print(numREMcycles * REM_DURATION)
	result = currdate - datetime.timedelta(minutes=numREMcycles * REM_DURATION)
	print(result)
	return result
