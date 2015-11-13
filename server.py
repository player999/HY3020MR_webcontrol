#!/usr/bin/python3

from bottle import route, run, post, request, static_file
import threading
import json
import time

measuring_thread = None
mutex = None

@route('/')
def index():
	return static_file('index.html', root='./htdocs')

@route('/static/<filepath:path>')
def files(filepath):
	return static_file(filepath, root='./htdocs')

@route('/current_values')
def current_values():
	retval = {}
	#Fake read values
	retval["current"] = measuring_thread.current
	retval["voltage"] = measuring_thread.voltage
	retval["error"] = "success";
	retval = json.dumps(retval)
	return retval

@post('/set_voltage')
def set_voltage():
	global mutex
	data = request.body.read().decode("UTF-8")
	data = json.loads(data)
	voltage = data["value"]
	mutex.acquire()
	#Do settings
	mutex.release()
	print(voltage)
	response = {"error": "success"}
	return json.dumps(response)

@post('/set_current')
def set_current():
	global mutex
	data = request.body.read().decode("UTF-8")
	data = json.loads(data)
	current = data["value"]
	mutex.acquire()
	#Do settings
	mutex.release()
	print(current)
	response = {"error": "success"}
	return json.dumps(response)

class Measuring(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.voltage = 0
		self.current = 0
	def run(self):
		#Measuring
		global mutex
		while 1:
			mutex.acquire()
			self.voltage += 1
			self.current += 1
			mutex.release()
			time.sleep(5)


if __name__ == "__main__":
	global measuring_thread
	global mutex
	mutex = threading.Lock()
	measuring_thread = Measuring()
	measuring_thread.start()
	run(host="", port=1488, debug=True)