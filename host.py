from pqueue import event_queue, enqueue
import event
import packet

class Host:
    # List of existing addresses
    addresses = []

    # Map of host ids to Host objects, this will be populated by the parser
    h_map = {}

    # TODO: Need to decide how addresses are determined, and whether
    # they're passed in from input or generated in this constructor

    # Each host contains an address (field type?), connecting link,
    # and id (string).
    def __init__(self, host_id, link):
        # Addresses start from 1.
        self.address = len(Host.addresses) + 1
        Host.addresses.append(self.address)

        self.id = host_id

        # Each host is connected to a single link.
        self.link = link

        # Hash table recording what packet we're expecting
        # from which flow.
        self.expected_pkt = {}

    def receive(self, pkt, time):
        print (pkt.payload, time)
        if (isinstance(pkt, packet.Ack)):
            pkt.flow.receiveAck(pkt, time)
        
        else:
            # Only send ACKs for packets we have not yet recieved 
            # (next_pkt = pkt.number) or packets out of order
            # (next_pkt < pkt.number).
            # If first packet from flow, then set expected_pkt to 0.
            if self.expected_pkt.setdefault(pkt.flow, 0) <= pkt.number:

                # If the packet is the one we're expecting,
                # increment its value in next_packet.
                if self.expected_pkt[pkt.flow] == pkt.number:
                    self.expected_pkt[pkt.flow] += 1

                ack = packet.makeAck(pkt, self.expected_pkt[pkt.flow])
                enqueue(event.SendPacket(time, ack, self.link, self))

            # If the incoming packet has a number LESS THAN the one
            # we're expecting, it's a duplicate and we don't care
            # about it. Don't send an ACK.
            

    def __str__(self):
        return "<Host ID: " + str(self.id) + ", Address: " + str(self.address) +  \
            ", Link: " + str(self.link) + ">"

    __repr__ = __str__
