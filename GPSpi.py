

# !/usr/bin/env python
# -*- coding: utf-8 -*-
#### 500.2 mb B efi boot 103.8 fat32 efi system
import pygame
import thread
import sys
import time
import datetime
import csv
import nmea

import gps.py



class GPSpi():

    def __init__(self):
        self.exit = False
        self.navstat_mode = 0
        # Switches for autopilot, routing, and AIS
        self.auto = False
        self.ais = False
        self.aismap_data = None
        # Location and baudrate of serial device
        self.serial_info = [None, None]

        self.eng_tach_rose_1 = [[395, 263, '0'], [273, 152, '10'], [389, 38, '20'], [506, 152, '30']]
        self.eng_tach_rose_2 = [[312, 232, '5'], [298, 75, '15'], [476, 71, '25'], [475, 232, '35']]
        #self.unit = lib.geomath.UNIT()
        #self.alarm = lib.alarm.ALARM()
        #self.gui = lib.gui.GUI()
        self.cache = nmea.CACHE()

        self.gps = gps.GPS(self.gui, self.cache, self.unit)
        # Get settings
        self.settings()

    def start(self, csv_filename):
        '''Starts the NAVSTAT program and contains main loop.'''
        # Attempts to create a serial NMEA connection
        self.connect()
      #  self.gps.track.distance_start()
        # Main program loop - continue until quit

        # katya - "gps_data.csv" is the output filename. you can change it if you want
        with open(csv_filename, "w", 128, newline='') as log_file:
            log_file_writer = csv.writer(log_file, delimiter=',')
        colnames = [ "utc", "lat", "lon", "speed"]
        log_file_writer.writerow(colnames)
        while self.exit == False:
            # katya - the line below writes this data to the file
            log_file_writer.writerow([self.nmea.data_gps['utc'], self.nmea.data_gps['lat'], self.nmea.data_gps['lon'], self.nmea.data_gps['speed']])
            time.sleep(0.3) # set sampling rate in seconds. this takes a sample every 0.3 secs

def connect(self):
    '''Determines whether a serial connection is available.'''
    x = 0
    connection = False
    # Readies a serial connection for NMEA GPS data
    self.nmea = nmea.NMEA0183(self.serial_info[0], self.serial_info[1], 5)
    while connection == False:
        try:
            # Attempts to make a serial connection
            self.nmea.read()
            connection = True
            failed = False
            # Waits until a proper data stream is available
            while self.nmea.data_gps['lat'] == 0 and self.nmea.data_gps['lon'] == 0:
                pass
            # Turns on tracking and routing if activated
            self.gps.track.switch()
            self.gps.route.switch()
        except:
            # Try 5 times - no serial connection - shut down
            if x == 5:
                self.nmea.exit = True
                connection = True
                # Returns tracking and routing to OFF
                self.gps.track.mode = False
                self.gps.route.mode = False
            x = x + 1


def settings(self):
		'''Open .config and load settings into respective variables'''
		settings = open('navstat.config', 'r')
		#Run through each line and load a setting
		for line in settings:
			#Line is not blank
			if line != '\n' or '' or None:
				#Line is not a comment
				if line[0:1] != '#':
					#Break up the setting name from contents
					settings_item = line.split('=')
					settings_item[1] = settings_item[1].rstrip()
					#Load settings - more info in navstat.config
					if settings_item[0] == 'frame_x':
						self.gui.size[1] = int(settings_item[1])
					elif settings_item[0] == 'frame_y':
						self.gui.size[0] = int(settings_item[1])
					elif settings_item[0] == 'top_speed':
						self.gps.speed_top = int(settings_item[1])
					elif settings_item[0] == 'night_mode':
						if str(settings_item[1]) == 'OFF':
							self.gui.night = True
						else:
							self.gui.night = False
					elif settings_item[0] == 'track_mode':
						if str(settings_item[1]) == 'OFF':
							self.gps.track.mode = True
						else:
							self.gps.track.mode = False
					elif settings_item[0] == 'mini_mode':
						if str(settings_item[1]) == 'OFF':
							self.gui.mini = True
						else:
							self.gui.mini = False
					elif settings_item[0] == 'track_secs':
						self.gps.track.save_info[0] = int(settings_item[1])
					elif settings_item[0] == 'track_save':
						self.gps.track.save_info[1] = int(settings_item[1])
					elif settings_item[0] == 'track_location':
						self.gps.track.location = str(settings_item[1])
					elif settings_item[0] == 'track_maxsize':
						self.gps.track.maxsize = int(settings_item[1])
					elif settings_item[0] == 'route_location':
						self.gps.route.location = str(settings_item[1])
					elif settings_item[0] == 'unit_distance':
						if str(settings_item[1]) == 'KM':
							self.unit.measure[0] = 0
						elif str(settings_item[1]) == 'MI':
							self.unit.measure[0] = 1
						elif str(settings_item[1]) == 'NM':
							self.unit.measure[0] = 2
						self.unit.text[0] = settings_item[1]
					elif settings_item[0] == 'unit_speed':
						if str(settings_item[1]) == 'KPH':
							self.unit.measure[1] = 0
						elif str(settings_item[1]) == 'MPH':
							self.unit.measure[1] = 1
						elif str(settings_item[1]) == 'NMPH':
							self.unit.measure[1] = 2
						self.unit.text[1] = settings_item[1].replace('PH','')
					elif settings_item[0] == 'gps_location':
						self.serial_info[0] = str(settings_item[1])
					elif settings_item[0] == 'gps_baudrate':
						self.serial_info[1] = int(settings_item[1])
					elif settings_item[0] == 'version':
						self.gui.version = settings_item[1]
					elif settings_item[0] == 'xte_alarm':
						self.xte_alarm = settings_item[1]
		settings.close()


def quit(self):
    '''Gets ready to quit.'''
    self.gui.screen.fill(self.gui.colour_1)
    self.gui.txt_out((self.gui.font_3.render('Exiting cleanly...', True, self.gui.colour_2)) ,355 ,128)
    pygame.display.flip()
    try:
        # Closes GPS serial connection
        self.nmea.quit()
    except:
        pass
    # Closes any open track files
    self.gps.track.off()
    time.sleep(2)
    pygame.quit()
    sys.exit()


# import cProfile
if __name__ == "__main__":
    gps = GPSpi()
    # set filename of your csv output file
    csv_filename = "gps_data.csv"
    gps.start(csv_filename)

