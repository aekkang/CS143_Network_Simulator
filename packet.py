class Packet(object):
    def __init__(self, sender, recipient, payload, number, size, flow):
        self.size = size
        self.sender = sender
        self.recipient = recipient
        self.payload = payload
        self.number = number
        self.flow = flow

    def __str__(self):
        return "<Packet Payload: " + str(self.payload) + ", Size: " + str(self.size) +  \
            ", Sender: " + str(self.sender) + ", Recipient: " +  \
            str(self.recipient) + ">"

    __repr__ = __str__

class Ack(Packet):
    ACK_SIZE = 64

    # Inheritance syntax from
    # Source: http://stackoverflow.com/questions/9698614/
    #         super-raises-typeerror-must-be-type-not-classobj-for-new-style-class
    def __init__(self, sender, recipient, number, flow):
        super(self.__class__, self).__init__(sender, recipient, \
            "ACK %d" % number, number, Ack.ACK_SIZE, flow)

def makeAck(pkt):
    return Ack(pkt.recipient, pkt.sender, pkt.number, pkt.flow)


class RtAck(Packet):
    def __init__(self, rtpkt):
        super(self.__class__, self).__init__(rtpkt.recipient, rtpkt.sender, \
            "RT ACK", 0, Ack.ACK_SIZE, None)
        self.rtpkt = rtpkt


class DataPkt(Packet):
    PACKET_SIZE = 1024

    def __init__(self, sender, recipient, payload, number, flow):
        super(self.__class__, self).__init__(sender, recipient, payload, \
            number, DataPkt.PACKET_SIZE, flow)

class RoutingPkt(Packet):
    PACKET_SIZE = 64

    def __init__(self, sender, recipient, distvec, bf_round):
        super(self.__class__, self).__init__(sender, recipient, "RtPkt", \
            0, RoutingPkt.PACKET_SIZE, None)
        self.distvec = distvec
        self.bf_round = bf_round

