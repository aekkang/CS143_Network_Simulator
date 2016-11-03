from pqueue import event_queue, enqueue
import event
import packet

class Host:
    # List of existing addresses
    addresses = []

    def __init__(self, link):
        # Addresses start from 1.
        self.address = len(Host.addresses) + 1
        Host.addresses.append(self.address)

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
        print (pkt.payload)
        if (isinstance(pkt, packet.Ack)):
            return;
        notack = packet.Ack(self, pkt.sender)
        enqueue(event.SendPacket(time, notack, self.link))
