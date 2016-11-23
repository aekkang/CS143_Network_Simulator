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

        # In bytes
        self.buffer_load = 0

        # Ends is a list that contains the object on either side of the list.
        # Its size at any time should be at most two.
        self.ends = []

        # Metric lists
        self.lost_packets = 0
        self.aggr_flow_rate = 0
        self.buf_occupancy = []
        self.packet_loss = []

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
            return

        self.buffer.append(buf_obj)
        self.aggr_flow_rate += 1
        self.buffer_load += pkt.size


    def buffer_get(self):
        pkt, time = self.buffer.pop(0)
        self.buffer_load -= pkt.size
        return (pkt, time)

    def buffer_empty(self):
        return len(self.buffer) == 0

    def update_metrics(self, time):
        bufload = float(self.buffer_load) / self.buffer_size * 100
        pktloss = self.lost_packets
        flowrate = self.aggr_flow_rate / time

        metrics.update_link(self.id, bufload, pktloss, flowrate, time)

        # To look into
        self.buf_occupancy.append(self.buffer_load)
        self.packet_loss.append(self.lost_packets)

    def __str__(self):
        return "<Link ID: " + str(self.id) + ", Link Rate: " + str(self.rate) + \
            ", Propogation Delay: " + str(self.prop_delay) + ", Buffer size: " + \
            str(self.buffer_size) + ", Buffer load: " + str(self.buffer_load) +\
             ", Ends: " + str(self.ends) + "ENDS>\n"

    __repr__ = __str__


