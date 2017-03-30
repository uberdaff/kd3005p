#!/usr/bin/env python
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

import kd3005p

def main(args):
	psu = kd3005p.kd3005pInstrument('COM11')
	if psu.isConnected == True:
		print(psu.getIdn())
		psu.setVolt(13.37)
		psu.setAmp(0.1)
		print(psu.readVolt())
		print(psu.readAmp())
		print(psu.status)
	psu.close()	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
