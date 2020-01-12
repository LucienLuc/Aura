import os, sys

sys.path.append("./atlastk")
sys.path.append("../atlastk")

import atlastk as Atlas
import time
import alarm
import arduino
import video_comparison as vc
import datetime

head = """
<title>GUI</title>
"""

body = """
<div style="display: table; margin: 50px auto auto auto;">
<div id = curralarm style = "display: flex; justify-content: space-around; margin: 5px auto auto auto;"> No alarm set</div>
<div style="display: table; margin: 50px auto auto auto;">
<select id = hour>
	<option value = None> Hour </option>
	<option value = 1> 1 </option>
	<option value = 2> 2 </option>
	<option value = 3> 3 </option>
	<option value = 4> 4 </option>
	<option value = 5> 5 </option>
	<option value = 6> 6 </option>
	<option value = 7> 7 </option>
	<option value = 8> 8 </option>
	<option value = 9> 9 </option>
	<option value = 10> 10 </option>
	<option value = 11> 11 </option>
	<option value = 12> 12 </option>
</select>
:
<select id = minute>
	<option value = None> Minute </option>
	<option value = 00> 00 </option>
	<option value = 05> 05 </option>
	<option value = 10> 10 </option>
	<option value = 15> 15 </option>
	<option value = 20> 20 </option>
	<option value = 25> 25 </option>
	<option value = 30> 30 </option>
	<option value = 35> 35 </option>
	<option value = 40> 40 </option>
	<option value = 45> 45 </option>
	<option value = 50> 50 </option>
	<option value = 55> 55 </option>
</select>
<select id = ampm>
	<option value = "AM"> AM </option>
	<option value = "PM"> PM </option>
</select>
<div style="display: flex; justify-content: space-around; margin: 5px auto auto auto;" >
<button data-xdh-onevent="Set">Set Alarm</button>
</div>
<div style="display: table; margin: 50px auto auto auto;">
"""


#global variables
alarmtime = 0
isCalibrated = False

#private states
inBed = False
isAsleep = False
timeIntoBed = 0
timeInSleep = 0
waketime = 0

def run():
	global waketime
	vc.start_video_stream()
	waketime = alarm.getWakeUpDate(alarmtime)
	checkInBed()
	inBedNotSleeping()
	alarmControl()

#make sure that the person is in the bed
def checkInBed():
	global inBed, timeIntoBed
	while not inBed:
		inBed = vc.run()
	timeIntoBed = timeIntoBed = datetime.datetime.now()

def inBedNotSleeping():
	global isAsleep, timeInSleep, timeIntoBed
	while inBed and not isAsleep:
		tempInBed = vc.run()
		temp = alarm.getDateDifference(timeIntoBed)
		print(temp, timeIntoBed)
		if datetime.timedelta(minutes = alarm.SLEEP_OFFSET) < temp:
			isAsleep = True
			timeInSleep = datetime.datetime.now()
			break
		if not tempInBed:
			timeIntoBed = datetime.datetime.now()

def alarmControl():
	remwake = alarm.calculateREMwake(timeInSleep, waketime)
	while inBed and isAsleep:
		print(remwake, '<=', datetime.datetime.now())
		if remwake <= datetime.datetime.now():
			stateOutBed = vc.calibrate()
			arduino.alarm()
			#while not stateOutBed:
			#	stateOutBed = vc.run()
			vc.calibrate()
			break

#returns minutes past 12:00 AM
def convertTime(hour,minute,ampm):
	res = 0
	if(ampm == "PM" and hour != "12"):
		hour = int(hour) + 12
	elif(ampm == "AM" and hour == "12"):
		hour = 0
	res = int(hour) * 60
	res = int(res) + int(minute)
	return res

def acConnect(dom):
	dom.setLayout("", body)
	dom.focus("curralarm")

def acSet(dom):
	if(dom.getContent("hour") == "None" or dom.getContent("minute") == "None"):
		dom.alert("Please select a valid time")
	else:
		hour = dom.getContent("hour")
		minute = dom.getContent("minute")
		ampm = dom.getContent("ampm")
		dom.setContent("curralarm", "Alarm set to " + hour + ":" + minute + " " + ampm)
		global alarmtime 
		alarmtime = convertTime(hour,minute,ampm)
		run()

callbacks = {
	"": acConnect,
	"Set": acSet,
}

#finds port that arduino is connected to
port = arduino.findPort()
'''
if(not arduino.testArduinoConnection()): 
	exit()
	'''
Atlas.launch(callbacks, None, head)
