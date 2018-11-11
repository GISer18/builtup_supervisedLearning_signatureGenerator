# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 01:26:14 2018

@author: route2sabya
"""



import time
start_time = time.time()
# import the necessary packages
import cv2
import os, sys
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




def setup_dir(path):

    
    
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)



# load if you have coordinates

#image_coordx = io.imread(img_coord_xpath)
#image_coordy = io.imread(img_coord_ypath)






# super-pixel SLIC segmentation
def SLIC_sps(seg_range_min, seg_range_max,image_in,output_path):

    # loop over t\he number of segments
    for numSegments in (seg_range_min,seg_range_max):
        # apply SLIC and extract (approximately) the supplied number
        # of segments
        segments = slic(image_in, n_segments=numSegments, sigma=10,multichannel=True)



        # create the output of SLIC
        fig = plt.figure("Superpixels -- %d segments" % (numSegments))
        ax = fig.add_subplot(1, 1, 1)
        ax.imshow(mark_boundaries(image_in, segments))
        plt.axis("off")

        # save the plots
        time_str = datetime.datetime.now()
        filename = str(time_str).replace(':','_')
        filename = filename.strip(' ').replace(' ','')
        plt.savefig('{0}\{1}{2}.png'.format(output_path,filename,numSegments))
        #print(segments)
    return segments




def access_segments(segments_in,image_in):

    # loop over the unique segment values
    

    
    for (i, segVal) in enumerate(np.unique(segments_in)):
        
        

        mask = np.zeros((image_in).shape[:2], dtype="uint8")
        
        #print (mask)
        mask[segments_in == segVal] = 255

        # lets try to save the individual segments

        # slow method
        
        # fast method
        where = np.array(np.where(mask))
        print (where.shape)
        #where = imutils.resize(where, width=299, height=299)

        x1, y1 = np.amin(where, axis=1)
        x2, y2 = np.amax(where, axis=1)
        sub_image = image_in[x1:x2, y1:y2]
        print (sub_image.mean())
        #img = imutils.resize(img, width=1280)

        if sub_image.mean() >= 110 :
            #sub_image = imutils.resize(sub_image, width=299, height=299)
            cv2.imwrite(r"roi{0}.jpg".format(segVal), sub_image)
              
        
        #cv2.imwrite("roi{0}.jpg".format(segVal), sub_image)

        #############################################

        
        time_str = datetime.datetime.now()
        filename2 = str(time_str).replace(':', '_')
        filename2 = filename2.strip(' ').replace(' ', '')
        #show the masked region
        #cv2.imwrite('filename2{0}.png'.format("_segment"), img)
        #img_segval = Image.fromarray(segVal, 'RGB')
        #img_segval.save('my_segval{0}.png'.format(i))
        #img_segval.show()
        #cv2.imshow("Mask", mask)
        #cv2.imshow("Applied", cv2.bitwise_and(image, image, mask=mask))
        #cv2.waitKey(1000)

    return mask






def resize(dirs,img_path_2,px_size):
    for item in dirs:
        if os.path.isfile(img_path_2+r"\{0}".format(item)):
            im = Image.open(img_path_2+r"\{0}".format(item))
            f, e = os.path.splitext(img_path_2+r"\resized\{0}".format(item))
            imResize = im.resize((px_size,px_size), Image.ANTIALIAS)
            
            imResize.save( f + r"resized.jpg", "JPEG") #, quality=90



