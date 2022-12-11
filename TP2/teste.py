import socket
from threading import Thread
import json
import sys
import pickle
import b_database
from time import sleep
import time
import os



def readVideoFile():
    filename = 'movie.Mjpeg'
    print("Reading Video File and saving to database...")
    try:
        file = open(filename, 'rb')
    except:
        print("Error opening file!")
        raise IOError
    frameNum = 0
    buffer = []
    ###### Get next frame (nextFrame from VideoStream.py)
    file_stats = os.stat(filename)
    unread_FileSize_bytes = file_stats.st_size  #here it represents the total size of the file in bytes, because none was read untill now
    print(f'File Size in Bytes is {unread_FileSize_bytes}')
    while (unread_FileSize_bytes ) > 0:
        data = file.read(5) # Get the framelength from the first 5 bytes
        if data:
            frameLenght = int(data)
            #Read the current frame
            data = file.read(frameLenght)
            print(data)
            sleep(5)
            buffer.append(data)
            frameNum += 1 
        unread_FileSize_bytes = unread_FileSize_bytes - 5 - frameLenght

    

readVideoFile()