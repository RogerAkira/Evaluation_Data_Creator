import sys
import csv
import datetime
import os
import struct
import wave, struct, numpy, time
import matplotlib.pyplot as plt
#import wavefile
import numpy as np
import scipy
from pydub import AudioSegment
#import audiolab
from scipy.io.wavfile import write

#################################################################################################################################
#                                                        Introduction/Setup of program                                          #
#################################################################################################################################
#edit only 4 lines 16,18,20,22

#-------------------------
print ('Starting Road Noise Mixer')
#-------------------------


#Path of clean speech audio files are entered below
cleanspeechpath = 'C:/Python27/convolver/cleanspeechappen/converted/'
#Path to clean speech csv file + csv filename 
cleanspeechcsv = "C:/Python27/convolver/cleanspeechappen/cleanspeechappen.csv"
#Path of Road Noise are entered below
roadnoisepath = 'C:/Python27/rn/converted/'
#Path to Road Noise csv file + csv filename
roadnoisecsv = "C:/Python27/rn/rn.csv"
#Enter Result Folder
result_loc = "C:/Python27/convolver/appenrn/"



#Confirmation on correct file locations
print("Clean speech files located at " + cleanspeechpath)
print("Road Noise audio file located at " + roadnoisepath)
print("----------------------------------------------------------------------------")

# Set Result file name

print('Result will be output to ' + result_loc)

print("----------------------------------------------------------------------------")
#################################################################################################################################
#                                                         Main body of Code                                                     #
#################################################################################################################################

#Grabs csv files that list filenames of both clean speech and Road Noise responses
#csrow is row of cleanspeech
with open(cleanspeechcsv, 'rb') as f:
	reader1 = csv.reader(f)
	csrow = reader1.next()
	for csrow in reader1:
		with open(roadnoisecsv, 'rb') as f:
			reader = csv.reader(f)
			rnrow = reader.next()
			try:
				for rnrow in reader:
					
	#grabs cs and Road Noise filename as a path
					csfilename = os.path.normpath(os.path.join(cleanspeechpath, csrow[0]))
					rnfilename = os.path.normpath(os.path.join(roadnoisepath, rnrow[0]))
					#flug = os.path.exists(audiofilename)
					#convert to numpy array
					
					
					time1 = time.time()
					
					sound1 = AudioSegment.from_file(csfilename)
					sound2 = AudioSegment.from_file(rnfilename)

					combined = sound1.overlay(sound2)
					time2 = time.time()
					dur = time2 - time1
					print "Completed " + csrow[0] + " latency " + str(dur)
					combined.export(result_loc+'mixed'+csrow[0], format='wav')
					
					# Write the data to 'newname.wav'
					#scipy.io.wavfile.write('impulsed' +csrow[0]+'.wav', rate, newdata)
					
					
					
			except ValueError:
				print('opps')
			
	
