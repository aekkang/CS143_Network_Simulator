class Link:
    ids = []

    def __init__(self, rate, prop_delay, link_buffer):
        # IDs start from 1.
        self.id = len(ids) + 1
        ids.append(self.id)

        self.rate = rate
        self.prop_delay = prop_delay
        self.link_buffer = link_buffer
