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
        self.next_pkt = {}

    def receive(self, pkt, time):
        print (pkt.payload, time)
        if (isinstance(pkt, packet.Ack)):
            pkt.flow.receiveAck(pkt, time)
        
        else:
            # If the incoming packet has a number greater than the one
            # we're expecting, a packet has been dropped.
            if self.next_pkt.setdefault(pkt.flow, 1) <= pkt.number:
                # Makes an ACK for the packet the recipient is expecting from
                # a given flow. If this is the first packet the host has
                # received from a flow, it expects pkt no. 1.
                print 'recieved pkt ', pkt.number, ' sending ack ', self.next_pkt[pkt.flow]
                ack = packet.makeAck(pkt, self.next_pkt[pkt.flow])
                enqueue(event.SendPacket(time, ack, self.link, self))

                # If the packet is the one we're expecting,
                # increment its value in next_packet.
                if self.next_pkt[pkt.flow] == pkt.number:
                    self.next_pkt[pkt.flow] += 1

            # If the incoming packet has a number LESS THAN the one
            # we're expecting, it's a duplicate and we don't care
            # about it. Don't send an ACK.
            

    def __str__(self):
        return "<Host ID: " + str(self.id) + ", Address: " + str(self.address) +  \
            ", Link: " + str(self.link) + ">"

    __repr__ = __str__
