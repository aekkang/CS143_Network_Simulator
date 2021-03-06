import matplotlib.pyplot as plt

# Get rid of matplotlib warnings
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

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
lr_times = {}
fr_times = {}
f_times = {}

VERBOSE = False

colors = ['yellowgreen', 'cornflowerblue', 'salmon', 'mediumpurple', \
          'goldenrod', 'mediumaquamarine', 'darkblue', 'orchid', \
          'mediumvioletred', 'cadetblue']
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

# Update link metrics
def update_link(link_id, bufload, pktloss, flowrate, time, update_link_rate):
    global buffer_load, packet_loss, flow_rate, l_times

    dict_insert(link_id, buffer_load, bufload)
    dict_insert(link_id, packet_loss, pktloss)
    dict_insert(link_id, l_times, time)
    
    # Only update link rate in discrete time intervals
    if update_link_rate:
        dict_insert(link_id, flow_rate, flowrate)
        dict_insert(link_id, lr_times, time)

# Update flow metrics
def update_flow(flow_id, send_r, rec_r, rtts, w_size, time, update_flow_rate):
    global send_rate, receive_rate, round_trip_time

    dict_insert(flow_id, send_rate, send_r)
    
    # Only update flow rate in discrete time intervals
    if update_flow_rate:
        dict_insert(flow_id, receive_rate, rec_r)
        dict_insert(flow_id, fr_times, time)

    dict_insert(flow_id, round_trip_time, rtts)
    dict_insert(flow_id, window_sizes, w_size)
    dict_insert(flow_id, f_times, time)

def report_metrics(time):
    global last_report_time
    if time > last_report_time + 10:
        plot_metrics(False, time)
        last_report_time = time


def plot_metrics(final, time):
    global buffer_load, packet_loss, flow_rate, fig, l_times, f_times, \
        send_rate, receive_rate, round_trip_time, window_sizes

    for i in link_ids:
        if get_num(i) not in [1, 2, 3]:
            continue

        t = l_times[i]
        clr_str = colors[get_num(i)]

        ax_fr = fig.add_subplot(611)
        ax_fr.set_ylim((-1, 10))
        ax_fr.set_xlabel('time (s)')
        ax_fr.set_ylabel('link rate\n(Mbps)')
        ax_fr.plot(lr_times[i], flow_rate[i], color=clr_str, label=i)

        ax_bl = fig.add_subplot(612)
        ax_bl.set_ylim((-1, 140))
        ax_bl.set_xlabel('time (s)')
        ax_bl.set_ylabel('buffer load\n(pkts)')
        ax_bl.plot(t, buffer_load[i], color=clr_str, label=i, lw=0.3)

        ax_pl = fig.add_subplot(613)
        ax_pl.set_ylim((-1, 10))
        ax_pl.set_xlabel('time (s)')
        ax_pl.set_ylabel('packet loss\n(pkts)')
        ax_pl.plot(t, packet_loss[i], color=clr_str, label=i)

        plt.legend(loc='upper right', prop={'size': 9})

    for i in flow_ids:
        t = f_times[i]
        clr_str = colors[get_num(i)]

        ax_sr = fig.add_subplot(614)

        ax_sr.set_xlabel('time (s)')
        ax_sr.set_ylabel('flow rate\n(Mbps)')
        ax_sr.plot(fr_times[i], receive_rate[i], color=clr_str, label=i)

        ax_ws = fig.add_subplot(615)
        ax_ws.plot(t, window_sizes[i], color=clr_str, label=i, lw=1.0)
        ax_ws.set_xlabel('time (s)')
        ax_ws.set_ylabel('window size\n(pkts)')

        ax_rtt = fig.add_subplot(616)
        ax_rtt.plot(t, round_trip_time[i], color=clr_str, label=i, lw=1.0)
        ax_rtt.set_xlabel('time (s)')
        ax_rtt.set_ylabel('round trip time')

        plt.legend(loc='lower right', prop={'size': 9})


    if final is False:
        plt.draw()
        plt.pause(0.5)
        plt.gcf().clear()

    else:
        print "Showing plot"
        plt.draw()
        plt.show()

def cprint(*args):
    if VERBOSE:
        print (" ".join((map(str, args))))
