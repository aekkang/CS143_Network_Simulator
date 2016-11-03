PACKET_SIZE = 1024.0

class Link:
    ids = []

    def __init__(self, rate, prop_delay, link_buffer, ends):
        # IDs start from 1.
        self.id = len(Link.ids) + 1
        Link.ids.append(self.id)

        self.rate = rate       #in bytes per second
        self.prop_delay = prop_delay
        self.link_buffer = link_buffer
        self.buf_processing = False
        self.ends = ends

    def buffer_add(self, pkt):
        self.link_buffer.append(pkt)

    def buffer_get(self):
        return self.link_buffer.pop(0)

    def buffer_empty(self):
        return len(self.link_buffer) == 0


