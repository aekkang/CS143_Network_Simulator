import event
import Queue

event_queue = Queue.PriorityQueue()

def enqueue(evt):
    event_queue.put((evt.end_time, evt))

def dequeue():
    assert(not event_queue.empty())
    p, evt = event_queue.get()
    return evt

def qempty():
    return event_queue.empty()
