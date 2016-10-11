'''
Created on Sep 19, 2016

@author: TDARSEY
'''

from threading import Thread

import .logger
logger = Pingas.logger.initLogger()

import pyping
import numpy as np
from matplotlib import pyplot

import time

pyplot.ion()

class NetworkPlot(object): 
    def __init__(self, rolling_count = None):
        
        #super(NetworkPlot, self).__init__()
        
        self.startTime = time.time()
        
        self._lastPollTime = self.startTime
        
        
        self.rolling_count = rolling_count
        
        self.xData = np.array([], dtype=float) #Unix Time
        self.yData = np.array([], dtype=float) #Ping
        
        self.figure, self.ax = pyplot.subplots()
        self.lines, = self.ax.plot([],[])
        
        self.ax.set_autoscaley_on(True)
        self.ax.set_ylim( 0, 1000 )
        
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
            
    def setData(self, times, values):
        self.xData = np.array( times,  dtype=float )
        self.yData = np.array( values, dtype=float )
        logger.debug('New Values set for the plot')
        self.updatePlot()
        
    def updatePlot(self):
        
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(self.xData)
        self.lines.set_ydata(self.yData)
                
        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view(tight = None, scalex=True, scaley=False)
        logger.debug('Plot Updated')
        #We need to draw *and* flush
        
    def redrawPlot(self):
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        
    def tick(self):
        self.redrawPlot()
        
    def run(self):
        while True:
            self.tick()
    
if __name__ == "__main__":
    testNetworkPlot = NetworkPlot()
    testNetworkPlot.setData([1, 2, 3, 4, 5, 6, 7, 8], [2, 4, 8, 16, 32, 64, 128, 256])
    testNetworkPlot.run()
    testNetworkPlot.join()
    



#plt.subplots_adjust(hspace=0.9)
#plt.subplot(121)
#plt.hexbin(xRecord, yRecord, bins='log', cmap=plt.cm.YlOrRd_r)
#plt.plot(xRecord, yRecord)
#plt.axis([xmin, xmax, ymin, ymax], bins='log')
#plt.title("Average Ping")
#cb = plt.colorbar()
#cb.set_label('Ping (Log) ')

#plt.show()
