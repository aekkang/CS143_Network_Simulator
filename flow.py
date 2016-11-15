from math import ceil
from pqueue import event_queue, enqueue
import packet
import event

class Flow:

    f_map = {}

    def __init__(self, flow_id, source, destination, data_amt, start_time):
        self.id = flow_id
        self.source = source
        self.destination = destination
        # Data_amt is in megabytes.
        self.data_amt = data_amt
        self.start_time = start_time


    def __str__(self):
        return "<Flow ID: " + str(self.id) + ", Source: " + str(self.source) +  \
            ", Destination: " + str(self.destination) + ", Data Amount: " +  \
            str(self.data_amt) + ", Start time: " + str(self.start_time) + ">"

    __repr__ = __str__

    def startFlow(self):
        # Figure out how many packets to send.
        # This is a fixed amount P = data_amt/pkt_size
        # Where pkt_size is 1024 bytes.

        # =====TODO: put PACKET_SIZE as a global variable for reference?====

        num_packets = int(ceil(self.data_amt * 1.0e6 / packet.Packet.PACKET_SIZE))

        for i in range(num_packets):
            pkt = packet.Packet(self.source, self.destination, i)
            enqueue(event.SendPacket(1, pkt, self.source.link, self.source))
