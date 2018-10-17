import thread
import time
import datetime
import geomath
import math
import pygame
import sys


class GPS():

    def __init__(self, gui, cache, unit):
        # Degree character required for lat/long
        self.degree = chr(176)
        # Top speed on the speedometer
        self.speed_top = 2
        # Compass rose x,y points
        self.compass_rose_1 = [[393, 40, 'N'], [278, 152, 'W'], [393, 263, 'S'], [502, 152, 'E']]
        self.compass_rose_2 = [[298, 75, 'NW'], [298, 232, 'SW'], [475, 232, 'SE'], [475, 75, 'NE']]
        self.compass_rose_3 = [[(400, 62), (400, 82)], [(471, 91), (461, 101)], [(500, 162), (480, 162)],
                               [(471, 233), (461, 223)], [(400, 262), (400, 242)], [(329, 233), (339, 223)],
                               [(300, 162), (320, 162)], [(329, 91), (339, 101)]]
        # Used to calculate the location of text
        self.calc_size = geomath.calc_size
        # Used to calculate the position of a line in a circle
        self.calc_line = geomath.calc_line
        # Used to convert units
        self.unit = unit
        # Holds GUI data
        self.gui = gui
        # Holds cached GPS data
        self.cache = cache
        self.route = ROUTE(self.cache, ALARM())
        self.track = TRACK(self.cache)



    def latlong(self):
        '''Positions and draws the lat/long interface.

        Keyword arguments:
        lat -- the current latitude position
        lon -- the current longitude position

        '''
        # Draws the basic latlon interface
        pygame.draw.rect(self.gui.screen, self.gui.colour_2, (0, 0, 250, 20))
        self.gui.txt_out((self.gui.font_3.render('POS', True, self.gui.colour_1)), 107, 0)
        # Cuts the decimal count down to 5
        lat = self.cache.gps['lat']
        lon = self.cache.gps['lon']
        lat_out = ("%.5f" % self.cache.gps['lat'])
        lon_out = ("%.5f" % self.cache.gps['lon'])
        # Applies N/S, W/E based on negative value
        if lat < 0:
            lat_out = lat_out[1:] + ' S'
        elif lat > 0:
            lat_out = lat_out + ' N'
        if lon < 0:
            lon_out = lon_out[1:] + ' W'
        elif lon > 0:
            lon_out = lon_out + ' E'
        # Determines the lat length, and centres accordingly
        l_len = len(lat_out)
        if l_len == 10:
            ext_1 = 20
        elif l_len == 11:
            ext_1 = 1
        else:
            ext_1 = 40
        # Determines the lon length, and centres accordingly
        l_len = len(lon_out)
        if l_len == 10:
            ext_2 = 20
        elif l_len == 11:
            ext_2 = 1
        else:
            ext_2 = 40
        # Draws the lat/long interface text
        self.gui.txt_out((self.gui.font_4.render(lat_out, True, self.gui.colour_2)), 20 + ext_1, 30)
        self.gui.txt_out((self.gui.font_4.render(lon_out, True, self.gui.colour_2)), 20 + ext_2, 75)
