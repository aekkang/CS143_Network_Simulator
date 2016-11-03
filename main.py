from pqueue import event_queue, enqueue, dequeue, qempty
import event
import link
import host
import packet

time = 0

tp = packet.Packet(1,2)
tlink = link.Link(256, 10, [tp], [1,2])
cbev = event.CheckBuffer(0, tlink)
bdpev = event.BufferDoneProcessing(2, tlink)


enqueue(bdpev)
enqueue(cbev)
ev = dequeue()

'''
while True:
    if (not qempty()):
        event = dequeue()
        time = event.start_time
        event.process()
    else:
        time += 1                   #increment time (idk why)
    break

'''