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

    # Order link IDs for consistent metric reporting
    metrics.link_ids = link.Link.l_map.keys()
    metrics.link_ids.sort()
    link.Link.ids.sort()

    metrics.flow_ids = flow.Flow.f_map.keys()


    # Initial BF routing
    router.set_rneighbours()
    initial_bf(routers)

    # Set rerouting to happen periodically
    enqueue(event.Reroute(event.Reroute.WAIT_INTERVAL, 1))

    for flow in flows:
        flow.startFlow()

    while (qempty() == False and flows_done(flows) is False):
        event = dequeue()
        set_global_time(event.start_time)
        event.process()

        # Update link and flow metrics
        for lnk in links:
            lnk.update_metrics(get_global_time())
        for flow in flows:
            flow.update_metrics(get_global_time())

        metrics.report_metrics(get_global_time())
    
    metrics.plot_metrics(True, get_global_time())

    print ("SIMULATION END")

