class Packet(object):
    def __init__(self, sender, recipient, payload, number, size, flow):
        self.size = size
        self.sender = sender
        self.recipient = recipient
        self.payload = payload
        self.number = number
        self.flow = flow


class Ack(Packet):
    ACK_SIZE = 64

    # Inheritance syntax from
    # Source: http://stackoverflow.com/questions/9698614/
    #         super-raises-typeerror-must-be-type-not-classobj-for-new-style-class
    def __init__(self, sender, recipient, number, flow):
        super(self.__class__, self).__init__(sender, recipient, \
            "ACK %d" % number, number, Ack.ACK_SIZE, flow)

def makeAck(pkt, pkt_number):
    return Ack(pkt.recipient, pkt.sender, pkt_number, pkt.flow)


class DataPkt(Packet):
    PACKET_SIZE = 1024

    def __init__(self, sender, recipient, payload, number, flow):
        super(self.__class__, self).__init__(sender, recipient, payload, \
            number, DataPkt.PACKET_SIZE, flow)
