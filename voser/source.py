import basic_functions
import numpy as np

class Source:
	def __init__(self, x=0, y=0, invert=False, delay=0, gain=0):
		self.x = x
		self.y = y
		self.invert = invert
		self.delay = delay
		self.gain = gain

	#list like [] index emulation
	#__getslice__, __setslice__  not implemented
	def __getitem__(self, i):
		'''
			sorry, not elegant
			still faster than counstructing a dict for this tho
		'''
		if (i==0):
			return self.x
		if (i==1):
			return self.y
		if (i==2):
			return self.invert
		if (i==3):
			return self.delay
		if (i==4):
			return self.gain
		print("Requested index: {}".format(i))
		raise("index out of bounds")

	def __setitem__(self, i, value):
		'''
			sorry, not elegant
		'''
		if (i==0):
			self.x = value
		if (i==1):
			self.y = value
		if (i==2):
			self.invert = value
		if (i==3):
			self.delay = value
		if (i==4):
			self.gain = value

		return ;

	def distance(self, x, y):
		'''
			Returns distance between this source and specified point
			Parameters
				x, y: float
					point coordiantes
			Returns
				distance
		'''
		return np.sqrt((x-self.x)**2 + (y-self.y)**2)


	def calculateAmplitude(self, distance, reference_level=0):
		'''
			Returns sound level produced by this source in given position
			Parameters
				distance: float
					distance from the source
				reference_level: float, optional
					if reference_level is provided, gain of this source is relative to that
			Returns
				pressure level in pascals, not in dB logarithimc scale

		'''
		p1 = basic_functions.dBTop(self.gain + reference_level)
		return(p1/distance)

	
	def calculatePhase(self, distance, k, w):
		'''
			Returns sound level produced by this source in given position
			Parameters
				distance: float
					distance of source from the listener
				k: flaot
					wave number
				w: float
					angular frequency [rad/s]
				reference_level: float, optional
					if reference_level is provided, gain of this source is relative to that
			Returns
				pressure level in pascals, not in dB logarithimc

		'''
		inversion_shift = np.pi if self.invert else 0;
		delay_shift = self.delay*w
		positional_shift = k*distance
		#not really sure, whether delay shift should be negative
		return (positional_shift - delay_shift + inversion_shift)


	def vawe(self, x, y, k, w, reference_level = 0, distance_limit = 0.5):
		'''
			Returns sound level produced by this source in given position
			Parameters
				x, y: float
					position of listener
				k: flaot
					wave number
				w: float
					angular frequency [rad/s]
				reference_level: float, optional
					if reference_level is provided, gain of this source is relative to that
				distance: float, optional
			Returns
				pressure level in pascals, not in dB logarithimc

		'''
		#print(x, y)
		dist = self.distance(x, y)
		mask = dist>distance_limit

		amplitude = np.where(mask, self.calculateAmplitude(dist, reference_level=reference_level), np.nan)
		phase = np.where(mask, self.calculatePhase(dist, k, w), np.nan)

		return amplitude, phase
		