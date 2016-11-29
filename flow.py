from math import ceil
from pqueue import event_queue, enqueue, get_global_time, qempty
import packet
import event

class Flow:

    f_map = {}

    INITIAL_SEND = 0
    DUP_SEND = 1

    def __init__(self, flow_id, source, destination, data_amt, start_time):
        self.id = flow_id
        self.source = source
        self.destination = destination
        # Data_amt is in megabytes.
        self.data_amt = data_amt
        self.start_time = start_time

        self.window_size = 1
        self.curr_pkt = 0
        self.num_packets = int(ceil(data_amt * 1.0e6 / packet.DataPkt.PACKET_SIZE))

        self.unacknowledged = {}
        self.timeout = 1.0
        self.dup_pkt = None

        # For TCP FAST
        self.min_RTT = 100.0
        self.curr_RTT = 0.0
        self.GAMMA = 0.5
        self.ALPHA = 15


    def __str__(self):
        return "<Flow ID: " + str(self.id) + ", Source: " + str(self.source) +  \
            ", Destination: " + str(self.destination) + ", Data Amount: " +  \
            str(self.data_amt) + ", Start time: " + str(self.start_time) + ">"

    __repr__ = __str__

    def startFlow(self):
        # While our window isn't filled yet, we create packets.
        while (self.curr_pkt < min(self.num_packets, self.window_size)):
            pkt = packet.DataPkt(self.source, self.destination, \
                "PACKET %d" % self.curr_pkt, self.curr_pkt, self)

            # We send the packet (put the event in the pqueue at the
            # flow's start time.
            enqueue(event.SendPacket(self.start_time, pkt, \
                self.source.link, self.source))
            
            enqueue(event.PacketTimeout(self.start_time + self.timeout, pkt))

            # We keep track of which packets we haven't received ACKS
            # for yet.
            self.unacknowledged[self.curr_pkt] = self.start_time
            self.curr_pkt += 1

        '''
        for i in range(num_packets):
            pkt = packet.Packet(self.source, self.destination, i, i)
            enqueue(event.SendPacket(1, pkt, self.source.link, self.source))
        '''
        # Fix receiveAck to be in this format:
        # 1. if ACK is a duplicate ACK
        #   - move into fast recovery state
        #   - window is W/2 + 1
        #   - set dup_ack_num = ack.number
        #   - increase window by +1 for every additional dup-ack
        #   - exit fast recovery state when a non-dup ack is received
        # 2. if not, update window
        #   - depends on algorithm: Reno or FAST
        # 3. (execute regardless of whether 1 or 2 happened) if we have space in our window (i.e. calculate window_size - unacknowledged)
        #   - send out that many packets
        #
    def receiveAck(self, ack, curr_time):
        # We recieve ACKs with number = the next packet it expects.
        # This means packet number (ack.number - 1) was received,
        # so we delete that packet num from the unacknowledged HT.

        # If that packet has already been acknowledged (i.e. not in
        # the HT) then we have a duplicate ACK for packet ack.number.
        if self.unacknowledged.get(ack.number - 1, None) == None:
            # If we receive a duplicate ACK we need to resend a packet
            if self.dup_pkt != ack.number:

                # Update what our current duplicate we're handling is.
                self.dup_pkt = ack.number

                # Remake the missing packet.
                print 'resending dropped packet ', ack.number

                print "checking for packet %d in map" % ack.number
                print self.unacknowledged.get(ack.number)

                pkt = packet.DataPkt(self.source, self.destination, \
                    "PACKET %d" % ack.number, ack.number, self)

                # Resend the packet.
                enqueue(event.SendPacket(curr_time, pkt, self.source.link, \
                 self.source))
                enqueue(event.PacketTimeout(curr_time + self.timeout, pkt))
                
                # Set the curr_pkt to the next packet that was dropped.
                self.curr_pkt = ack.number + 1

                # Edit the start time logged in the unack map.
                self.unacknowledged[ack.number - 1] = curr_time

                # Halve our window size.
                self.window_size = self.window_size / 2
                print "current packet ", self.curr_pkt

        # If we've successfully received an ACK for an UNACK'd packet,
        # we remove the packet from the map and update our RTT estimate.
        else:   
            # We can remove the correctly acknowledged packet from our
            # unacknowledged packets map
            for pktnum in self.unacknowledged:
                if pktnum < ack.number - 1:
                    self.unacknowledged.pop(pktnum)

            self.curr_RTT = curr_time - self.unacknowledged.pop(ack.number - 1)

            # Update our min_RTT
            if self.curr_RTT < self.min_RTT:
                self.min_RTT = self.curr_RTT

            # TCP FAST: Calculate our new window size
            self.window_size = min(2 * self.window_size, (1 - self.GAMMA) * \
                self.window_size + self.GAMMA * ((self.min_RTT / self.curr_RTT) * \
                self.window_size + self.ALPHA))

            print "new window size is ", self.window_size

        window_space = int(self.window_size - len(self.unacknowledged))

        for i in xrange(window_space):
            if (self.curr_pkt < self.num_packets):
                pkt = packet.DataPkt(self.source, self.destination, \
                    "PACKET %d" % self.curr_pkt, self.curr_pkt, self)

                # Send new packet + timeout event
                enqueue(event.SendPacket(curr_time, pkt, self.source.link, self.source))
                enqueue(event.PacketTimeout(curr_time + self.timeout, pkt))

                self.unacknowledged[self.curr_pkt] = curr_time
                self.curr_pkt += 1
                
        print "curr_pkt is ", self.curr_pkt
    
    def handleTimeout(self, pkt, curr_time):
        # If unacknowledged, resend the packet + its timeout event
        if pkt.number in self.unacknowledged:
            print 'handling packet timeout for packet ', pkt.number
            print 'time is ', curr_time
            enqueue(event.SendPacket(curr_time, pkt, self.source.link, \
             self.source))
            enqueue(event.PacketTimeout(curr_time + self.timeout, pkt))
    
