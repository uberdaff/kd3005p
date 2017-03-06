# -*- coding: utf-8 -*-
#
#  Copyright 2017 uberdaff
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
# Requirement: pyserial
#
# getIdn() - Get instrument identification
# setVolt(tal) - Set the voltage on the output
# getVolt() - Get the 'set' voltage
# readVolt() - Get a measurement of the voltage
# setAmp(tal) - Set the current limit
# getAmp() - Get the 'set' current limit
# readAmp() - Get a measurement of the output current
# setOut(bool) - Set the state of the output
# setOcp(bool) - Set the state of the over current protection
# getStatus() - Get the state of the output and CC/CV
#

import time
import serial

class kd3005pInstrument:
	isConnected = False
	psu_com = None
	status = {}
	
	def __init__(self, psu_com):
		psu_com.isOpen()
		self.psu_com = psu_com
		self.isConnected = True
		self.status=self.getStatus()
	
	def close(self):
		self.psu_com.close()
	
	def serWriteAndRecieve(self, data, delay=0.05): # data er ein stre
		self.psu_com.write(data)
		out = ''
		time.sleep(delay)
		while self.psu_com.inWaiting() > 0:
			out += self.psu_com.read(1)
		if out != '':
			return out
		return None
	
	def getIdn(self):
		return self.serWriteAndRecieve("*IDN?", 0.3)
	
	def setVolt(self, voltage, delay=0.01):
		self.serWriteAndRecieve("VSET1:"+"{:1.2f}".format(voltage))
		time.sleep(delay) # Vent på at straumforsyninga stabilisera seg.
	
	def getVolt(self):
		return self.serWriteAndRecieve("VSET1?")
	
	def readVolt(self):
		return self.serWriteAndRecieve("VOUT1?")
	
	def setAmp(self, amp, delay=0.01):
		self.serWriteAndRecieve("ISET1:"+"{:1.3f}".format(amp))
		time.sleep(delay) # Vent på at straumforsyninga stabilisera seg.
	
	def getAmp(self):
		return self.serWriteAndRecieve("ISET1?")
	
	def readAmp(self):
		return self.serWriteAndRecieve("IOUT1?")
	
	def setOut(self, state):
		if(state == True):
			self.serWriteAndRecieve("OUT1")
		elif(state == False):
			self.serWriteAndRecieve("OUT0")
	
	def setOcp(self, state):
		if(state == True):
			self.serWriteAndRecieve("OCP1")
		elif(state == False):
			self.serWriteAndRecieve("OCP0")
	
	def getStatus(self):
		stat = ord(self.serWriteAndRecieve("STATUS?")[0])
		if (stat&(1 << 0))==0:
			self.status["Mode"]="CC"
		else:
			self.status["Mode"]="CV"
		if (stat&(1 << 6))==0:
			self.status["Output"]="Off"
		else:
			self.status["Output"]="On"
		return self.status
	
