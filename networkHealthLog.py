'''
Created on Sep 20, 2016

@author: TDARSEY
'''

import pyping
import time

from Pingas.newtorkPlot import NetworkPlot

import Pingas.logger
logger = Pingas.logger.initLogger()

import threading

class Record(object):
    def __init__(self, time, response):
        self.time = time
        self.response = response

    def __lt__(self, other):
        if other.time:
            if self.time < other.time:
                return True
        return False
        
class NetworkHealthLog(threading.Thread):
    def __init__(self):
        super(NetworkHealthLog, self).__init__()
        
        self.alive = True
        
        self.onTick = None
        
        self.pingCount = 1
        self.period = 1.0/10
        self.timeout = 1000
        self.records = []
        
    def addRecord(self, time, response):
        record = Record(time, response)
        self.records.append(record)
        if(len(self.records) > 1 and time < self.records[-2].time):
            self.records = sorted(self.records)

        
    def getRecordsForPlot(self):
        returnRecords = ([], [])
        
        for record in self.records:
            returnRecords[0].append(record.time)
            returnRecords[1].append(record.response.avg_rtt)
            
        return returnRecords
    
    def poll(self):
        now = time.time()
        ping_response = pyping.ping('google.com', self.period * 1000 , 1) #Host, Timeout, Packet size            
        self.addRecord(now, ping_response)
        logger.info("Ping:\t%sms", ping_response.avg_rtt)
        
    def setOnTickCallbakc(self, callback):
        self.onTick = callback

    def softStop(self):
        self.alive = False

    def run(self):
        while self.alive:
            self.poll()
            self.onTick()
            time.sleep(1)
            
if __name__ == "__main__":
    
    testNetworkPlot = NetworkPlot()
    nhl = NetworkHealthLog()
    
    def updateNetworkPlot():
        records = nhl.getRecordsForPlot()
        testNetworkPlot.setData(records[0], records[1])
    
    nhl.setOnTickCallbakc(updateNetworkPlot)
    
    try:
        nhl.start()
        testNetworkPlot.run()
    except:
        logger.info('NHL ending.')
        nhl.softStop()
    finally:
        nhl.join()
        logger.info('NHL Thread Joined.')
    #pingGraph = NetworkPlot()
    
    
    """
    while True:
        nhl.tick()
        data = nhl.getRecordsForPlot()
        print data
        pingGraph.setData(data[0], data[1])
        pingGraph.updatePlot()
        pingGraph.redrawPlot()
    """
    
    
    #nhl.run()