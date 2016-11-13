import sys
from pqueue import event_queue, enqueue, dequeue, qempty
import event
import link
import host
import packet
import flow

from parser import parse


if __name__ == "__main__":
	# Read arguments to figure out what test case
	TEST_CASE = sys.argv[1]
	time = 0

	# Parser Configuration
	INFILE = './input/test_case_' + TEST_CASE

	# Lists of each object returned from the parser
	links, hosts, routers, flows = parse(INFILE)

	for flow in flows:
		flow.startFlow()

	'''
	# ============ Test case -1 ======================
	l1 = link.Link('L1', 10, 10, [])
	h1 = host.Host('H1', l1)
	h2 = host.Host('H2', l1)

	for i in "THIS IS A MESSAGE":
	    pkt = packet.Packet(h1, h2, i)
	    enqueue(event.SendPacket(1, pkt, h1.link))
	# END TEST CASE -1 ===================================
	'''

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