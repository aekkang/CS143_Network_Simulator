last_report_time = -1

# Link metrics
buffer_load = {}
packet_loss = {}
flow_rate = {}

link_ids = []

def update_link(link_id, bufload, pktloss, flowrate):
    global buffer_load, packet_loss, flow_rate
    buffer_load[link_id] = bufload
    packet_loss[link_id] = pktloss
    flow_rate[link_id] = flowrate

def report_metrics(time):
    global last_report_time
    if time > last_report_time:
        print_metrics(time)
        last_report_time = time

def print_metrics(time):
    global buffer_load, packet_loss, flow_rate
    print ("========================================")
    print ("Time: %.8fs" % time)

    for i in link_ids:
        print ("Link %s: [Buffer load: %.2f%%, Packet Loss: %d pkts, Flow rate: %.2f pkts/second]" % (i, buffer_load[i], packet_loss[i], flow_rate[i]))
    print ()