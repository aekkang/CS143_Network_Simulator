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


    def send(self):
        '''
        Sends a packet.
        '''
        pass

    def generate(self):
        '''
        Makes a packet.
        '''
        pass

    def receive(self, pkt, time):
        print (pkt.payload, time)
        if (isinstance(pkt, packet.Ack)):
            pkt.flow.receiveAck(pkt, time)
        
        else:
            #ack = packet.Ack(self, pkt.sender, pkt.number)
            ack = packet.makeAck(pkt)
            enqueue(event.SendPacket(time, ack, self.link, self))
            

    def __str__(self):
        return "<Host ID: " + str(self.id) + ", Address: " + str(self.address) +  \
            ", Link: " + str(self.link) + ">"

    __repr__ = __str__
