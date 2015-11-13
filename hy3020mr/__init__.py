import serial
import time

class Psu:
	__hy3020mr_port = None
	def __init__(self, port_name = "/dev/ttyUSB0"):
		self.setPort(port_name)

	def setPort(self, port_name):
		self.__hy3020mr_port= serial.Serial(
		    port=port_name,
		    baudrate=9600,
		    parity=serial.PARITY_NONE,
		    stopbits=serial.STOPBITS_ONE,
		    bytesize=serial.EIGHTBITS
		)
		self.__hy3020mr_port.close()
		
	def getValues(self):
		self.__hy3020mr_port.open()
		if not self.__hy3020mr_port.isOpen():
			return None, None
		self.__hy3020mr_port.write(bytes('8', "UTF-8"))
		data = self.__hy3020mr_port.read(6).decode("UTF-8")
		print(data)
		self.__hy3020mr_port.close()
		voltage = float(data[0:3]) / 10
		current = float(data[3:6]) / 10
		return voltage, current

	def setData(self, data, tp):
		self.__hy3020mr_port.open()
		if not self.__hy3020mr_port.isOpen():
			return False
		output_buf = tp
		output_buf += "%03d" % (int(data * 10))
		summa = 0
		for i in range(0, 5):
			summa += int(output_buf[i])
		summa = summa % 10
		output_buf += str(summa)
		self.__hy3020mr_port.write(bytes(output_buf, "UTF-8"))
		time.sleep(2)
		data = self.__hy3020mr_port.read()
		self.__hy3020mr_port.close()
		if data[0] == 0:
			return True
		else:
			return False

	def setVoltage(self, voltage):
		if not (isinstance(voltage, int) or isinstance(voltage, float)):
			return False
		if voltage > 30:
			return False
		if voltage < 0:
			return False
		return self.setData(voltage, "20")

	def setCurrent(self, current):
		if not (isinstance(current, int) or isinstance(current, float)):
			return False
		if current > 20:
			return False
		if current < 0:
			return False
		return self.setData(voltage, "10")

