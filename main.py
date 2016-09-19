'''
Created on Sep 19, 2016

@author: TDARSEY
'''

import pyping


import numpy as np
import matplotlib.pyplot as plt
from numpy.core.multiarray import dtype

import time
from pyping.core import Ping

plt.ion()



class PingGraph(object):
 
    def __init__(self, period = 1, rolling_count = None):
        
        self.startTime = time.time()
        
        self._lastPollTime = self.startTime
        
        self.period = period
        self.timeout = self.period
        
        self.rolling_count = rolling_count
        
        self.xData = np.array([], dtype=float) #Unix Time
        self.yData = np.array([], dtype=float) #Ping
        
        self.figure, self.ax = plt.subplots()
        self.lines, = self.ax.plot([],[])
        
        self.ax.set_autoscaley_on(True)
        self.ax.set_ylim(0, self.timeout * 1000 )
        #Other stuff
        self.ax.grid()
        #self.ax.set_aspect('auto', adjustable='datalim', anchor='SW')
        #self.ax.ticklabel_format(useOffset=True, style='sci')
        self.ax.set_xticks([])
        
        self.figure.tight_layout(renderer=None, pad=0, h_pad=None, w_pad=None, rect=None)
                
        """
        plt.plot(xRecord, yRecord)
        plt.axis([xmin, xmax, ymin, ymax], bins='log')
        plt.title("Average Ping")
        """
    def updatePlot(self):
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(self.xData)
        self.lines.set_ydata(self.yData)
        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view(tight = None, scalex=True, scaley=False)
        #We need to draw *and* flush
        
    def redrawPlot(self):
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        
    def addRecord(self, data):
        x, y = data
        self.xData = np.append( self.xData, [x] )
        self.yData = np.append( self.yData, [y] )
        
        if (self.rolling_count and len(self.xData) > self.rolling_count):
            self.xData = np.delete( self.xData, 0 )
            self.yData = np.delete( self.yData, 0 )

    def pollData(self):
        ping_request = pyping.ping('google.com', self.period * 1000 , 1) #Host, Timeout, Packet size
        averagePing = ping_request.avg_rtt
        if( not averagePing ):
            averagePing = 0.0
        
        x = time.time() - self.startTime
        y = float(averagePing)
        
        self._lastPollTime = time.time()
        
        return x, y

    def run(self):
        while True:
            if(time.time() - self._lastPollTime > self.period):
                self.addRecord(self.pollData())
                self.updatePlot()
            self.redrawPlot()

    
    
PingGraph(
        rolling_count = 100,
        period = 0.1
    ).run()



#plt.subplots_adjust(hspace=0.9)
#plt.subplot(121)
#plt.hexbin(xRecord, yRecord, bins='log', cmap=plt.cm.YlOrRd_r)
#plt.plot(xRecord, yRecord)
#plt.axis([xmin, xmax, ymin, ymax], bins='log')
#plt.title("Average Ping")
#cb = plt.colorbar()
#cb.set_label('Ping (Log) ')

#plt.show()
