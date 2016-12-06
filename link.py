import packet
import metrics
from pqueue import get_global_time, global_time
PACKET_SIZE = 1024.0

class Link:
    ids = []

    # Map of link ids to Link objects, this will be populated by the parser
    l_map = {}

    def __init__(self, link_id, rate, prop_delay, buffer_size):
        self.id = link_id
        Link.ids.append(self.id)

        self.rate = rate       # in bytes per second
        self.prop_delay = prop_delay

        # buffer size is passed in in bytes
        self.buffer_size = buffer_size

        self.buffer = []
        self.buf_processing = False
        self.size_in_transit = 0

        # In bytes
        self.buffer_load = 0
        self.buffer_pkts = 0

        # Bellman-Ford link cost
        self.bf_lcost = 1

        # Ends is a list that contains the object on either side of the list.
        # Its size at any time should be at most two.
        self.ends = []

        # Metric lists
        self.lost_packets = 0
        self.prev_lost_packets = 0
        self.prev_packetloss = 0
        self.aggr_flow_rate = 0
        self.prev_flow_rate = 0
        self.prev_time = 0


    def add_end(self, entity):
        assert(len(self.ends) < 2)
        self.ends.append(entity)

    def get_receiver(self, sender):
        assert(sender in self.ends)
        if self.ends[0] == sender:
            return self.ends[1]
        return self.ends[0]

    def buffer_add(self, buf_obj):
        # Buffer objects are (packet, time) tuples
        pkt, time = buf_obj

        # Drop packet if the buffer is full
        if self.buffer_load >= self.buffer_size:
            self.lost_packets += 1
            print ("Dropped a packet. Now at: %d" % self.lost_packets)
            return

        self.buffer.append(buf_obj)
        if isinstance(pkt, packet.DataPkt):
            self.aggr_flow_rate += pkt.size * 8
        self.buffer_load += pkt.size
        self.buffer_pkts += 1


    def buffer_get(self):
        pkt, time = self.buffer.pop(0)
        self.buffer_load -= pkt.size
        self.buffer_pkts -= 1
        self.size_in_transit = pkt.size
        return (pkt, time)

    def buffer_empty(self):
        return len(self.buffer) == 0

    def update_metrics(self, time):
        bufload = self.buffer_pkts
        pktloss = self.lost_packets - self.prev_lost_packets
        self.prev_lost_packets = self.lost_packets

        if time >= self.prev_time + 0.1:
            link_rate = (self.aggr_flow_rate - self.prev_flow_rate)\
                        / (1024 ** 2 * (time - self.prev_time))

            self.prev_time = time
            self.prev_flow_rate = self.aggr_flow_rate
            update_link_rate = True

            
        else:
            link_rate = 0
            update_link_rate = False
                  
        metrics.update_link(self.id, bufload, pktloss, link_rate, time, update_link_rate)

    def set_linkcost(self):
        self.bf_lcost = self.buffer_load + 1
        if self.buf_processing:
            self.bf_lcost += self.size_in_transit

    def __str__(self):
        return "<Link ID: " + str(self.id) + ", Link Rate: " + str(self.rate) + \
            ", Propogation Delay: " + str(self.prop_delay) + ", Buffer size: " + \
            str(self.buffer_size) + ", Buffer load: " + str(self.buffer_load) +\
             ", Ends: " + str(self.ends) + "ENDS>\n"

    __repr__ = __str__


def set_linkcosts():
    for link_id in Link.ids:
        Link.l_map[link_id].set_linkcost()
