import matplotlib.pyplot as plt

last_report_time = -1

# Link metrics
buffer_load = {}
packet_loss = {}
flow_rate = {}

link_ids = []


def get_link_num(link_id):
    return int(link_id[1:])

def update_link(link_id, bufload, pktloss, flowrate):
    global buffer_load, packet_loss, flow_rate
    buffer_load[link_id] = bufload
    packet_loss[link_id] = pktloss
    flow_rate[link_id] = flowrate

def report_metrics(time):
    global last_report_time
    if time > last_report_time + 0.25:
        #print_metrics(time)
        plot_metrics()
        last_report_time = time

def print_metrics(time):
    global buffer_load, packet_loss, flow_rate
    print ("========================================")
    print ("Time: %.8fs" % time)

    for i in link_ids:
        print ("Link %s: [Buffer load: %.2f%%, Packet Loss: %d pkts, Flow rate: %.2f pkts/second]" % (i, buffer_load[i], packet_loss[i], flow_rate[i]))
    

    print ()

def plot_metrics():
    global buffer_load, packet_loss, flow_rate

    link_id_num = []
    b_load_num = []
    p_loss_num = []
    f_rate_num = []

    for i in link_ids:
        link_id_num.append(get_link_num(i))

    for i in link_ids:
        # print ("Link %s: [Buffer load: %.2f%%, Packet Loss: %d pkts, Flow rate: %.2f pkts/second]" % (i, buffer_load[i], packet_loss[i], flow_rate[i]))
        b_load_num.append(buffer_load[i])
        p_loss_num.append(packet_loss[i])
        f_rate_num.append(flow_rate[i])


    plt.xlim([-1, 6])
    plt.gcf().clear()
    plt.plot(link_id_num, b_load_num, "r--", link_id_num, p_loss_num, "bs", link_id_num, f_rate_num, "g^")
    # plt.show()
    plt.draw()
    plt.pause(0.01)

