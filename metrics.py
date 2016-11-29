import matplotlib.pyplot as plt

last_report_time = -1

# Link metrics
buffer_load = {}
packet_loss = {}
flow_rate = {}

link_ids = []
times = {}

colors = ['r', 'g', 'b', 'y', 'k', 'c']

fig = plt.figure(figsize=(10, 10))

def get_link_num(link_id):
    return int(link_id[1:])

# appends an item to the end of a list mapped from a key in a dictionary
def dict_insert(key, d, item):
    if key not in d:
        d[key] = [item]
    else:
        d[key].append(item)

def update_link(link_id, bufload, pktloss, flowrate, time):
    global buffer_load, packet_loss, flow_rate, times

    dict_insert(link_id, buffer_load, bufload)
    dict_insert(link_id, packet_loss, pktloss)
    dict_insert(link_id, flow_rate, flowrate)
    dict_insert(link_id, times, time)

def report_metrics(time):
    global last_report_time
    if time > last_report_time + 10:
        plot_metrics(False, time)
        last_report_time = time

# def print_metrics(time):
#     global buffer_load, packet_loss, flow_rate
#     print ("========================================")
#     print ("Time: %.8fs" % time)

#     for i in link_ids:
#         print ("Link %s: [Buffer load: %.2f%%, Packet Loss: %d pkts, Flow rate: %.2f pkts/second]" % (i, buffer_load[i], packet_loss[i], flow_rate[i]))
    
#     print ()

def plot_metrics(final, time):
    global buffer_load, packet_loss, flow_rate, fig, times

    for i in link_ids:

        if get_link_num(i) not in [1, 2]:
            continue

        t = times[i]
        clr_str = colors[get_link_num(i)]

        ax_bl = fig.add_subplot(311)
        ax_bl.set_ylim((-1, 100))
        ax_bl.plot(t, buffer_load[i], color=clr_str, label=i, lw=0.4)
        ax_bl.set_xlabel('time')
        ax_bl.set_ylabel('buffer load')

        ax_pl = fig.add_subplot(312)
        ax_pl.set_ylim((-1, 50))
        ax_pl.set_xlabel('time')
        ax_pl.set_ylabel('packet loss')
        ax_pl.plot(t, packet_loss[i], color=clr_str, label=i)

        ax_fr = fig.add_subplot(313)
        ax_fr.set_ylim((-1, 2000))
        ax_fr.set_xlabel('time')
        ax_fr.set_ylabel('flow rate')
        ax_fr.plot(t, flow_rate[i], color=clr_str, label=i)

        plt.legend(loc='upper right')

    if final is False:
        plt.draw()
        plt.pause(0.5)
        plt.gcf().clear()

    else:
        print "Showing plot"
        plt.draw()
        plt.show()


