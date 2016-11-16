from math import ceil
from pqueue import event_queue, enqueue, get_global_time, qempty
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

        self.window_size = 100
        self.curr_pkt = 0
        self.num_packets = int(ceil(data_amt * 1.0e6 / packet.DataPkt.PACKET_SIZE))


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
        while (self.curr_pkt < min(self.num_packets, self.window_size)):
            pkt = packet.DataPkt(self.source, self.destination, \
                "PACKET %d" % self.curr_pkt, self.curr_pkt, self)
            enqueue(event.SendPacket(self.start_time, pkt, \
                self.source.link, self.source))
            self.curr_pkt += 1

        '''
        for i in range(num_packets):
            pkt = packet.Packet(self.source, self.destination, i, i)
            enqueue(event.SendPacket(1, pkt, self.source.link, self.source))
        '''
    def receiveAck(self, ack, curr_time):
        if (self.curr_pkt < self.num_packets):
            pkt = packet.DataPkt(self.source, self.destination, \
                "PACKET %d" % self.curr_pkt, self.curr_pkt, self)
            enqueue(event.SendPacket(curr_time, pkt, self.source.link, self.source))
            self.curr_pkt += 1


