class Packet(object):
    PACKET_SIZE = 1024
    def __init__(self, sender, recipient, payload, size=PACKET_SIZE):
        self.size = size
        self.sender = sender
        self.recipient = recipient
        self.payload = payload

    def NewPacket(self, meta, payload):
        ''' If this is really necessary '''
        Packet.__init__(meta.sender, meta.recipient, payload, Packet.PACKET_SIZE)

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
    def __init__(self, sender, recipient):
        super(self.__class__, self).__init__(sender, recipient, "ACK", Ack.ACK_SIZE)
