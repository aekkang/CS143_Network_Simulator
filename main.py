import sys
from pqueue import *
import event
import link
import host
import packet
import flow
import metrics

from parser import parse

if __name__ == "__main__":
    
    # Verify that a test case number was given
    if len(sys.argv) != 2:
        print "usage: python main.py [TEST_CASE_NO]"
        sys.exit(-1)
    
    # Read arguments to figure out what test case
    TEST_CASE = sys.argv[1]

    # Parser Configuration
    INFILE = './input/test_case_' + TEST_CASE


    # Lists of each object returned from the parser
    hosts, links, routers, flows = parse(INFILE)
    metrics.link_ids = link.Link.l_map.keys()
    metrics.link_ids.sort()

    # Hard-code routing tables for test-case 1
    if TEST_CASE == '1':
        routers[0].routing_table = {'H1': 'L0', 'H2': 'L1'}
        routers[1].routing_table = {'H1': 'L1', 'H2': 'L3'}
        routers[2].routing_table = {'H1': 'L2', 'H2': 'L4'}
        routers[3].routing_table = {'H1': 'L4', 'H2': 'L5'}

    for flow in flows:
        flow.startFlow()

    '''
    # ============ Test case -1 ======================
    l1 = link.Link('L1', 10, 10, [])
    h1 = host.Host('H1', l1)
    h2 = host.Host('H2', l1)
    l1.ends = [h1, h2]

    for i in "THIS IS A MESSAGE":
        pkt = packet.Packet(h1, h2, i)
        enqueue(event.SendPacket(1, pkt, h1.link, h1))
    # END TEST CASE -1 ===================================
    '''

    while (qempty() == False):
        event = dequeue()
        set_global_time(event.start_time)
        event.process()
        for link in links:
            link.update_metrics(get_global_time())
        metrics.report_metrics(get_global_time())
    metrics.plot_metrics(True, get_global_time())
    print ("SIMULATION END")
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