from pqueue import event_queue, enqueue
import event
import packet

class Host:
    # Map of host ids to Host objects, this will be populated by the parser
    h_map = {}

    def __init__(self, host_id, link):
        self.id = host_id

        # Each host is connected to a single link.
        self.link = link

        # Hash table recording what packet we're expecting
        # from which flows.
        self.expected_pkt = {}
        self.received_pkts = {}

    def receive(self, pkt, time):
        # Pass ACKs to flows to handle congestion control and dropped packets
        if (isinstance(pkt, packet.Ack)):
            pkt.flow.receiveAck(pkt, time)
        
        else:
            # Only send ACKs for packets we have not yet recieved 
            # (next_pkt = pkt.number) or packets out of order
            # (next_pkt < pkt.number).
            # If first packet from flow, then set expected_pkt to 0.
            if self.expected_pkt.setdefault(pkt.flow.id, 0) <= pkt.number:

                # If the packet is the one we're expecting,
                # increment its value in next_packet.
                if self.expected_pkt[pkt.flow.id] == pkt.number:
                    self.expected_pkt[pkt.flow.id] += 1
                    while self.expected_pkt[pkt.flow.id] in \
                    self.received_pkts.setdefault(pkt.flow.id, []):
                        self.received_pkts[pkt.flow.id].remove(self.expected_pkt[pkt.flow.id])
                        self.expected_pkt[pkt.flow.id] += 1
                else:
                    self.received_pkts.setdefault(pkt.flow.id, []).append(pkt.number)

                ack = packet.makeAck(pkt.flow, self.expected_pkt[pkt.flow.id])
                enqueue(event.SendPacket(time, ack, self.link, self))

                pkt.flow.received_packets += 1

            # If the incoming packet has a number LESS THAN the one
            # we're expecting, it's a duplicate and we don't care
            # about it. Don't send an ACK.
            

    def __str__(self):
        return "<Host ID: " + str(self.id) + ", Address: " + str(self.address) +  \
            ", Link: " + str(self.link) + ">"

    __repr__ = __str__
