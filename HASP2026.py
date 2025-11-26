from time import sleep
import numpy
import cv2
import zwoasi
import AsiModule
from ModeControl import ModeControl
from ModeControl import SystemMode
import GuiderModule
import threading
import serial
import random
import struct
import ModeControl_OLD
import keyboard
from getch import getch, pause

def input_worker_thread():
    while True:
        print("Input\n")
        global stop_input_thread
        global command_in
        #serialPort.write(b'A')
        #print(serialPort.read(94))
        #bytesread = serialPort.readline()
        #print(bytesread)
        #elements = bytesread.decode().split(",")
        #if ((len(elements) > 1) and elements[1] == "$GPGGA"):
        #    print ("Data: " + elements[2])
        #    #print (elements)
        #    #for item in elements:
        #    #    print (str(item))
        #elif (elements[0] != ""):
        #    print ("Command: " + str(elements[0][2:4]))
        #    command_in = int(elements[0][3:4])
        #    #print (str(elements[0][2:4]))
        #else:
        #    print ("Nothing")    
        #for item in elements:
        #    print (str(item))
        if stop_input_thread:
        #    serialPort.close()
           break
        sleep(5.0)
    
def output_worker_thread():
    while True:
        print("Output\n")
        global stop_output_thread
        #serialPort.write(ba)
        #if (serialPort.is_open):
        #    serialPort.write(randint())
        if stop_output_thread:
            break
        sleep(5.0)
    
def processing_worker_thread():
    while True:
        print("Processing\n")
        global command_in
        global stop_processing_thread
        #serialPort.write(b'C')
        if stop_processing_thread:
            break
        sleep(5.0)

# Initialize the startup conditions
print("Initializing")
#serialPort = serial.Serial(port="COM1", baudrate=9600, bytesize=8, timeout=5, stopbits=serial.STOPBITS_ONE, parity='N')
#serialPort = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, bytesize=8, timeout=5, stopbits=serial.STOPBITS_ONE, parity='N')
modeControl = ModeControl()
command_in = 0

# Setup the worker threads
input_thread = threading.Thread(target=input_worker_thread, args=())
processing_thraed = threading.Thread(target=processing_worker_thread, args=())
output_thread = threading.Thread(target=output_worker_thread, args=())

global stop_input_thread
global stop_output_thread
global stop_processing_thread

stop_input_thread = False
stop_output_thread = False
stop_processing_thread = False

print("Starting")    
input_thread.start()
processing_thraed.start()
output_thread.start()

while True:
    modeControl.SystemMCL()
    
    key = getch()   # This is a blocking call
    stop_input_thread = True
    stop_output_thread = True
    stop_processing_thread = True
    break
    
print("Done!")
