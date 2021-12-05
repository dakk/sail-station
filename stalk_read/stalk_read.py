# Copyright (C) 2020 by GeDaD <https://github.com/Thomas-GeDaD/openplotter-MCS>
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# any later version.
# You should have received a copy of the GNU General Public License.
# If not, see <http://www.gnu.org/licenses/>.
#
# 2020-07-03 @MatsA Added function for inverting signal and using RPi internal pull up/down
# 2020-08-18 Updated according to Thomas-GeDaD commits => reduce cpu consumption & Fix first character if 0x00 / string =00
#

import pigpio
import pynmea2
import time
import socket
import signal
import sys

port = 4041  # Define udp port for sending
ip = '127.0.0.1'  # Define ip default localhost 127.0.0.1
gpio = 4  	# Define gpio where the SeaTalk1 (yellow wire) is sensed
invert = 0      # Define if input signal shall be inverted 0 => not inverted, 1 => Inverted
pud = 2         # define if using internal RPi pull up/down 0 => No, 1= Pull down, 2=Pull up


global angle, speed
angle = 0
speed = 0


def process(sorig):
	global speed, angle
	s = sorig.split(',')[1::]
	nmea = None

	# AWA Corresponding NMEA sentence: MWV
	if len(s) >= 4 and s[0] == '10' and s[1] == '01':
		angle = (int('0x'+s[3], 16) + int('0x'+s[2], 16) * 0xff) / 2
		#print ('awa', angle)
		#nmea = pynmea2.MWV(True, 'R', angle, 'N', 'A')
		# Create nmea string mwv for wind angle
		angle = "{:.1f}".format(angle)
		nmea = '$IIMWV,%s,R,%s,k,A' % (angle, speed)

	# AWS Corresponding NMEA sentence: MWV
	elif len(s) >= 4 and s[0] == '11' and s[1] == '01':
		speed = (int('0x' + s[2], 16) & 0x7f) + int('0x' + s[3][1], 16) / 10
		#print('aws', speed)
		#nmea = pynmea2.MWV(True, 'R', speed, 'N', 'A')
		# Create nmea string mwv for wind speed
		speed = "{:.1f}".format(speed)
		nmea = '$IIMWV,%s,R,%s,k,A' % (angle, speed)

	# DEPTH NMEA sentences: DPT, DBT
	elif len(s) >= 5 and s[0] == '00' and s[1] == '02':
		depth = (int('0x'+s[3], 16) + int('0x'+s[4], 16) * 0xff) / 10 * 0.3048
		#print ('depth', depth)
		#nmea = pynmea2.DPT('IN', 'DPT', (str(depth)))

		# Create nmea string dpt for depth
		depth = "{:.1f}".format(depth)
		nmea = '$IIDBT,,f,%s,M,,F' % (depth)

	# Water temp Corresponding NMEA sentence: MTW
	elif len(s) >= 4 and s[0] == '27' and s[1] == '01':
		temp = ((int('0x'+s[2], 16) + int('0x'+s[3], 16) * 0xff) - 100.)/10.
		#print ('temp', temp)
		#nmea = pynmea2.MTW(temp, 'celsius')

		# Create nmea string mtw for water temp
		temp = "{:.1f}".format(temp)
		#nmea = '$IIMTW,%s,C,%s,C,%s,C' % (temp, temp, temp)
		#nmea = '$IIMDA,,I,,B,,C,%s,C,,,,C,,T,,M,,N,,M' % (temp)

	# Compass
	elif len(s) >= 4 and s[0] == '9c':
		U = int('0x' + s[1][0], 16)
		VW = int('0x' + s[2], 16)
		hdg = (U & 0x3) * 90 + (VW & 0x3F) * 2 + \
			((U & (2 if 0xC == 0xC else 1)) if (U & 0xC) else 0)
		# print('heading', hdg)
		hdg = "{:.0f}".format(hdg)
		nmea = 'IIHDM,%s,M' % (hdg)

	# SOG Corresponding NMEA sentence: VHW
	elif len(s) >= 4 and s[0] == '20' and s[1] == '01':
		sog = ((int('0x'+s[2], 16) + int('0x'+s[3], 16) * 0xff))/10.
		#print ('sog', sog)
		#nmea = pynmea2.VHW(sog, 'T', 'M', 'N')

		# Create nmea string vhw for speed over ground
		#nmea = '$IIVHW,%s,T,M,N,N' % (sog)

	if nmea != None:
		return str(pynmea2.parse(nmea)) + '\r\n'
	else:
		return sorig + '\r\n'


if __name__ == '__main__':
	print('Stalk_read starting...')
	st1read = pigpio.pi()

	try:
		st1read.bb_serial_read_close(gpio)  # close if already run
	except:
		pass

	# Read from chosen GPIO with 4800 Baudrate and 9 bit
	st1read.bb_serial_read_open(gpio, 4800, 9)
	st1read.bb_serial_invert(gpio, invert)		# Invert data
	st1read.set_pull_up_down(gpio, pud)		# Set pull up/down

	data = ""

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print('Stalk_read reading')
	try:
		while True:
			out = (st1read.bb_serial_read(gpio))
			out0 = out[0]
			if out0 > 0:
				out_data = out[1]
				x = 0
				while x < out0:
					if out_data[x+1] == 0:
						string1 = str(hex(out_data[x]))
						if out_data[x] > 15:
							string1 = str(hex(out_data[x]))
						elif out_data[x] == 0:
							string1 = "0x00"
						else:
							string1 = "0x0"+str(hex(out_data[x]).lstrip("0x"))
						data = data+string1[2:] + ","
					else:
						data = data[0:-1]
						data = "$STALK,"+data
						dd = process(data)
						sock.sendto(dd.encode('utf-8'), (ip, port))
						# print(data)
						string2 = str(hex(out_data[x]))
						string2_new = string2[2:]
						if len(string2_new) == 1:
							string2_new = "0"+string2_new
						data = string2_new + ","

					x += 2
			time.sleep(0.01)

	except KeyboardInterrupt:
		st1read.bb_serial_read_close(gpio)
		print("exit")
