'''
Created on Sep 23, 2016

@author: TDARSEY
'''

def initLogger():
    
    import logging
    logger = logging.getLogger('nhl')
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.INFO)
    
    return logger
