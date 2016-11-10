# The parser initializes a network given a series of
# hosts, routers, links and flows

# Assumes input is in this format



'''

n_l = number of links

For each link:
link_id
link_rate
link_delay
link_buffer_size

n_h = number of hosts

For each host:
network_address
connecting_link
host_id

n_r = number of routers

For each router:
network_address
number of connected links
link_1 ... link_n
router_id

n_f = number of flows

For each flow:
flow_id
flow_src
flow_dest
data_amt
flow_start_time

'''

# Kevin Thoughts
# Construct object in order

# Links, Routers/Hosts, Packets (importance is links first, really)


# A Problem: I'd have to create the id->object maps for the links, routers,
# hosts, flows in the parser itself while the maps are being generated in the
# classes also

# Possibility: generate the maps in the parser class and pass them to the 
# classes. (How to do this?)

# See here: https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide

import link as link_class
import host as host_class

TEST_CASE = '1'
INFILE = './input/test_case_' + TEST_CASE

def next_line(f, cast='s'):
    if cast == 'f':
        return float(f.readline().strip())
    elif cast == 'i':
        return int(f.readline().strip())

    return f.readline().strip()

def parse_hosts(f, l_map):
    hosts = []
    h_map = {}

    num_hosts = next_line(f, 'i')
    print num_hosts

    print "HOSTS\n"

    for i in xrange(num_hosts):
        addr = next_line(f)
        print addr

        link_id = next_line(f)
        print link_id
        host_link = l_map[link_id]
        print host_link

        host_id = next_line(f)
        print host_id

        h = host_class.Host(host_id, host_link)
        h_map[host_id] = h
        hosts.append(h)

        print

    return (hosts, h_map)

def parse_routers(f, l_map):
    num_routers = int(next_line(f))
    print num_routers

    if num_routers > 0:
        print "ROUTERS\n"

    for i in xrange(num_routers):
        addr = next_line(f)
        print addr

        num_links = int(next_line(f))
        print num_links

        for j in xrange(num_links):
            link = next_line(f)
            print link

        router_id = next_line(f)
        print router_id

        print

def parse_links(f):
    links = []
    l_map = {}

    num_links = int(next_line(f))
    print num_links

    print "LINKS\n"

    for i in xrange(num_links):
        link_id = next_line(f)
        print link_id

        link_rate = next_line(f)
        print link_rate

        link_delay = next_line(f)
        print link_delay

        link_buffer_size = next_line(f)
        print link_buffer_size

        l = link_class.Link(link_id, link_rate, link_delay, link_buffer_size)
        l_map[link_id] = l
        links.append(l)

        print

    return (links, l_map)

def parse_flows(f):
    num_flows = int(next_line(f))
    print num_flows

    print "FLOWS\n"

    for i in xrange(num_flows):
        flow_id  = next_line(f)
        print flow_id, type(flow_id)

        flow_src = next_line(f)
        print flow_src

        flow_dest = next_line(f)
        print flow_dest

        data_amount = next_line(f)
        print data_amount

        flow_start_time = next_line(f)
        print flow_start_time

        print

def parse(file_name):
    f = open(file_name, 'r')

    links = []
    l_map = {}

    hosts = []
    h_map = {}

    routers = []
    flows = []

    links, l_map = parse_links(f)
    hosts, h_map = parse_hosts(f, l_map)
    parse_routers(f, l_map)
    parse_flows(f)

    f.close()

    print links, l_map, len(links)
    print
    print hosts, h_map, len(hosts)
    print

parse(INFILE)
