# this represents a queue except for a music playlist not random elements

# useless rn



from queue import Queue

class Q:
    def __init__(self):
        self.queue = Queue()

    def add(self, songName):
        self.queue.put(songName)
    
    def remove(self, songName):
        self.queue.queue.remove(songName)

    def next(self):
        return self.queue.get()

#q = Q()
#q.t('a')
#list(q.queue.queue)