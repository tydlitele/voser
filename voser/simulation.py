from PyQt5 import QtCore
from dataModel import *
import math
import numpy as np
import source

distance_limit = 1
Pref = 20e-6



#this wolud work and would be nice and kinda pythonic
#but terribly inefficient
#i am leaving it here for now, altough this code isn't really used
#oh, and this works on units of acoustis pressure (~Pa), not logarithmic (~dB)
class cosWave:
    def __init__(self, a, phi):
        self.a = a
        self.phi = phi

    def __init__(self, distance, dref, k, phi): #dref: reference level in dB, phi: phase shift of original source
        self.a = dref + 20*np.log10(1/distance)
        self.phi = phi + distance*k

    def __add__(self, other):
        s=self.a*math.sin(self.phi) + other.a*math.sin(other.phi)
        c=self.a*math.cos(self.phi) + other.a*math.cos(other.phi)
        a = np.sqrt(np.pow(c, 2) + np.pow(s, 2))
        phi = np.arctan2(s/c)
        return cosWave(a, phi)



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


def pascalsTodB(P):
    return 20*np.log10(P/Pref)


class Simulator:
    def __init__(self):

        sub1 = source.Source(-1, 0, True, False, 0, 0)
        sub2= source.Source(1, 0, True, False, 0, 0)
        
        initialList=[sub1, sub2]
        self.sourcesModel = SourcesModel(initialList)

        self.xmin = -15
        self.xmax = 15
        self.ymin = -15
        self.ymax = 15


        self.xsamples = 150
        self.ysamples = 150
        

        #Sound pressure level [dBa @ 1m]
        self.D_ref = 90

        self.f = 100
        self.v = 300

    def k(self):
        return (2*np.pi * self.f/self.v)

    def getSourcesModel(self):
        return self.sourcesModel

    def computeGrid(self):
        x_width = (self.xmax-self.xmin)/self.xsamples
        y_width = (self.ymax-self.ymin)/self.ysamples
        self.x_coords = np.linspace(self.xmin+.5*x_width, self.xmax-.5*x_width, num=self.xsamples)
        self.y_coords = np.linspace(self.xmin+.5*x_width, self.xmax-.5*x_width, num=self.xsamples)
        

        #now I will take sources into account
        #first select active ones

        processedSources = [source[:] for source in self.sourcesModel.sources if source.active]
        self.sources_array = np.asarray(processedSources, dtype=np.float64)


        #print(self.sources_array)


        distances_array = np.empty((self.xsamples, self.ysamples, self.sources_array.shape[0]), dtype=np.float64)

        #this is probably quite inefficient :(
        #hopefully I will get to it later
        for i in range(self.xsamples):
            for j in range(self.ysamples):
                #print(self.distances(self.x_coords[i], self.y_coords[j]))
                distances_array[i, j, :] = self.distances(self.x_coords[i], self.y_coords[j])

        print(distances_array.shape)

        pressure_array = np.apply_along_axis(self.pressure, 2, distances_array)
        phase_shift_array = np.apply_along_axis(self.phaseShift, 2, distances_array)

        #another dirty hack
        #I think I should have thnough about this before
        self.a_array = np.empty((self.xsamples, self.ysamples), dtype=np.float64)
        self.phi_array = np.empty((self.xsamples, self.ysamples), dtype=np.float64)

        for i in range(self.xsamples):
            for j in range(self.ysamples):
                #print(self.distances(self.x_coords[i], self.y_coords[j]))
                a, phi = superposeWaveArray(pressure_array[i, j, :], phase_shift_array[i, j, :])
                self.a_array[i, j] = a
                self.phi_array[i, j] = phi


        self.result_db = pascalsTodB(self.a_array)
        '''
        from matplotlib import pyplot as plt
        plt.imshow(self.result_db)
        plt.show()
        '''

        print(pressure_array.shape)
        print(phase_shift_array.shape)


    def pressure(self, distances):
        P1 = Pref*np.exp((self.D_ref + self.sources_array[:, 5])/20)
        return P1/distances


    def phaseShift(self, distances):
        timeShift = self.k()*distances 
        inversions = self.sources_array[:, 3]
        return (timeShift + np.pi*inversions)

    def distance(self, x1, y1, sourceNum):
        if(isinstance(sourceNum, int)):
            x2=self.sources_array[sourceNum, 0]
            y2=self.sources_array[sourceNum, 1]

        else:
            raise("enter source index as parameter")
        return(np.sqrt((x1-x2)**2 + (y1-y2)**2))


    def distances(self, x, y):
        distances = np.empty(self.sources_array.shape[0], dtype=np.float64)

        for i in range(self.sources_array.shape[0]):
            distances[i] = self.distance(x, y, i)
            
        #distances = distance(self.sourcesModel.sources, x, y)
        #print(distances)
        return distances


