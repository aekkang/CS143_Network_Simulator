class Packet:
    def __init__(self, meta, payload):
        self.meta = meta
        self.payload = payload

        self.size = 1024
        self.sender = "lol"
        self.recipient = "pls"

    # TODO: how do we handle ACKs?
