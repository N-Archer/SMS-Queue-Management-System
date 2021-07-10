class Queue:

    def __init__(self):
        self._queue = []
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'

    def enqueue(self, item):
        self._queue.append(item)
        return self._queue
    def dequeue(self):
        return self._queue.pop(0)
    def get_queue(self):
        return self._queue
    def size(self):
        return len(self._queue) 