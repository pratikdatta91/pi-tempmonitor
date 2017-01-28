#!/bin/sh

import os 
import glob
import time 
import sys 
import datetime 
import urllib2 
import collections
import subprocess
from ISStreamer.Streamer import Streamer
import RPi.GPIO as io 
import urllib
import thread

baseURL = "https://api.thingspeak.com/update?api_key=HFM96M1A2BXX9X0V" 
baseURL1 = "https://maker.ifttt.com/trigger/temp/with/key/nhP9WYV1M_RRMtccG-pbfFpNFVxUPGpIyf_KmvubSRy/"
 

#initiate the temperature sensor 

os.system('modprobe w1-gpio') 

os.system('modprobe w1-therm') 

 

#set up the location of the sensor in the system 

base_dir = '/sys/bus/w1/devices/' 

device_folder = glob.glob(base_dir + '28*')[0] 

device_file = device_folder + '/w1_slave' 

 

def read_temp_raw(): #a function that grabs the raw temperature data from the sensor

     f = open(device_file, 'r')

     lines = f.readlines()

     f.close()

     return lines 

 

def read_temp(): #a function that checks that the connection was good and strips out the temperature

     lines = read_temp_raw()

     while lines[0].strip()[-3:] != 'YES':

         time.sleep(0.2)

         lines = read_temp_raw()

     equals_pos = lines[1].find('t=')

     if equals_pos !=-1:

         temp_string = lines[1][equals_pos+2:]

         temp_c = float(temp_string)/1000.0

         temp_f = temp_c * 9.0/5.0 + 32.0

         return temp_c 

 

while True: #infinite loop

	streamer = Streamer(bucket_name="Home Temperature Sensor",bucket_key="hometemp1234",access_key="b3L6pg1moHF8iq8UzsCwLDDZ4DtY07h2")
     
	tempin = read_temp() #get the temp

     	values = [datetime.datetime.now(), tempin]

     	g = urllib2.urlopen(baseURL + "&field1=%s" % (tempin))
	query_args = {}
	query_args['value1'] = str(tempin)
	query_args['value2'] = str(datetime.datetime.now())
	data = urllib.urlencode(query_args)
	request = urllib2.Request(baseURL1,data)
	response = urllib2.urlopen(request)
	streamer.log("Temperature (C)", tempin)
	streamer.flush()
#	print "Temperature: " + str(tempin) + " C"
	
	time.sleep(60) 
