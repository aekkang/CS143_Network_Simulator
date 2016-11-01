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