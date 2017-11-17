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



# global waLoad
# global wavSave
# global convolution
# global normalize


#################################################################################################################################
#                                                        Introduction/Setup of program                                          #
#################################################################################################################################


#-------------------------
print ('Starting Audio File Convolver')
#-------------------------
#Path of database output csv
csvpath = sys.argv[1]
#result location
result_loc = sys.argv[2]


#Confirmation on correct file locations
print("Clean speech files located at " + csvpath)
print("Result located at " + result_loc)
print("----------------------------------------------------------------------------")

# Set Result file name
#################################################################################################################################
#                                                         Read from CSV file                                                    #
#################################################################################################################################

#Grabs csv files that list filenames of both clean speech and impulse responses
#csrow is row of cleanspeech
with open(csvpath, 'rb') as f:
	reader1 = csv.reader(f)
	csrow = reader1.next()
	for csrow in reader1:
			try:
			
			
			#grabs cs and impulse filename as a path
				csfile = os.path.normpath(os.path.join(csrow[0], csrow[1]))
				impfile = os.path.normpath(os.path.join(csrow[2], csrow[3]))
				rnfile = os.path.normpath(os.path.join(csrow[4], csrow[5]))		
							
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


				fnameA = csfile
				fnameB = impfile
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

				#result = normalize(result, inBitWidth)
				#printGraph(result, fnameA)

				wavSave(result_loc+"con", result, paramsA)
				
			except ValueError:
				print('opps')
			
	
