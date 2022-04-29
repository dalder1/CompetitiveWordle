###
### Daniel Alderman, Ann Marie Burke, Ethan Schreiber
### CS 21 Concurrent Programming
### Spring 2022
### Project: Wordle with Friends
### WorkQueue.py:
###     Implementation of a work queue utilizing condition objects
###

import threading

class WorkQueue():
    def __init__(self):
        '''
        Constructor, initializes work queue, lock, and condition variable
        '''
        self.workList = []
        self.queueLock = threading.Lock()
        self.workAvailable = threading.Condition(self.queueLock)
    
    def isWork(self):
        '''
        predicate for wait_for, returns false if the queue is empty else true
        '''
        if self.workList:
            return True
        else:
            return False
    
    def addWork(self, work):
        '''
        add work to the queue in thread-safe manner
        '''
        with self.queueLock:
            self.workList.append(work)
            self.workAvailable.notify()
    
    def getWork(self):
        '''
        get work from queue in thread-safe manner, waiting if no work available
        '''
        with self.queueLock:
            while(not self.workList):
                # we use wait_for so that if the cond_var is notified before
                # a thread is ready, we still check if there is work
                self.workAvailable.wait_for(self.isWork)
            work = self.workList.pop(0)
        return work
