

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





def quit(self):
    '''Gets NAVSTAT ready to quit.'''
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

