from math import ceil
from pqueue import event_queue, enqueue, get_global_time, qempty
import packet
import event
import metrics

class Flow:
    f_map = {}
    # Set by command-line arguments.
    TCP_ALG = ''

    def __init__(self, flow_id, source, destination, data_amt, start_time):
        self.id = flow_id
        self.source = source
        self.destination = destination
        # data_amt is in megabytes.
        self.data_amt = data_amt
        self.start_time = start_time

        self.window_size = 1
        self.curr_pkt = 0
        self.num_packets = int(ceil(data_amt * 1.0e6 / packet.DataPkt.PACKET_SIZE))

        self.done_sending = False

        self.unacknowledged = {}
        self.timeout = 1.0
        self.dup_pkt = None

        # For TCP Reno
        self.ssthreshold = 500.0 # Set threshold initially high
        self.dup_count = 0
        self.fr_flag = False

        # For TCP FAST
        self.min_RTT = 100.0
        self.curr_RTT = None
        self.prev_RTT = None
        self.RTTALPHA = 0.125
        self.GAMMA = 0.5
        self.ALPHA = 15
        self.update_period = 0.02

        self.last_dup_time = 0

        # Metric lists
        self.sent_packets = 0
        self.received_packets = 0
        self.prev_recv_packets = 0
        self.prev_time = 0


    def __str__(self):
        return "<Flow ID: " + str(self.id) + ", Source: " + str(self.source) +  \
            ", Destination: " + str(self.destination) + ", Data Amount: " +  \
            str(self.data_amt) + ", Start time: " + str(self.start_time) + ">"

    __repr__ = __str__

    def startFlow(self):
        # While our window isn't filled yet, we create packets.
        while (self.curr_pkt < min(self.num_packets, self.window_size)):
            self.makePacket("PACKET %d" % self.curr_pkt, self.curr_pkt, self.start_time)

            if self.TCP_ALG == 'fast':
                enqueue(event.UpdateWindow(self.start_time + self.update_period, self))

            # We keep track of which packets we haven't received ACKS
            # for yet.
            self.unacknowledged[self.curr_pkt] = self.start_time
            self.curr_pkt += 1
            self.sent_packets += 1

    def makePacket(self, payload, number, start_time):
        # Makes a new packet and then enqueues SendPacket and PacketTimeout
        # events.
        pkt = packet.DataPkt(self.source, self.destination, payload, number, self)

        # We send the packet (put the event in the pqueue at the flow's start
        # time.
        enqueue(event.SendPacket(start_time, pkt, self.source.link, self.source))
        enqueue(event.PacketTimeout(start_time + self.timeout, pkt))

    def receiveAck(self, ack, curr_time):
        # We recieve ACKs with number = the next packet it expects.
        # This means packet number (ack.number - 1) was received,
        # so we delete that packet num from the unacknowledged HT.

        # If that packet has already been acknowledged (i.e. not in
        # the HT) then we have a duplicate ACK for packet ack.numberself.
        if self.unacknowledged.get(ack.number - 1, None) == None:          
            # (1): This is a new duplicate packet we're dealing with.
            if self.dup_pkt != ack.number:
                # Update what our current duplicate we're handling is.
                self.dup_pkt = ack.number
                self.dup_count = 1
            else:
                self.dup_count += 1

            if self.dup_count == 3:
                self.halve_window(ack, curr_time, tcp_algo=self.TCP_ALG)
            elif self.dup_count > 3:
                self.fast_recovery(curr_time, tcp_algo=self.TCP_ALG)

        # If we've successfully received an ACK for an UNACK'd packet,
        # we remove the packet from the map and update our RTT estimate.
        else:
            # We can remove the correctly acknowledged packet from our
            # unacknowledged packets map
            if self.fr_flag:
                if self.TCP_ALG == "reno":
                    self.window_size = self.ssthreshold
                self.fr_flag = False

            for pktnum in self.unacknowledged.keys():
                if pktnum < ack.number - 1:
                    self.unacknowledged.pop(pktnum)

            self.adjust_window(ack, curr_time, self.TCP_ALG)

        if self.curr_pkt == self.num_packets:
            self.done_sending = True

        # Send as many more packets as the window allows.
        window_space = max(int(self.window_size - len(self.unacknowledged)), 0)

        for i in xrange(window_space):
            if (self.curr_pkt < self.num_packets):
                self.makePacket("PACKET %d" % self.curr_pkt, self.curr_pkt, curr_time)

                self.unacknowledged[self.curr_pkt] = curr_time
                self.curr_pkt += 1
                self.sent_packets += 1

        if self.curr_pkt % 100 == 0:
            print "current packet is %d from flow %s" % (self.curr_pkt, self.id)


    def update_metrics(self, time):
        send_rate = self.sent_packets / (time + 1)
        rec_rate = self.received_packets / (time + 1)

        if (time - self.prev_time) >= 0.1:
            recv_packets = self.received_packets - self.prev_recv_packets
            recv_rate = (recv_packets * 1024 * 8.0)\
                        / ((1024 ** 2) * (time - self.prev_time))
            self.prev_time = time
            self.prev_recv_packets = self.received_packets
            update_flow_rate = True
            
        else:
            recv_rate = 0
            update_flow_rate = False


        if self.done_sending is False:
            metrics.update_flow(self.id, send_rate, recv_rate, self.curr_RTT, 
                self.window_size, time, update_flow_rate)

    def fast_window(self):
        if self.curr_RTT != None:
            return min(2 * self.window_size, (1 - self.GAMMA) * \
                    self.window_size + self.GAMMA * ((self.min_RTT / self.curr_RTT) * \
                    self.window_size + self.ALPHA))
        else:
            return 2 * self.window_size

    def halve_window(self, ack, curr_time, tcp_algo='fast'):
        # Halve our window size.
        self.window_size /= 2

        if tcp_algo == 'reno':
            self.ssthreshold = max(self.window_size, 2)
            self.window_size += 3

        # Remake the missing packet.
        print '\tresending dropped packet', ack.number
        self.makePacket("PACKET %d" % ack.number, ack.number, curr_time)

        # Set the curr_pkt to the next packet that was dropped.
        # self.curr_pkt = ack.number + 1

        # Edit the start time logged in the unack map.
        self.unacknowledged[ack.number - 1] = curr_time
        print "\tnew window size is", self.window_size
        # print "current packet", self.curr_pkt

        self.fr_flag = True


    def fast_recovery(self, curr_time, tcp_algo='fast'):
        self.window_size += 1
        self.fr_flag = True

        # Send as many more packets as the window allows.
        window_space = max(int(self.window_size - len(self.unacknowledged)), 0)

        for i in xrange(window_space):
            if (self.curr_pkt < self.num_packets):
                self.makePacket("PACKET %d" % self.curr_pkt, self.curr_pkt, curr_time)

                self.unacknowledged[self.curr_pkt] = curr_time
                self.curr_pkt += 1

    def adjust_window(self, ack, curr_time, tcp_algo='fast'):

        # If this is not the first duplicate ACK for a given
        # dup ACK number, then we do fast recovery stuff, i.e.
        # adding 1 to the window size.

        self.prev_RTT = self.curr_RTT
        self.curr_RTT = curr_time - self.unacknowledged.pop(ack.number - 1)

        if tcp_algo == 'fast':
            
            # Update our min_RTT
            if self.curr_RTT < self.min_RTT:
                self.min_RTT = self.curr_RTT
            if self.min_RTT < 0.0005:
                self.min_RTT = self.curr_RTT

            if self.prev_RTT != None:
                self.curr_RTT = self.RTTALPHA * self.curr_RTT + \
                (1 - self.RTTALPHA) * self.prev_RTT

        else:
            # If received an ACK and in slow start phase
            # (i.e. window size < threshold), then increase
            # window size by 1 per ACK received.
            if self.window_size < self.ssthreshold:
                self.window_size = self.window_size + 1

            # If we are in congestion avoidance mode,
            # increase the window size by 1 / W per ACK.
            else:
                self.window_size = self.window_size + (1.0 / self.window_size)

    
    def handleTimeout(self, pkt, curr_time):
        # If unacknowledged, resend the packet + its timeout event
        if pkt.number in self.unacknowledged:
            enqueue(event.SendPacket(curr_time, pkt, self.source.link, \
             self.source))
            enqueue(event.PacketTimeout(curr_time + self.timeout, pkt))
            self.unacknowledged[pkt.number] = curr_time
    
