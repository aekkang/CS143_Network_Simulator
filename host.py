from pqueue import event_queue, enqueue
import event
import packet

class Host:
    # List of existing addresses
    addresses = []

    # Map of host ids to Host objects, this will be populated by the parser
    maps = {}

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

        # PARSER:
        # Map the host_id to this object in the map
        # maps[host_id] = self

    
    def get_host(host_id):
        '''
        Returns a host given a host_id, or throws a KeyError 
        if the key is invalid
        '''
        return maps[host_id]

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
        print (pkt.payload)
        if (isinstance(pkt, packet.Ack)):
            return;
        notack = packet.Ack(self, pkt.sender)
        enqueue(event.SendPacket(time, notack, self.link))
