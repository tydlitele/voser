import numpy as np

p_ref = 20e-6
'''0 dB in pascals reference '''


def dBTop(d):
	'''
		Converts wave amplitude from logarithmic scale
		Parameters:
			d (float): wave amplitude in dB
		Returns:
			wave amplitude in pascals

	'''
	return np.power(10, d/20)*p_ref

def pTodB(p):
	'''
		Converts wave amplitude to logarithmic scale
		Parameters:
			p (float): wave amplitude in pascals
		Returns:
			wave amplitude in dB

	'''
	return 20*np.log10(p/p_ref)

#quick and dirty test, sorry
'''
a=np.array([1,2,3,4])
print(a)
b=pTodB(a)
print(b)
c=dBTop(b)
print(c)
'''