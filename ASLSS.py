#!/usr/bin/python
# GoogleMapDownloader.py
# Created by Hayden Eskriett [http://eskriett.com]
#
# A script which when given a longitude, latitude and zoom level downloads a
# high resolution google map
# Find the associated blog post at: http://blog.eskriett.com/2013/07/19/downloading-google-maps/


import time
start_time = time.time()
# import the necessary packages
import cv2
#import sys
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float,img_as_ubyte
from skimage import io
import matplotlib.pyplot as plt
import datetime
import numpy as np
import imutils
from tkinter import filedialog
from tkinter import *
#np.set_printoptions(threshold=np.nan)

import pandas as pd
import PIL
from PIL import Image
import argparse
import pprint
#########################
import urllib.request
from PIL import Image

import math
import random
import os
import slic_app
from slic_app import setup_dir,SLIC_sps,access_segments,resize



class GoogleMapDownloader:
    """
        A class which generates high resolution google maps images given
        a longitude, latitude and zoom level
    """

    def __init__(self, lat, lng,stride, zoom=17):
        """
            GoogleMapDownloader Constructor

            Args:
                lat:    The latitude of the location required
                lng:    The longitude of the location required
                zoom:   The zoom level of the location required, ranges from 0 - 23
                        defaults to 12
        """
        self._lat = lat
        self._lng = lng
        
        self._stride = stride
        self._zoom = zoom

    def getXY(self):
        """
            Generates an X,Y tile coordinate based on the latitude, longitude
            and zoom level

            Returns:    An X,Y tile coordinate
        """

        tile_size = 256

        # Use a left shift to get the power of 2
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles
        numTiles = 1 << self._zoom

        # Find the x_point given the longitude
        point_x = (tile_size / 2 + self._lng * tile_size / 360.0) * numTiles // tile_size

        # Convert the latitude to radians and take the sine
        sin_y = math.sin(self._lat * (math.pi / 180.0))

        # Calulate the y coorindate
        point_y = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(
        tile_size / (2 * math.pi))) * numTiles // tile_size

        return int(point_x), int(point_y)

    def generateImage(self, **kwargs):
        """
            Generates an image by stitching a number of google map tiles together.

            Args:
                start_x:        The top-left x-tile coordinate
                start_y:        The top-left y-tile coordinate
                tile_width:     The number of tiles wide the image should be -
                                defaults to 5
                tile_height:    The number of tiles high the image should be -
                                defaults to 5
            Returns:
                A high-resolution Goole Map image.
        """

        start_x = kwargs.get('start_x', None)
        start_y = kwargs.get('start_y', None)
        tile_width = kwargs.get('tile_width', self._stride)
        tile_height = kwargs.get('tile_height', self._stride)

        # Check that we have x and y tile coordinates
        # Check that we have x and y tile coordinates
        if start_x == None or start_y == None:
            start_x, start_y = self.getXY()

        # Determine the size of the image
        width, height = 256 * tile_width, 256 * tile_height

        # Create a new image of the size require
        map_img = Image.new('RGB', (width, height))

        for x in range(0, tile_width):
            for y in range(0, tile_height):
                url = 'https://mt1.google.com/vt/lyrs=s?x=' + str(start_x + x) + '&y=' + str(
                    start_y + y) + '&z=' + str(self._zoom)

                current_tile = str(x) + '-' + str(y)
                urllib.request.urlretrieve(url, current_tile)
                print ("pausing for 2 seconds...row and column: {0}".format(x))
                time.sleep(random.randint(4,10))

                im = Image.open(current_tile)
                map_img.paste(im, (x * 256, y * 256))

                os.remove(current_tile)

        return map_img



    
def main():

    

               



               
    #input lat, lon, zoom level from user
    
    lat_i = input("Please input latitude coordinates in degree decimals(WGS84:4326): ")
    lat_i = float((lat_i.strip()))
    lon_i = input("Please input longitude coordinates in degree decimals(WGS84:4326): ")
    lon_i = float((lon_i.strip()))
    zoom_i = input("Please input zoom level value: \nThe following list shows the approximate level of detail you can expect to see at each zoom level:\n1: World\n5: Landmass/continent\n10: City\n15: Streets\n20: Buildings\n Enter value : ")
    zoom_i = int(zoom_i.strip())

    stride_i = input("Enter the number of images to be stitched on both x and y direction: ")
    stride_i = int(stride_i.strip())
    
    px_dim = input("Input pixel height or only width for output samples: ")
    px_dim = int(px_dim.strip())

    seg_min = input("Input number of segments desired (minimum): ")
    seg_min = int(seg_min.strip())
    seg_max = input("Input number of segments desired (maximum)): ")
    seg_max = int(seg_max.strip())
    
    gmd = GoogleMapDownloader(lat_i, lon_i, stride_i,zoom_i)

    print("The tile coorindates are {}".format(gmd.getXY()))

    try:
        # Get the high resolution image
        img = gmd.generateImage()
    except IOError:
        print("Could not generate the image - try adjusting the zoom level and checking your coordinates")
    else:
        # Save the image to disk
        input_seg_path = filedialog.askdirectory()
        setup_dir(input_seg_path+"/input_seg")
        setup_dir(input_seg_path+"/output")
        img.save(r"{0}/input_seg/new_gurugram_sample.png".format(input_seg_path))
        print("The map has successfully been created")
    
    img_path = filedialog.askopenfilename()
    output_path = filedialog.askdirectory()
    io.use_plugin('pil')
    image_in= img_as_ubyte(io.imread(img_path,dtype="uint8"))

    setup_dir(output_path+"/segments")
    setup_dir(output_path+"/segments/resized")
    print (image_in.max(),image_in.min(),image_in.shape, image_in.dtype)
    segments = slic_app.SLIC_sps(seg_min,seg_max,image_in,output_path)
    access_segments(segments, image_in)
    img_path_2 = filedialog.askdirectory()
    setup_dir(r"{0}\resized".format(img_path_2))
    dirs = os.listdir(img_path_2)
    resize(dirs,img_path_2, px_dim)
    #root.mainloop()
    


  
# time   



#total_time = time.time() - start_time
#print ("total time: {0}".format(total_time))    
    

    
if __name__ == '__main__':
    main()
    
    print ("The program will exit now. Thank you for your patience")
    #quit()
    
