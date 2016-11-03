from pqueue import event_queue, enqueue, dequeue, qempty
import event

time = 0
while True:
    if (not qmepty()):
        event = dequeue()
        time = event.start_time
        event.process()


