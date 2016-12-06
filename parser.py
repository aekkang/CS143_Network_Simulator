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

import link as link_class
import host as host_class
import router as router_class
import flow as flow_class


def next_line(f, cast='s'):
    '''
    Reads a line in the file and strips it of white spaces and the newline
    character. An optional letter argument will cast it to a float or int.
    '''
    if cast == 'f':
        return float(f.readline().strip())
    elif cast == 'i':
        return int(f.readline().strip())

    return f.readline().strip()

def parse_hosts(f, l_map):
    hosts = []
    h_map = {}

    num_hosts = next_line(f, 'i')

    for i in xrange(num_hosts):
        addr = next_line(f)

        link_id = next_line(f)

        # Get the link object with that ID from the map
        host_link = l_map[link_id]

        host_id = next_line(f)

        # Construct host object, add it to host map and list
        h = host_class.Host(host_id, host_link)
        h_map[host_id] = h
        hosts.append(h)

        # Add the host as an 'end' to the link
        host_link.add_end(h)

    # Set the map for the host class
    host_class.Host.h_map = h_map

    return (hosts, h_map)

def parse_routers(f, l_map):
    routers = []
    r_map = {}
    r_links = []

    num_routers = int(next_line(f))

    for i in xrange(num_routers):
        addr = next_line(f)

        num_links = int(next_line(f))

        for j in xrange(num_links):
            link_id = next_line(f)
            
            r_links.append(link_id)

        router_id = next_line(f)

        # Construct router and update router map and list
        r = router_class.Router(router_id, r_links)
        r_map[router_id] = r
        routers.append(r)

        # Update the ends of the links connected to each router
        for l_id in r_links:
            mapped_link = l_map[l_id]
            mapped_link.add_end(r)

        # Reset r_links after each iteration
        r_links = []

    # Set the map for the router class
    router_class.Router.r_map = r_map

    return (routers, r_map)

def parse_links(f):
    links = []
    l_map = {}

    num_links = int(next_line(f))

    for i in xrange(num_links):
        link_id = next_line(f)

        # Input link rate is in MB/s. Convert to
        # pass link_rate into constructor in bytes per second
        link_rate = (next_line(f, 'f')) * 1e6 / 8
        # print link_rate

        # Input link delay is in milliseconds. Convert to
        # seconds when passing to constructor
        link_delay = next_line(f, 'f') * 0.001

        # Input buffer size is in MB.
        # Passing buffer size into constructor in bytes
        link_buffer_size = next_line(f, 'f') * 1e3
        # print link_buffer_size

        # Construct link and add to link map and list of links
        l = link_class.Link(link_id, link_rate, link_delay, link_buffer_size)
        l_map[link_id] = l
        links.append(l)

    # Set the map for the link class
    link_class.Link.l_map = l_map

    return (links, l_map)

def parse_flows(f, h_map):
    flows = []
    f_map = {}

    num_flows = int(next_line(f))

    for i in xrange(num_flows):
        flow_id  = next_line(f)

        # ID for the source of the flow
        flow_src = next_line(f)

        # Host object of the source
        src_host = h_map[flow_src]

        # ID for the destination of the flow
        flow_dest = next_line(f)

        # Host object of the destination
        dest_host = h_map[flow_dest]

        # Amount of data to be sent by the flow
        data_amount = next_line(f, 'i')

        # Flow start time
        flow_start_time = next_line(f, 'f')

        # Construct the flow, insert it into the map and append
        # it to the list of flows
        flow = flow_class.Flow(flow_id, src_host, dest_host, 
                            data_amount, flow_start_time)
        f_map[flow_id] = flow
        flows.append(flow)

    # Set the Flow class map
    flow_class.Flow.f_map = f_map

    return (flows, f_map)

def parse(file_name):
    f = open(file_name, 'r')

    links, l_map = parse_links(f)
    hosts, h_map = parse_hosts(f, l_map)
    routers, r_map = parse_routers(f, l_map)
    flows, f_map = parse_flows(f, h_map)

    f.close()

    return (hosts, links, routers, flows)
