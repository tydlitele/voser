from PyQt5 import QtCore
#from dataModel import *
import math
import numpy as np
import source
import basic_functions

distance_limit = 1
Pref = 20e-6




def superposeWaveArray(a_array, phi_array):
    a = 0
    phi = 0

    for a2, phi2 in zip(a_array, phi_array):
        a, phi = superpose2Waves(a, phi, a2, phi2)

    return (a, phi)


def superpose2Waves(a1, phi1, a2, phi2):
    s=a1*np.sin(phi1) + a2*np.sin(phi2)
    c=a1*np.cos(phi1) + a2*np.cos(phi2)

    return (np.sqrt(s**2 + c**2), np.arctan(s/c))

def coords1d(beg, end, samples):
    width = (end-beg)/samples
    coords = np.linspace(beg + .5*width, end-.5*width, samples)
    return coords

class Simulator:
    def __init__(self):
        self.sources = []

        self.xmin = -25
        self.xmax = 25
        self.ymin = -25
        self.ymax = 25


        self.xsamples = 200
        self.ysamples = 200
        
        self.distance_limit = 1.

        #Sound pressure level [dBa @ 1m]
        self.D_ref = 90

        self.f = 100
        self.v = 300

    def k(self):
        return (self.w()/self.v)

    def w(self):
        return 2*np.pi*self.f

   
    def initializeSources(self, sources):
        '''
            Accepts list of sources
        '''
        #i may just simply delete current list and create a new one
        #since following computations will be more time expensive
        self.sources = []

        #[print(*i) for i in sources]
        self.sources= [source.Source(*i) for i in sources]
        #print(self.sources)
        print("Simulator loaded {} sources".format(len(self.sources)))
 
    def coords(self, xmin=None, xmax=None, ymin=None, ymax=None, xsamples=None, ysamples=None):
        '''
            returns a tuple of np arrays
            for x and y rectangular grid
        '''
        if xmin:
            self.xmin = xmin
        if xmax:
            self.xmax = xmax
        if ymin:
            self.ymin = ymin
        if ymax:
            self.ymax = ymax
        if xsamples:
            self.xsamples = xsamples
        if ysamples:
            self.ysamples = ysampels

        x_coords = coords1d(self.xmin, self.xmax, self.xsamples)
        y_coords = coords1d(self.ymin, self.ymax, self.ysamples)

        return (x_coords, y_coords)



    def compute(self, sources=None):
        if sources:
            self.initializeSources(sources)

        x_coords, y_coords = self.coords();

        x_mesh, y_mesh = np.meshgrid(x_coords, y_coords)

        distances = np.asarray([i.distance(x_mesh, y_mesh) for i in self.sources])

        n = len(self.sources)

        #now calculate amplitude and phase for every source in every point
        #I dont like this part
        #seem too naive and not very "pythonic" and "numpyic"

        amplitudes = np.empty((self.xsamples, self.ysamples, len(self.sources)))
        phases = np.empty((self.xsamples, self.ysamples, len(self.sources)))
        
        for i in range(n):
            amplitudes[:, :, i], phases [:, :, i] = self.sources[i].vawe(x_mesh, y_mesh, self.k(), self.w(), reference_level=self.D_ref, distance_limit=self.distance_limit)


        #and now this is even worse
        #any hints how to vectorise this?
        amplitude = np.empty((self.xsamples, self.ysamples))
        phase = np.empty((self.xsamples, self.ysamples))


        for i in range (self.xsamples):
            for j in range (self.ysamples):
                amplitude[i, j], phase[i, j] = superposeWaveArray(amplitudes[i, j, :], phases[i, j, :])

        self.result = basic_functions.pTodB(amplitude)
        return(amplitude, phase)


        #print(basic_functions.pTodB(self.sources[0].calculateAmplitude(2, reference_level=self.D_ref)))

    def xRange(self):
        return self.xmin, self.xmax
    def yRange(self):
        return self.ymin, self.ymax