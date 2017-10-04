import sys
import csv
import datetime
import os
import struct
import wave, struct, numpy, time
import numpy as np
import scipy
from scipy.io.wavfile import read
from scipy.io.wavfile import write
from scipy.signal import fftconvolve



#################################################################################################################################
#                                                        Introduction/Setup of program                                          #
#################################################################################################################################
#edit only 4 lines 16,18,20,22

#-------------------------
print ('Starting Audio File Convolver')
#-------------------------


#Path of clean speech audio files are entered below
cleanspeechpath = 'C:/Python27/convolver/cleanspeechappen/converted/'
#Path to clean speech csv file + csv filename 
cleanspeechcsv = "C:/Python27/convolver/cleanspeechappen/cleanspeechappen.csv"
#Path of impulse audio files are entered below
impulsepath = 'C:/Python27/convolver/impulse/converted/'
#Path to impulse csv file + csv filename
impulsecsv = "C:/Python27/convolver/impulse/impulse1.csv"
#result location
result_loc = 'C:/Python27/convolver/appenimpulsed/'


#Confirmation on correct file locations
print("Clean speech files located at " + cleanspeechpath)
print("Impulse audio file located at " + impulsepath)
print("----------------------------------------------------------------------------")

# Set Result file name

print('Result will be output to ' + result_loc)

print("----------------------------------------------------------------------------")
#################################################################################################################################
#                                                         Read from CSV file                                                    #
#################################################################################################################################

#Grabs csv files that list filenames of both clean speech and impulse responses
#csrow is row of cleanspeech
with open(cleanspeechcsv, 'rb') as f:
	reader1 = csv.reader(f)
	csrow = reader1.next()
	for csrow in reader1:
		with open(impulsecsv, 'rb') as f:
			reader = csv.reader(f)
			improw = reader.next()
			try:
				for improw in reader:
					
	#grabs cs and impulse filename as a path
					csfilename = os.path.normpath(os.path.join(cleanspeechpath, csrow[0]))
					ifilename = os.path.normpath(os.path.join(impulsepath, improw[0]))
					#flug = os.path.exists(audiofilename)
					
########################################################################################################################################					
#                                                        MAIN BODY OF CODE                                                             #					
########################################################################################################################################					
					def wavLoad (fname):
					   wav = wave.open(fname, "r")
					   (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
					   params = wav.getparams()
					   frames = wav.readframes (nframes * nchannels)
					   formats = ["B", "h", "no_support_for_24bit", "i"] # B - unsigned char (standard size = 1); h - sig. short (standard size = 2); i - sig. integer (size 4).
					   fmt = ("%i" % nframes + formats[sampwidth-1]) * nchannels # unpacks string of bytes according packing.
					   # More on packing: bytes are packed with specific chunk sizes. Each chunk size has signedness and length
					   out = struct.unpack_from(fmt, frames) 
					   wav.close()
					   return out, params

					def wavSave (name, samples, params):
						"Packs data into 16bit mono format and saves WAV file"
						wav = wave.open(name, 'w')
						wav.setparams(params)
						data = "" # assuming string of bytes is a string.
						for it in samples:
							data += struct.pack("h", it)
						wav.writeframes(data)
						wav.close()

						
					def convolution(x, h):
						"Does FIR convolution using numpy arrays. y(k) = sum(x(k-n) * h(n)). Normalizes waveform. Slow (1s of signal = 10 s of processing)"    
						y = numpy.zeros(x.size + h.size)
						ct = 0
						for k in x:
							# for each sample k in signal y, multiply with array h. Add to array y: start at position 0, 1, 2, 3 ... etc.
							# when last k is taken, IR h will fill array y until position y.size - 1. Next multiplication would be with 0.
							y[ct : ct + h.size] += k * h
							ct += 1
						return y

					def normalize(y, bitwidth):
						"Normalizes according to bitwidth"
						if abs(numpy.amax(y)) > abs(numpy.amin(y)): larger = numpy.amax(y)
						else: larger = abs(numpy.amin(y))
						y = y / larger * ((2**bitwidth / 2) - 1) # normalize assuming 16bit width, signed format.
						return y


					fnameA = csfilename
					fnameB = ifilename
					inBitWidth = 16

					(samplesA, paramsA) = wavLoad(fnameA)
					(samplesB, paramsB) = wavLoad(fnameB)
					sampArrayA = numpy.array(samplesA)
					sampArrayB = numpy.array(samplesB)

					time1 = time.time()
					result = convolution(sampArrayA, sampArrayB)
					time2 = time.time()
					dur = time2 - time1
					print "Convolution complete in " + str(dur) + " second(s)."

					result = normalize(result, inBitWidth)
					#printGraph(result, fnameA)

					wavSave(result_loc+"con"+csrow[0], result, paramsA)
		
			except ValueError:
				print('opps')
			
	
