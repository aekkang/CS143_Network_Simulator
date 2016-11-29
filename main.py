import sys
from pqueue import *
import event
import link
import host
import packet
import flow
import metrics
import router

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
    if TEST_CASE == '1' or TEST_CASE == '3':
        routers[0].routing_table = {'H1': 'L0', 'H2': 'L1',\
        'R2':'L1', 'R3':'L2', 'R4':'L1'}
        routers[1].routing_table = {'H1': 'L1', 'H2': 'L3',\
        'R1':'L1', 'R4':'L3', 'R3':'L1'}
        routers[2].routing_table = {'H1': 'L2', 'H2': 'L4',\
        'R1':'L2', 'R4':'L4', 'R2':'L2'}
        routers[3].routing_table = {'H1': 'L3', 'H2': 'L5',\
        'R1':'L3', 'R2':'L3', 'R3':'L4'}

    router.set_rneighbours()
    link.Link.ids.sort()

    enqueue(event.Reroute(0, 1))
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

        for lnk in links:
            lnk.update_metrics(get_global_time())
        metrics.report_metrics(get_global_time())
    
    metrics.plot_metrics(True, get_global_time())

    print ("SIMULATION END")
