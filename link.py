PACKET_SIZE = 1024.0

class Link:
    ids = []

    def __init__(self, rate, prop_delay, link_buffer, ends):
        # IDs start from 1.
        self.id = len(ids) + 1
        ids.append(self.id)

        self.rate = rate       #in bytes per second
        self.prop_delay = prop_delay
        self.link_buffer = link_buffer
        self.ends = ends

    def buffer_add(self, pkt):
        self.link_buffer.append(pkt)

    def buffer_get(self, pkt):
        self.link_buffer.remove(pkt)

    def get_recipient(self, sender):
        for i in self.ends:
            if i != sender:
                return i

