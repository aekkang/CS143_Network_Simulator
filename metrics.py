import matplotlib.pyplot as plt

last_report_time = -1

# Link metrics
buffer_load = {}
packet_loss = {}
flow_rate = {}

# Flow metrics
send_rate = {}
receive_rate = {}
round_trip_time = {}
window_sizes = {}

link_ids = []
flow_ids = []

l_times = {}
f_times = {}

colors = ['r', 'g', 'b', 'y', 'k', 'c', 'peru', 'fuchsia', 'teal', 'darkkhaki']
avg_color = 'plum'

fig = plt.figure(figsize=(10, 10))

def get_num(_id):
    return int(_id[1:])

# appends an item to the end of a list mapped from a key in a dictionary
def dict_insert(key, d, item):
    if key not in d:
        d[key] = [item]
    else:
        d[key].append(item)

def update_link(link_id, bufload, pktloss, flowrate, time):
    global buffer_load, packet_loss, flow_rate, l_times

    dict_insert(link_id, buffer_load, bufload)
    dict_insert(link_id, packet_loss, pktloss)
    dict_insert(link_id, flow_rate, flowrate)
    dict_insert(link_id, l_times, time)

def update_flow(flow_id, send_r, rec_r, rtts, w_size, time):
    global send_rate, receive_rate, round_trip_time

    dict_insert(flow_id, send_rate, send_r)
    dict_insert(flow_id, receive_rate, rec_r)
    dict_insert(flow_id, round_trip_time, rtts)
    dict_insert(flow_id, window_sizes, w_size)
    dict_insert(flow_id, f_times, time)

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
    global buffer_load, packet_loss, flow_rate, fig, l_times, f_times, \
        send_rate, receive_rate, round_trip_time, window_sizes

    for i in link_ids:

        # if get_num(i) not in [0, 1, 2, 5]:
        #     continue

        t = l_times[i]
        clr_str = colors[get_num(i)]

        ax_fr = fig.add_subplot(611)
        ax_fr.set_ylim((-1, 2000))
        ax_fr.set_xlabel('time')
        ax_fr.set_ylabel('link rate')
        ax_fr.plot(t, flow_rate[i], color=clr_str, label=i)

        ax_pl = fig.add_subplot(612)
        ax_pl.set_ylim((-1, 100))
        ax_pl.set_xlabel('time')
        ax_pl.set_ylabel('packet loss')
        ax_pl.plot(t, packet_loss[i], color=clr_str, label=i)

        plt.legend(loc='upper right', prop={'size': 9})

        ax_bl = fig.add_subplot(613)
        ax_bl.set_ylim((-1, 100))
        ax_bl.plot(t, buffer_load[i], color=clr_str, label=i, lw=0.4)

        ax_bl.set_xlabel('time')
        ax_bl.set_ylabel('buffer load')

    for i in flow_ids:

        t = f_times[i]
        clr_str = colors[get_num(i)]

        ax_sr = fig.add_subplot(614)
        ax_sr.plot(t, send_rate[i], color=clr_str, label=i)
        ax_sr.plot(t, receive_rate[i], color='lightsage', label=i)
        ax_sr.set_xlabel('time')
        ax_sr.set_ylabel('send/receieve rate')

        ax_ws = fig.add_subplot(615)
        ax_ws.plot(t, window_sizes[i], color=clr_str, label=i, lw=0.2)
        ax_ws.set_xlabel('time')
        ax_ws.set_ylabel('window size')

        # avg_ws = []
        # sum_ = 0
        # for j in xrange(len(window_sizes[i])):
        #     avg_ws.append((sum_ + window_sizes[i][j]) / t[j])

        # ax_ws.plot(t, avg_ws, color=avg_color, label=i)

        ax_rtt = fig.add_subplot(616)
        ax_rtt.plot(t, round_trip_time[i], color=clr_str, label=i, lw=0.2)
        ax_rtt.set_xlabel('time')
        ax_rtt.set_ylabel('round trip time')

        plt.legend(loc='lower right', prop={'size': 9})

    # TODO? Per host metrics. But in our test cases, none of the flows share
    # a common host for a source or destination


    if final is False:
        plt.draw()
        plt.pause(0.5)
        plt.gcf().clear()

    else:
        print "Showing plot"
        plt.draw()
        plt.show()


