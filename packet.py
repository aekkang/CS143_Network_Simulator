class Packet:
    def __init__(self, meta, payload):
        self.meta = meta
        self.payload = payload

    # TODO: how do we handle ACKs?
