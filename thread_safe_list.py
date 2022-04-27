import threading

class Thread_Safe_List():
    def __init__(self):
        '''
        Constructor, initializes list, and lock
        '''
        self.list = []
        self.list_lock = threading.Lock()
    
    def append(self, elem):
        '''
        adds elem to list
        '''
        self.list_lock.acquire()
        self.list.append(elem)
        self.list_lock.release()
    
    def remove(self, elem):
        '''
        removes elem from list
        '''
        self.list_lock.acquire()
        self.list.remove(elem)
        self.list_lock.release()
    
    def __getitem__(self, key):
        '''
        overload array access
        '''
        self.list_lock.acquire()
        if key >= len(self.list):
            self.list_lock.release()
            raise IndexError('End')
        elem = self.list[key]
        self.list_lock.release()
        return elem
