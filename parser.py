# The parser initializes a network given a series of
# hosts, routers, links and flows

# Assumes input is in this format

'''
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

n_l = number of links

For each link:
link_id
link_rate
link_delay
link_buffer_size


n_f = number of flows

For each flow:
flow_id
flow_src
flow_dest
data_amt
flow_start_time

'''

def next_line(f):
    return f.readline().strip()

TEST_CASE = '1'
INFILE = 'test_case_' + TEST_CASE

f = open(INFILE, 'r')

num_hosts = int(next_line(f))
print num_hosts

print "HOSTS\n"

for i in xrange(num_hosts):
    addr = next_line(f)
    print addr

    link_id = next_line(f)
    print link_id

    host_id = next_line(f)
    print host_id

    print

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

    print

num_flows = int(next_line(f))
print num_flows

'''
flow_id
flow_src
flow_dest
data_amt
flow_start_time
'''
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


f.close()
