#!/usr/bin/python3

from bottle import route, run
import json

@route('/hello')
def hello():
	return "Hello World!"

@route('/current_values')
def current_values():
	retval = {}
	retval["current"] = 1.1
	retval["voltage"] = 12.5
	retval = json.dumps(retval)
	return retval

if __name__ == "__main__":
	run(host="", port=1488, debug=True)