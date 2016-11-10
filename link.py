PACKET_SIZE = 1024.0

class Link:
    ids = []

    # Map of link ids to Link objects, this will be populated by the parser
    maps = {}

    def __init__(self, link_id, rate, prop_delay, buffer_size):
        # IDs start from 1.
        self.id = len(Link.ids) + 1
        Link.ids.append(self.id)

        self.rate = rate       # in bytes per second
        self.prop_delay = prop_delay
        self.buffer_size = buffer_size

        self.buffer = []
        self.buf_processing = False

    def buffer_add(self, pkt):
        self.buffer.append(pkt)

    def buffer_get(self):
        return self.buffer.pop(0)

    def buffer_empty(self):
        return len(self.buffer) == 0


