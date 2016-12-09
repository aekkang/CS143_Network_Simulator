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

def flows_done(flows):
    for f in flows:
        if f.done_sending is False:
            return False
    return True

def initial_bf(routers):
    for rtr in routers:
        rtr.reset_distvec()
        rtr.bf_updated = {}
        rtr.bf_changed = False

    for bf_round in range (len(routers)):
        for rtr in routers:
            for n_rtr in rtr.rneighbours:
                n_dvec = router.Router.r_map[n_rtr].bf_distvec
                n_rtr_link = rtr.rneighbours[n_rtr]
                rtr.update_bf(n_rtr, n_dvec, n_rtr_link, 0, False)

if __name__ == "__main__":
    
    # Check for verbose option
    for i in sys.argv:
        if i == "-v":
            sys.argv.remove(i)
            metrics.VERBOSE = True

    # Verify that a test case number was given
    if len(sys.argv) != 3:
        print "usage: python main.py [-v] [TEST_CASE_NO] [TCP_ALG]"
        sys.exit(-1)
    
    # Read arguments to figure out what test case and TCP algorithm to use
    TEST_CASE = sys.argv[1]
    flow.Flow.TCP_ALG = sys.argv[2]

    # Parser configuration
    INFILE = './input/test_case_' + TEST_CASE


    # Lists of each object returned from the parser
    hosts, links, routers, flows = parse(INFILE)
    
    metrics.link_ids = link.Link.l_map.keys()
    metrics.link_ids.sort()

    metrics.flow_ids = flow.Flow.f_map.keys()

    '''
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
    
    #             R2
    #         L1/    \L3
    # H1--L0--R1      R4--L1--H2
    #         L2\    /L4
    #             R3 

    if TEST_CASE == '2':
        router.Router.r_map['R1'].routing_table = {'R2': 'L1'}
        router.Router.r_map['R2'].routing_table = {'R1': 'L1',\
        'R3': 'L2'}
        router.Router.r_map['R3'].routing_table = {'R2': 'L2',\
        'R4': 'L3'}
        router.Router.r_map['R4'].routing_table = {'R3': 'L3'}
    '''
    
    link.Link.ids.sort()
    router.set_rneighbours()
    initial_bf(routers)

    enqueue(event.Reroute(0, 1))
    for flow in flows:
        flow.startFlow()

    while (qempty() == False and flows_done(flows) is False):
        event = dequeue()
        set_global_time(event.start_time)
        event.process()

        for lnk in links:
            lnk.update_metrics(get_global_time())
        for flow in flows:
            flow.update_metrics(get_global_time())

        metrics.report_metrics(get_global_time())
    
    metrics.plot_metrics(True, get_global_time())

    print ("SIMULATION END")

