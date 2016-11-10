from pqueue import event_queue, enqueue, dequeue, qempty
import event
import link
import host
import packet

time = 0


# Test case -1
l1 = link.Link('L1', 10, 10, [])
h1 = host.Host('H1', l1)
h2 = host.Host('H2', l1)

for i in "THIS IS A MESSAGE":
    pkt = packet.Packet(h1, h2, i)
    enqueue(event.SendPacket(1, pkt, h1.link))

while (qempty() == False):
    event = dequeue()
    time = event.start_time
    event.process()

print (time)
'''
trash

tp = packet.Packet(1,2)
tlink = link.Link(256, 10, [tp], [1,2])
cbev = event.CheckBuffer(0, tlink)
bdpev = event.BufferDoneProcessing(2, tlink)


enqueue(bdpev)
enqueue(cbev)
ev = dequeue()

'''