import serial
from serial.tools.list_ports import grep
import time

main_port = None

def findPort():
	global main_port
	ports = grep("usb")
	ports = list(ports)
	if (len(ports) == 0):
		ports = grep("COM")
		ports = list(ports)
	main_port = ports[0].device
	return ports[0].device
'''
def testArduinoConnection():
    try: 
		serial = serial.Serial(port = port, baudrate = 9600)
		serial.close()
	except:
		print("Unable to connect to Arduino on port " + port)
        return false
    return true
'''
def activateAlarm():
	arduino = serial.Serial(port=main_port, baudrate = 9600)
	time.sleep(1)
	arduino.write(b'1')
	# print("Unable to connect to Arduino on port " + main_port)
	# exit()
	arduino.close()

def deactivateAlarm():
	try: 
		arduino = serial.Serial(port=main_port,baudrate = 9600)
		time.sleep(1)
		arduino.write(b'0')
	except:
		print("Unable to connect to Arduino on port " + main_port)
		exit()
	finally:
		arduino.close()

def alarm(dur=4, pause=4):
	activateAlarm()
	time.sleep(dur)
	deactivateAlarm()
	time.sleep(pause)
	